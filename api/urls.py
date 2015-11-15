from django.conf.urls import *
from api.views import *
urlpatterns = patterns('',
	url(r'^echo',echo),
	url(r'^friend_list',friend_list),
	url(r'^talk_msg_list',talk_msg_list)
)
