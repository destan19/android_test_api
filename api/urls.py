from django.conf.urls import *
from api.views import *
urlpatterns = patterns('',
	url(r'^echo',echo)
)
