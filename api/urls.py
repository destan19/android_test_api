from django.conf.urls import *
from api.views import *
urlpatterns = [
	url(r'^echo',echo),
	url(r'^blog',blog),
	url(r'^upload_test',upload_test),
	url(r'^friend_list',friend_list),
	url(r'^talk_msg_list',talk_msg_list),
	url(r'^init_data',init_data),
	url(r'^register',register),
	url(r'^show_user',show_user),
	url(r'^talkmsg',talkmsg),
	url(r'^comment',comment),
	url(r'^praise',praise),
	url(r'^upload_user_image',upload_user_image)
]
