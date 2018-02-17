# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.urls import reverse

from django.db import transaction
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from mimetypes import guess_type

from MIT.models import *
from MIT.forms import *

# Fetch stock info using google finance
from client import get_price_data, get_prices_data, get_open_close_data
import json
from django.utils import timezone

# from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail

@transaction.atomic
def register(request):
    context = {}
    #if method is get, always dispally the raw content
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'registration.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form
    # Validates the form.
    if not form.is_valid():
        return render(request, 'registration.html', context)
    # otherwise, create new user & player and add into db
    new_user = form.save()
    token = default_token_generator.make_token(new_user)
    email_body = """
    Welcome to MIT! Please click the link below to verify your email
    address and complete the registration of your account:

    http://%s%s
    """ % (request.get_host(), reverse('confirm_email', args=(new_user.username, token)))
    send_mail(subject="Verify your email address", message=email_body,
    from_email="lrao@andrew.cmu.com",recipient_list=[new_user.email])

    return render(request, 'auto_email_sent.html', context)

def auto_email(request):
    context = {}
    return render(request, 'password_reset_confirm.html', context)

@transaction.atomic
def confirm_email(request, username, token):
    user = get_object_or_404(User, username=username)

    if not default_token_generator.check_token(user, token):
        raise Http404
    user.is_active = True
    user.save()
    new_player = Player(user=user)
    new_player.save()
    # login newly authenticated user
    login(request, user)
    return redirect(reverse('home'))

@login_required
def game_overview(request, game_id):
    context = {}
    game = get_object_or_404(Game, id=game_id)
    player = get_object_or_404(Player, user=request.user)

    context['game'] = game
    context['player'] = player
    if GameInfo.objects.filter(game__exact=game, player__exact=player):
        context['join'] = False
    else:
        context['join'] = True
    return render(request, 'overview.html', context)

@transaction.atomic
@login_required
def create_game(request):
    context = {}

    if request.method == 'GET':
        context['form'] = CreateGameForm()
        return render(request, 'create_game.html', context)

    player = get_object_or_404(Player, user=request.user)
    new_game = Game(creator=player)
    form = CreateGameForm(request.POST, instance=new_game)

    if not form.is_valid():
        context['form'] = form
        return render(request, 'create_game.html', context)

    form.save()
    return redirect(reverse('game_overview', kwargs={'game_id':new_game.id}))


@login_required
def my_game_list(request):
    context = {}

    player = get_object_or_404(Player, user=request.user)
    context['player'] = player
    game_id_list = GameInfo.objects.values_list('game_id', flat=True).filter(player=player)
    context['games'] = Game.objects.filter(id__in=game_id_list)

    return render(request, 'game_list.html', context)

@login_required
def find_game(request):
    context = {}
    #find all the games in db
    games = Game.objects.order_by('-start_time')[:]
    context['games'] = games
    player = get_object_or_404(Player, user=request.user)
    context['player'] = player

    return render(request, 'find_game.html', context)

@login_required
def search_game(request):
    context = {}
    # if no use input
    if 'name' not in request.GET:
        return redirect(reverse('find_game'))
    #find ALL the games in db that contains name key word
    games = Game.objects.filter(name__icontains=request.GET['name'])
    context['games'] = games
    player = get_object_or_404(Player, user=request.user)
    context['player'] = player

    return render(request, 'find_game.html', context)

@transaction.atomic
@login_required
def join_game(request, game_id):
    context = {}
    # which user is joining the game
    player = get_object_or_404(Player, user=request.user)
    # which game is the user joining
    game = get_object_or_404(Game, id=game_id)
    # game participants increment by one
    game.counter += 1
    game.save()

    gameinfo = GameInfo(player=player, game=game)
    gameinfo.remaining_balance = game.starting_balance
    gameinfo.net_worth = game.starting_balance
    gameinfo.yesterday_net_worth = game.starting_balance
    gameinfo.save()
    return redirect(reverse('game_overview', kwargs={'game_id':game_id}))

@transaction.atomic
@login_required
def leave_game(request, game_id):
    context = {}
    # which user is leaving the game
    player = get_object_or_404(Player, user=request.user)
    # which game is the user leaving
    game = get_object_or_404(Game, id=game_id)
    # game participants decrement by one
    game.counter -= 1
    game.save()

    # delete every txn related to this player in this game
    Transaction.objects.filter(game__exact=game, creator__exact=player).delete()
    # delete every stock info related to this player in this game
    StockInfo.objects.filter(game__exact=game, player__exact=player).delete()
    # delete gameinfo object
    gameinfo = GameInfo.objects.get(game__exact=game, player__exact=player)
    gameinfo.delete()
    return redirect(reverse('game_overview', kwargs={'game_id':game_id}))

@login_required
def get_index_info(request, index_name):
    params = {}
    params['p'] = '1Y'
    params['i'] =  '86400' # Interval size in seconds ("86400" = 1 day intervals)
    if index_name == "DowJones":
        params['q'] = ".DJI"
        params['x'] = "INDEXDJX"
    elif index_name == "SP500":
        params['q'] = "SPX"
        params['x'] = "INDEXCBOE"
    elif index_name == "Nasdaq":
        params['q'] = ".IXIC"
        params['x'] = "INDEXNASDAQ"
    # else, using alpha vantage to get stock info on daily basis
    else:
        params['p'] = '1d'
        params['i'] =  '600'
        params['q'] = index_name

    info = get_price_data(params)
    return HttpResponse(info, content_type='text/csv')

@transaction.atomic
@login_required
def get_share_info(request, game_id, player_id):
    context = {}
    player = get_object_or_404(Player, id=player_id)
    game = get_object_or_404(Game, id=game_id)

    if 'stock_name' in request.GET and 'stock_type' in request.GET:
        # print request.GET['stock_name']
        # print request.GET['stock_type']

        if request.GET['stock_type'] == "SELL":
            search_type = "BUY"
        else:
            search_type = "SHORT"

        # find stock to sell or cover
        target = StockInfo.objects.filter(stock_name__exact=request.GET['stock_name'],
                stock_type__exact=search_type,game__exact=game,
                player__exact=player)
        if len(target) == 0:
            return HttpResponse(json.dumps({'name':request.GET['stock_name'], 'share':0}),
                            content_type='application/json; charset=utf8')
        else:
            return HttpResponse(json.dumps({'name':request.GET['stock_name'], 'share':target[0].shares}),
                            content_type='application/json; charset=utf8')

    elif 'stock_type' in request.GET and request.GET['stock_type'] == "NETWORTH":
        gameinfo = GameInfo.objects.get(game__exact=game, player__exact=player)
        return HttpResponse(json.dumps({'netWorth':gameinfo.net_worth}),
                        content_type='application/json; charset=utf8')

    # no stock name input, using this to draw portfolio image
    else:
        stock_name_list = []
        stock_share_list = []

        total_share = StockInfo.objects.filter(player=player, game=game).aggregate(sum=Sum('shares'))
        if total_share['sum']:
            total_share = float(total_share['sum'])
            stocks = StockInfo.objects.filter(player__exact=player, game__exact=game)

            # print total_share
            for stock in stocks:
                if stock.stock_type == "SHORT":
                    stock_name_list.append(stock.stock_name+" (SHORT) ")
                else:
                    stock_name_list.append(stock.stock_name)
                stock_share_list.append(round(stock.shares/total_share * 100.0,2))

        return HttpResponse(json.dumps({'name':stock_name_list, 'percent':stock_share_list}),
                        content_type='application/json; charset=utf8')

@login_required
def get_join_info(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    player = get_object_or_404(Player, user=request.user)
    join = False

    if GameInfo.objects.filter(game__exact=game, player__exact=player):
        join = False
    else:
        join = True
    return HttpResponse(json.dumps({'join':join}),
                        content_type='application/json; charset=utf8')

@login_required
def stock(request, game_id):
    context = {}
    game = get_object_or_404(Game, id=game_id)
    player = get_object_or_404(Player, user=request.user)
    context['player'] = player
    context['game'] = game
    params = []
    params.append({'q': ".DJI", 'x': "INDEXDJX"})
    params.append({'q': "SPX", 'x': "INDEXCBOE"})
    params.append({'q': ".IXIC", 'x': "INDEXNASDAQ"})
    # return a dataframe
    info = get_open_close_data(params,'1M')
    # extract useful info
    today_stats = info.iloc[-1]
    yesterday_stats = info.iloc[-2]
    month_stats = info.iloc[0]
    time = info.index[-1]

    index_names = ['.DJI', 'SPX', '.IXIC']
    for index_name in index_names:
        value = index_name+'_Open'
        context[index_name.replace(".", "") + 'Value'] = today_stats[value]
        net = index_name+'_Close'
        context[index_name.replace(".", "") + 'Net'] = today_stats[net] - yesterday_stats[net]
        context[index_name.replace(".", "") + 'Chance'] = round(float(context[index_name.replace(".", "") + 'Net'])
                                                        /float(yesterday_stats[net]) * 100.0, 2)
        context[index_name.replace(".", "") + 'Month'] = round(float(today_stats[net] - month_stats[net])
                                                        /float(month_stats[net]) * 100.0, 2)

    context['IndexTime'] = time
    return render(request, 'stock.html', context)

@transaction.atomic
@login_required
def buy_stock(request, game_id):
    context = {}
    # extract game info
    player = get_object_or_404(Player, user=request.user)
    game = get_object_or_404(Game, id=game_id)

    new_transaction = Transaction(creator=player, game=game)
    form = TransactionForm(request.POST, instance=new_transaction)
    # it is impossible that the form is invalid
    if not form.is_valid():
        context['game'] = game
        context['player'] = player
        context['form'] = form
        # if you can trade stock, then you must already joined the game
        context['join'] = False
        return render(request, 'overview.html', context)
    form.save()
    # check if stock record already exist
    try:
        Stock.objects.get(stock_name=request.POST['stock_name'])
    except ObjectDoesNotExist:
        new_stock = Stock(stock_name=request.POST['stock_name'],
                    current_price=float(request.POST['price']))
        stock_price_update(new_stock)
        # when FIRST create, populate with current_price
        new_stock.yesterday_price = new_stock.current_price
        new_stock.save()

    trade_type = request.POST['transaction_type']
    if trade_type.endswith("LIMIT") or trade_type.endswith("STOP"):
        pending_transaction_update(new_transaction)
        return redirect(reverse('portfolio', kwargs={'game_id':game_id, 'player_id':player.id}))

    # otherwise, trade_type is "BUY" or "SELL SHORT"
    buy_stock_helper(new_transaction)
    # update transaction time
    new_transaction.transaction_time = timezone.now()
    new_transaction.save()
    return redirect(reverse('portfolio', kwargs={'game_id':game_id, 'player_id':player.id}))

@transaction.atomic
@login_required
def sell_stock(request, game_id):
    context = {}
    # extract game info
    player = get_object_or_404(Player, user=request.user)
    game = get_object_or_404(Game, id=game_id)

    new_transaction = Transaction(creator=player, game=game)
    form = TransactionForm(request.POST, instance=new_transaction)
    # it is impossible that the form is invalid
    if not form.is_valid():
        context['game'] = game
        context['player'] = player
        context['form'] = form
        # if you can trade stock, then you must already joined the game
        context['join'] = False
        return render(request, 'overview.html', context)
    # create a new transaction record
    form.save()

    trade_type = request.POST['transaction_type']
    if trade_type.endswith("LIMIT") or trade_type.endswith("STOP"):
        pending_transaction_update(new_transaction)
        return redirect(reverse('portfolio', kwargs={'game_id':game_id, 'player_id':player.id}))
    # otherwise, trade_type is "SELL" or "COVER"
    # update player's game info
    sell_stock_helper(new_transaction)
    # update transaction time
    new_transaction.transaction_time = timezone.now()
    new_transaction.save()
    return redirect(reverse('portfolio', kwargs={'game_id':game_id, 'player_id':player.id}))

@transaction.atomic
@login_required
def portfolio(request, game_id, player_id):
    context = {}

    game = get_object_or_404(Game, id=game_id)
    player = get_object_or_404(Player, id=player_id)
    context['game'] = game
    # update player's ranking info
    ranking_update(game)

    current_short_price = 0.0
    buy_stock_price = 0.0
    short_stock_price = 0.0
    stocks = StockInfo.objects.filter(player__exact=player, game__exact=game)

    for stock in stocks:
        current_price = stock.get_current_price()
        if stock.stock_type == "BUY":
            buy_stock_price += stock.shares * current_price
        if stock.stock_type == "SHORT":
            short_stock_price += stock.total_value
            current_short_price += stock.shares * current_price

    total_stock_price = buy_stock_price + short_stock_price
    game_info = GameInfo.objects.get(player__exact=player, game__exact=game)
    game_info.short_reserve = round(current_short_price, 2)
    game_info.net_worth = round(game_info.remaining_balance + total_stock_price - game_info.short_reserve, 2)
    game_info.overall_gains = round(game_info.net_worth - game.starting_balance, 2)
    game_info.overall_return = round((game_info.overall_gains/game.starting_balance) * 100, 2)
    game_info.save()

    context['game_info'] = game_info
    context['stocks'] = stocks
    context['today_gains'] = round(game_info.net_worth - game_info.yesterday_net_worth, 2)
    context['transactions'] = Transaction.objects.filter(creator__exact=player, game__exact=game)
    context['player'] = get_object_or_404(Player, user=request.user)

    return render(request, 'Portfolio.html', context)

@transaction.atomic
@login_required
def ranking(request, game_id):
    context = {}
    # extract basic info
    game = get_object_or_404(Game, id=game_id)
    player = get_object_or_404(Player, user=request.user)

    context['game'] = game
    context['player'] = player
    context['game_infos'] = ranking_update(game)
    return render(request, 'ranking.html', context)

# daily update yesterday_net_worth and delete game if it has ended
# call by celery task
@transaction.atomic
def update_daily():
    # update ALL the game info object
    game_infos = GameInfo.objects.all()
    for game_info in game_infos:
        game_info.yesterday_net_worth = game_info.net_worth

    games = Game.objects.all()
    current_time = timezone.now()
    for game in games:
        # check whether this game has end
        if current_time > game.end_time:
            game.delete()

# periodically update stock price and deal with pending transaction
# call by celery task
@transaction.atomic
def update():
    # update ALL the stocks' current price
    stocks = Stock.objects.all()
    for stock in stocks:
        stock_price_update(stock)

    # deal with "BUY LIMIT" transaction type
    transactions = Transaction.objects.all()
    for txn in transactions:
        pending_transaction_update(txn)

# helper function, updating stock price(using google finance api)
@transaction.atomic
def stock_price_update(stock):
    params = []
    params.append({'q': stock.stock_name})
    info = get_open_close_data(params,'1d')
    # extract useful info
    today_stats = info.iloc[0]
    stock.current_price = float(today_stats[stock.stock_name+'_Close'])
    stock.save()

# helper function, updating pending transaction if necessary
@transaction.atomic
def pending_transaction_update(txn):
    # if this is not a pending transaction type, return immediately
    if txn.transaction_type == "BUY" or txn.transaction_type == "SELL":
        return

    # deal with "BUY LIMIT" transaction type
    if txn.transaction_type == "BUY LIMIT":
        # ONLY trigger when current price is lower than setting price
        if txn.get_current_price() <= txn.price:
            txn.transaction_type="BUY"
            txn.transaction_time = timezone.now()
            txn.price = txn.get_current_price()
            # invoke helper function, update transaction info if succeed
            if buy_stock_helper(txn):
                txn.save()

    # deal with "COVER LIMIT" transaction type
    elif txn.transaction_type == "COVER LIMIT":
        # ONLY trigger when current price is lower than setting price
        if txn.get_current_price() <= txn.price:
            txn.transaction_type="COVER"
            txn.transaction_time = timezone.now()
            txn.price = txn.get_current_price()
            txn.save()
            # invoke helper function
            sell_stock_helper(txn)

    # deal with "BUY STOP" transaction type
    elif txn.transaction_type == "BUY STOP":
        # ONLY trigger when current price is higher than setting price
        if txn.get_current_price() >= txn.price:
            txn.transaction_type="BUY"
            txn.transaction_time = timezone.now()
            txn.price = txn.get_current_price()
            # invoke helper function, update transaction info if succeed
            if buy_stock_helper(txn):
                txn.save()

    # deal with "COVER STOP" transaction type
    elif txn.transaction_type == "COVER STOP":
        # ONLY trigger when current price is higher than setting price
        if txn.get_current_price() >= txn.price:
            txn.transaction_type="COVER"
            txn.transaction_time = timezone.now()
            txn.price = txn.get_current_price()
            txn.save()
            # invoke helper function
            sell_stock_helper(txn)

    # deal with "SELL LIMIT" transaction type
    elif txn.transaction_type == "SELL LIMIT":
        # ONLY trigger when current price is higher than setting price
        if txn.get_current_price() >= txn.price:
            txn.transaction_type="SELL"
            txn.transaction_time = timezone.now()
            txn.price = txn.get_current_price()
            txn.save()
            # invoke helper function
            sell_stock_helper(txn)

    # deal with "COVEr LIMIT" transaction type
    elif txn.transaction_type == "SHORT LIMIT":
        # ONLY trigger when current price is higher than setting price
        if txn.get_current_price() >= txn.price:
            txn.transaction_type="SHORT"
            txn.transaction_time = timezone.now()
            txn.price = txn.get_current_price()
            # invoke helper function, update transaction info if succeed
            if buy_stock_helper(txn):
                txn.save()

    # deal with "BUY STOP" transaction type
    elif txn.transaction_type == "SELL STOP":
        # ONLY trigger when current price is lower than setting price
        if txn.get_current_price() <= txn.price:
            txn.transaction_type="SELL"
            txn.transaction_time = timezone.now()
            txn.price = txn.get_current_price()
            txn.save()
            # invoke helper function
            sell_stock_helper(txn)

    # deal with "COVER STOP" transaction type
    elif txn.transaction_type == "SHORT STOP":
        # ONLY trigger when current price is lower than setting price
        if txn.get_current_price() <= txn.price:
            txn.transaction_type="SHORT"
            txn.transaction_time = timezone.now()
            txn.price = txn.get_current_price()
            # invoke helper function, update transaction info if succeed
            if buy_stock_helper(txn):
                txn.save()

# helper function
def buy_stock_helper(transaction):
    game = transaction.game
    player = transaction.creator
    stock_name = transaction.stock_name
    trade_type = transaction.transaction_type
    trade_share = transaction.shares
    trade_price = transaction.price
    trade_value = trade_share * trade_price

    # update player's game info
    gameinfo = GameInfo.objects.get(game__exact=game, player__exact=player)
    # only "BUY" substract remaining balance
    if trade_type=="BUY":
        if gameinfo.remaining_balance >= trade_value:
            gameinfo.remaining_balance -= trade_value
        else:
            # transaction failed
            return False
    gameinfo.save()

    # update stockinfo, create new one if necessary
    target = StockInfo.objects.filter(stock_name__exact=stock_name,
            stock_type__exact=trade_type,game__exact=game, player__exact=player)
    if len(target) == 0:
        new_stockinfo = StockInfo(stock_name=stock_name,stock_type=trade_type,
                shares=trade_share,total_value=trade_value,player=player,game=game)
        # print new_stock
        new_stockinfo.save()
    else:
        old_stockinfo = target[0]
        old_stockinfo.shares += trade_share
        old_stockinfo.total_value += trade_value
        # print old_stockinfo
        old_stockinfo.save()
    return True

# helper function
def sell_stock_helper(transaction):
    game = transaction.game
    player = transaction.creator
    stock_name = transaction.stock_name
    trade_share = transaction.shares
    trade_type = transaction.transaction_type
    trade_price = transaction.price
    trade_value = trade_share * trade_price

    if trade_type == "SELL":
        search_type = "BUY"
    elif trade_type == "COVER":
        search_type = "SHORT"

    # update stock
    target = StockInfo.objects.filter(stock_name__exact=stock_name,
            stock_type__exact=search_type,game__exact=game, player__exact=player)
    if len(target) == 0:
        raise Http404("No stock can be found")
    else:
        old_stockinfo = target[0]
        old_stockinfo.shares -= trade_share
        # if no share left
        if old_stockinfo.shares == 0:
            old_stockinfo.delete()
        else:
            old_stockinfo.total_value -= trade_value
            old_stockinfo.save()
    # update player's game info
    gameinfo = GameInfo.objects.get(game__exact=game, player__exact=player)
    # only "SELL" add back remaining balance
    if trade_type == "SELL":
        gameinfo.remaining_balance += trade_value

    gameinfo.save()

# helper function, updating player's ranking info
def ranking_update(game):
    game_infos = GameInfo.objects.filter(game__exact=game).order_by('-net_worth')[:]
    counter = 1
    # update ranking field
    for game_info in game_infos:
        game_info.ranking = counter
        game_info.save()
        counter += 1

    return game_infos
