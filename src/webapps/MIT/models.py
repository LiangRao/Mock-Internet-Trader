# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    user = models.OneToOneField(User)
    def __unicode__(self):
        return self.user.username

# once create, never change
class Game(models.Model):
    # when player create a game, he does not automatically join in
    # one player can create multiply games
    creator = models.ForeignKey(Player, default=None)
    name = models.CharField(max_length=420)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.CharField(max_length=420, default=' ', blank=True)
    starting_balance = models.FloatField()
    short = models.BooleanField(default=False)
    stop = models.BooleanField(default=False)
    limit = models.BooleanField(default=False)
    # record number of players in this game right now
    counter = models.IntegerField(default=0, blank=True)

    def __unicode__(self):
        return self.name

    def get_creator(self):
        return self.creator

    def get_playernumber(self):
        return self.counter

# store player's info
class GameInfo(models.Model):
    # must-have attributes
    remaining_balance = models.FloatField(default=0.0, blank=True)
    net_worth = models.FloatField(default=0.0, blank=True)
    # use to calculate today's gain, yesterday_net_worth is updated every day
    yesterday_net_worth = models.FloatField(default=0.0, blank=True)
    # how to calculate: net_worth - balance
    overall_gains = models.FloatField(default=0.0, blank=True)
    overall_return = models.FloatField(default=0.0, blank=True)

    short_reserve = models.FloatField(default=0.0, blank=True)
    # current ranking within this game
    ranking = models.IntegerField(default=1, blank=True)
    # belongs to which player
    player = models.ForeignKey(Player, default=None)
    # which game the player is currently in
    game = models.ForeignKey(Game, default=None)

    def __unicode__(self):
        return self.player.id + "in game: " + self.game.name

    def get_name(self):
        return self.player

    def get_player_id(self):
        return self.player.id

class Transaction(models.Model):
    stock_name = models.CharField(max_length=50)
    order_time = models.DateTimeField(auto_now_add=True)
    # TODO: need to fix when support stop/limit
    transaction_time = models.DateTimeField(null=True, default=None)
    # possible value:BUY/SELL/SHORT/COVER/PENDING
    transaction_type = models.CharField(max_length=20, default="INVALID")
    # trade share amount
    shares = models.IntegerField(default=0)
    # trade price
    price = models.FloatField(default=0.0)
    # the creator of the transaction
    creator = models.ForeignKey(Player)
    # which game the transaction belongs to
    game = models.ForeignKey(Game)

    def get_current_price(self):
        return Stock.objects.get(stock_name__exact=self.stock_name).current_price

class StockInfo(models.Model):
    stock_name = models.CharField(max_length=50)
    # possible value: BUY/SELL/SHORT/COVER
    stock_type = models.CharField(max_length=20, default="INVALID")
    # total share amount owned by this player
    shares = models.IntegerField(default=0)
    # total value of this specific stock, you can transaction multiple times
    # the money you have spent on when buying this stock
    total_value = models.FloatField(default=0.0)
    # player + game uniquely define a stock
    player = models.ForeignKey(Player)
    game = models.ForeignKey(Game)

    def __unicode__(self):
        return self.stock_name + " " + self.stock_type + " " + str(self.shares) + " " + str(self.total_value)

    def get_current_price(self):
        return Stock.objects.get(stock_name__exact=self.stock_name).current_price

    def get_current_value(self):
        return round(self.get_current_price()*self.shares, 2)

    def get_gain(self):
        gain = round(self.get_current_price()*self.shares-self.total_value, 2)
        if self.stock_type == "SHORT":
            return gain * (-1.0)
        else:
            return gain

class Stock(models.Model):
    stock_name = models.CharField(max_length=50, primary_key=True)
    current_price = models.FloatField(default=0.0)

    def __unicode__(self):
        return self.stock_name + " :" + self.current_price
