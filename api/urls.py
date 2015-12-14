from django.conf.urls import *
from api.views import *
urlpatterns = [
	url(r'^echo',echo),
	url(r'^friend_list',friend_list),
	url(r'^talk_msg_list',talk_msg_list),
	url(r'^init_data',init_data),
	url(r'^register',register),
	url(r'^show_user',show_user),
	url(r'^talkmsg',talkmsg),
	url(r'^comment',comment),
	url(r'^praise',praise),
]
