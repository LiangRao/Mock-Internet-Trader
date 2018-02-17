from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

import MIT.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^sign-in$', auth_views.login, {'template_name':'signin.html'}, name='sign_in'),
    url(r'^sign-out$', auth_views.logout, {'next_page': '/'}, name='sign_out'),
    url(r'^register$', MIT.views.register, name='register'),
    url(r'^auto_email$', MIT.views.auto_email),
    url(r'^overview/(?P<game_id>\d+)$', MIT.views.game_overview, name='game_overview'),
    url(r'^stock/(?P<game_id>\d+)$$', MIT.views.stock, name='stock'),
    url(r'^join-game/(?P<game_id>\d+)$', MIT.views.join_game, name='join_game'),
    url(r'^leave-game/(?P<game_id>\d+)$', MIT.views.leave_game, name='leave_game'),
    url(r'^create-game$', MIT.views.create_game, name='create_game'),
    url(r'^find-game$', MIT.views.find_game, name='find_game'),
    url(r'^search-game$', MIT.views.search_game, name='search_game'),
    url(r'^my-game-list$', MIT.views.my_game_list, name='my_game_list'),
    url(r'^get-index-info/(?P<index_name>[a-zA-Z0-9_@\+\-]+)$', MIT.views.get_index_info, name='get_index_info'),
    url(r'^get-share-info/(?P<game_id>\d+)/(?P<player_id>\d+)$', MIT.views.get_share_info, name='get_share_info'),
    url(r'^get-join-info/(?P<game_id>\d+)$', MIT.views.get_join_info, name='get_join_info'),
    url(r'^buy-stock/(?P<game_id>\d+)$', MIT.views.buy_stock, name='buy_stock'),
    url(r'^sell-stock/(?P<game_id>\d+)$', MIT.views.sell_stock, name='sell_stock'),
    url(r'^ranking/(?P<game_id>\d+)$', MIT.views.ranking, name='ranking'),
    url(r'^portfolio/(?P<game_id>\d+)/(?P<player_id>\d+)$', MIT.views.portfolio, name='portfolio'),
    url(r'^confirm_email/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)/$', MIT.views.confirm_email, name='confirm_email'),

    url(r'^password_reset$', auth_views.password_reset, {'template_name':'password_reset.html',
        'from_email':'lrao@andrew.cmu.edu','post_reset_redirect':'/password_reset/done'},name='password_reset'),
    url(r'^password_reset/done$', auth_views.password_reset_done, {'template_name':'password_reset_done.html'}, name='password_reset_done'),
    url(r'^password_reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm,
        {'template_name':'password_reset_confirm.html', 'post_reset_redirect':'/complete'},
        name='password_reset_confirm'),
    url(r'^complete$', auth_views.password_reset_complete, {'template_name':'password_reset_complete.html'}, name='reset_complete'),
]
