from django.shortcuts import render
from django.http import HttpResponse

from django.template import loader,Context
from api.models import *
import json
import string
def echo(request):
        return HttpResponse("echo...");
# Create your views here.


def friend_list(request):
#	req_para=request.REQUEST.get("device_info")
#req_json=json.loads(req_para)
	total=0
	res_json={}

	f_list=[]
	for i in range(0,50):
		total=total+1
		friend={}
		friend['id']=i
		friend['name']="derry%d"%i
		friend['address']='GuangDong ShenZhen'
		friend['age']=26
		friend['email']='destan19@126.com'
		friend['company']='tencent'
		f_list.append(friend)
	res_json['total']=total
	res_json['list']=f_list;
	return HttpResponse(json.dumps(res_json))
	
	

def talk_msg_list(request):
	num=request.REQUEST.get("msg_num")
	total=0
	res_json={}

	msg_list=[]
	num2=string.atoi(num);
	if string.atoi(num) <=0 :
		num2=50
	for i in range(0,num2):
		total=total+1
		msg={}
		image_list=[]
		image1=""
		image2=""
		image3=""
		msg['id']=i
		msg['name']="derry%d"%i
		msg['locate']='guangzhou'
		msg['photo_url']="http://test.pychat.xyz:8000/images/%d/photo.png"%i

		for j in range(1,4):
			image="http://test.pychat.xyz:8000/images/%d/%d.png"%(i,j)
			image_list.append(image)
		msg['image_urls']=image_list

		msg['content']='I want to go shop,is there anyone follow  me?haha, just for test.....'
		msg_list.append(msg)
	res_json['total']=total
	res_json['list']=msg_list;
	return HttpResponse(json.dumps(res_json))

def init_data(request):
	print 'init data'
	for i in range(100,150):
		user=User()
		user.name="dxt_%d"%(i)
		user.address="sz_%d"%(i)
		user.email="dest%d@126.com"%(i)
		user.phone_num="13989973%d"%(i)
		user.save()
	return HttpResponse('ok')
	
def check_user_exist(username):
	try:
		user_id=User.objects.filter(name=username);
	except:
		return 0;
	if (any(user_id)):
		return 1;
	else:
		return 0;

		
def register(request):
	username=request.REQUEST.get("username")
	password=request.REQUEST.get("password")
	email=request.REQUEST.get("email")
	phone_num=request.REQUEST.get("phone_num")
	if username is None or password is None:
		return HttpResponse('error,username or password is requested.')
	if username == "" or password=="":
		return HttpResponse('username error.')
	
	user=User()
	if check_user_exist(username):
		return HttpResponse('user already exist.')
	user.name=username
	user.password = password
	if phone_num is not None:
		user.phone_num = phone_num
	if email is not None:
		user.email = email
	user.save()
	return HttpResponse('register success...')
	
def show_user(request):
	users=User.objects.all();
	t=loader.get_template('user_list.html')
	c=Context({
		'users':users,
			})
	return HttpResponse(t.render(c))
	
def talkmsg(request):
	username=request.REQUEST.get("username")
	if username is None:
		return HttpResponse('error,username is requested.')
	try:
		user_id=User.objects.filter(name=username);
	except:
		return HttpResponse('search error.')
	if (any(user_id)):
		msgs=TalkMsg.objects.all();
		t=loader.get_template('user_list.html')
		c=Context({
		'msgs':msgs,
			})
		return HttpResponse(t.render(c))
	else:
		return HttpResponse('user not exist.')
	
	