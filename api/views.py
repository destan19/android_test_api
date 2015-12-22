from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import loader,Context
from api.models import *
from django import forms
import json
import string
def echo(request):
        return HttpResponse("echo...");
		
def handle_uploaded_file(p,f):
    destination = open('name.jpg', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()		
# Create your views here.
def upload_test(request):
	if request.method == 'POST':
		print request.POST
		handle_uploaded_file(request.POST,request.FILES['file'])
		return HttpResponse("ok")
	else:
		form = UploadFileForm()
	return render(request,'upload_test.html', {'form': form})	
'''
	func:upload user image 
	desc:
	method:post
	para:
		username
		image
	file:
		image file
'''
def upload_user_image(request):
	
	if request.method == 'POST':
		print '111111111'
		#username=request.POST.get('name')
		print '2222222222'
		if username is None:
			print 'username is request'
			return HttpResponse("require username")
		print 'username=',username
		users=User.objects.filter(name=username)
		if not any(users):
			print 'username not exist'
			return HttpResponse('username is not exist')
		fp = open('%s/image.jpg'%(username), 'wb+')
		for chunk in request.FILE['file'].chunks():
			fp.write(chunk)
			fp.close()		
		print '33333333'
		return HttpResponse("ok")
	else:
		print 'get'
		return render(request,'upload_test.html')	
	
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
	username=request.GET.get("username")
	users=User.objects.all();
	t=loader.get_template('user_list.html')
	c=Context({
		'users':users,
			})
	return HttpResponse(t.render(c))
'''
data_obj['id']=msg.id
				data_obj['username']=msg.name
				data_obj['email']=msg.email
				data_obj['address']=msg.address
				data_obj['phone_num']=msg.phone_num
			'''

'''
	http://192.168.17.134/api/talkmsg?username=derry&json=1&start=1&end=100
	param:
		start
		username
		end
'''
def respTalkmsgJson(request):
	msg_json={}
	status_obj={}
	data_obj={}
	status_obj['code']=20000
	status_obj['msg']='success'
	username=request.GET.get("username")
	start=request.GET.get("start")
	end=request.GET.get("end")

	print 'resp talk msg'
	if username is None:
		status_obj['code']=40000
		status_obj['msg']='username is none'
		msg_json['status']=status_obj
	else:
		users=User.objects.filter(name=username)
		
		if not any(users):
			status_obj['code']=40001
			status_obj['msg']='username is not exist.'
			msg_json['status']=status_obj
		else:
			user=users[0]
			data_obj['total']=user.talkmsg_set.count()
			if start is None:
				start=0
			if end is None:
				msgs=user.talkmsg_set.all()[start:]
			else:
				msgs=user.talkmsg_set.all()[start:end]
			data_obj['count']=len(msgs)
			msg_arr=[]
			for msg in msgs:
				msg_obj={}
				msg_obj['id']=msg.id
				msg_obj['img_url']=msg.img_url
				msg_obj['content']=msg.content
				msg_obj['address']=msg.address
				msg_obj['device']=msg.device
				msg_arr.append(msg_obj)
			data_obj['list']=msg_arr
			msg_json['status']=status_obj
			msg_json['data']=data_obj	
	return HttpResponse(json.dumps(msg_json))
	
def talkmsg(request):
	msgs=[]
	comments={}
	praises={}
	users=[]
	username=request.GET.get("username")
	json_flag = request.GET.get("json")
	if json_flag is not None:
		return respTalkmsgJson(request)
		
	if username is None:
		users=User.objects.all()
	else:
		try:
			users=User.objects.filter(name=username);
		except:
			return HttpResponse('search error.')
	print users
	if (any(users)):
		for i in range(0,len(users)):
			msgs.extend(users[i].talkmsg_set.all())
		t=loader.get_template('talkmsg_list.html')
		c=Context({
		'msgs':msgs,
			})
		return HttpResponse(t.render(c))
	else:
		return HttpResponse('user not exist.')
	
def praise(request):
	tid=request.GET.get("id")
	if tid is None:
		return HttpResponse('id is None')
	msg=TalkMsg.objects.filter(id=tid)[0];
	if msg is None:
		return HttpResponse('talk msg is None')
	praises = msg.praise_set.all()
	print praises
	
	if (any(praises)):
		t=loader.get_template('praise_list.html')
		c=Context({
		'praises':praises,
			})
		return HttpResponse(t.render(c))
	return HttpResponse('ok')
	
def comment(request):
	tid=request.GET.get("id")
	if tid is None:
		return HttpResponse('id is None')
	msg=TalkMsg.objects.filter(id=tid)[0];
	if msg is None:
		return HttpResponse('talk msg is None')
	comments = msg.comment_set.all()
	print comments

	if (any(comments)):
		t=loader.get_template('comment_list.html')
		c=Context({
		'comments':comments,
			})
		return HttpResponse(t.render(c))
	return HttpResponse('ok')
	
def blog(request):
	if request.method=='POST':
		print 'post=',request.POST
		form =BlogForm(request.POST)
		if form.is_valid():
			return HttpResponse('hello')
	else:
		form=BlogForm()
	for field in form:
		'label=',field.label_tag
	#return render_to_response('blog.html',{'form':form})
	return render(request,'blog.html',{'form':form})
