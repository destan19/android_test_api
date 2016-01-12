from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import loader,Context
from api.models import *
from django import forms
import json
import string
import os
import urllib, urllib2
import re
import cookielib
import time
import xml.dom.minidom
import math
import csv
deviceId = 'e000000000000000'

DEBUG = True
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
		#username=request.POST.get('name')
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
	for i in range(100,300):
		t=TalkMsg()
		derry=User.objects.filter(name='derry')[0]
		if derry is None:
			print 'not find derry'
			derry=User.objects.all()[0]
		t.address="chang sha"
		t.device="iphone 6s"	
		t.user=derry
		t.img_url="http://test.pychat.xyz:8000/api/static/%d.jpg"%(i)
		t.content="The toilet paper rolls were delivered to the city hall by Inuyamas designated supplier earlier this December%d"%(i)
		t.save()
	return HttpResponse('init data ok')
	
def check_user_exist(username):
	try:
		user_id=User.objects.filter(name=username);
	except:
		return 0;
	if (any(user_id)):
		return 1;
	else:
		return 0;
def wx_login(request):
	res_json={}
	status_json= {}
	username=request.GET.get("username")
	password=request.GET.get("password")
	if username is None or password is None:
		status_json['code']=4001	
		status_json['msg']='username or password is none'
		return HttpResponse(json.dumps(res_json))

	users = User.objects.filter(name=username)
	if any(users):
		user=users[0]
		print user.password
		if user.password == password:
			status_json['code']=2000
			status_json['msg']='success'
		else:	
			status_json['code']=4002
			status_json['msg']='username or password error.'
	else:
		status_json['code']=4001
		status_json['msg']='user is not exist'
	
	res_json['status']=status_json
	print res_json
	return HttpResponse(json.dumps(res_json))
		
def register(request):
	status_obj={}
	status_obj['code']=2000
	status_obj['msg']='register success'
	username=request.GET.get("username")
	password=request.GET.get("password")
	email=request.GET.get("email")
	phone_num=request.GET.get("phone_num")
	if username is None or password is None:
		status_obj['code']=4000
		status_obj['msg']='username or password is none'
		return HttpResponse(json.dumps(status_obj))
	
	user=User()
	if check_user_exist(username):
		status_obj['code']=4001
		status_obj['msg']='username is already exist'
		return HttpResponse(json.dumps(status_obj))
	user.name=username
	user.password = password
	if phone_num is not None:
		user.phone_num = phone_num
	if email is not None:
		user.email = email
	user.save()
	return HttpResponse(json.dumps(status_obj))
	
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
	
def getUUID():
	
	url = 'https://login.weixin.qq.com/jslogin'
	params = {
		'appid': 'wx782c26e4c19acffb',
		'fun': 'new',
		'lang': 'zh_CN',
		'_': int(time.time()),
	}

	request = urllib2.Request(url = url, data = urllib.urlencode(params))
	response = urllib2.urlopen(request)
	data = response.read()

	# print data

	# window.QRLogin.code = 200; window.QRLogin.uuid = "oZwt_bFfRg==";
	regx = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)"'
	pm = re.search(regx, data)

	code = pm.group(1)
	uuid = pm.group(2)

	if code == '200':
		return uuid

	return ""	

def showQRImage(uuid):
	if len(uuid)==0:
		return;
	global tip
	url = 'https://login.weixin.qq.com/qrcode/' + uuid
	params = {
		't': 'webwx',
		'_': int(time.time()),
	}

	request = urllib2.Request(url = url, data = urllib.urlencode(params))
	response = urllib2.urlopen(request)

	tip = 1
	QRImagePath="api/static/img/%s.jpg"%(uuid)
	f = open(QRImagePath, 'wb')
	f.write(response.read())
	f.close()

def login(base_uri,redirect_uri):
	#global skey, wxsid, wxuin, pass_ticket, BaseRequest
	resp_data={}
	request = urllib2.Request(url = redirect_uri)
	response = urllib2.urlopen(request)
	data = response.read()

	print data

	'''
		<error>
			<ret>0</ret>
			<message>OK</message>
			<skey>xxx</skey>
			<wxsid>xxx</wxsid>
			<wxuin>xxx</wxuin>
			<pass_ticket>xxx</pass_ticket>
			<isgrayscale>1</isgrayscale>
		</error>
		<error><ret>0</ret><message>OK</message>
<skey>@crypt_8940936b_58307407faa32a423b87c161640d6b81</skey><wxsid>sEMWXrqKLdroEHFY</wxsid>
<wxuin>145618555</wxuin><pass_ticket>m2HZLGbXnyJmYunUeIaYmTAky6utoK29jx0a4NhAIZ4%3D</pass_ticket><isgrayscale>1</isgrayscale></error>
	'''

	doc = xml.dom.minidom.parseString(data)
	root = doc.documentElement

	for node in root.childNodes:
		if node.nodeName == 'skey':
			skey = node.childNodes[0].data
		elif node.nodeName == 'wxsid':
			wxsid = node.childNodes[0].data
		elif node.nodeName == 'wxuin':
			wxuin = node.childNodes[0].data
		elif node.nodeName == 'pass_ticket':
			pass_ticket = node.childNodes[0].data

	BaseRequest = {
		'Uin': int(wxuin),
		'Sid': wxsid,
		'Skey': skey,
		'DeviceID': deviceId,
	}
	resp_data['skey'] = skey
	resp_data['wxsid'] = wxsid
	resp_data['wxuin'] = wxuin
	resp_data['pass_ticket'] = pass_ticket
	resp_data['BaseRequest'] = BaseRequest
	print '1pass_ticket=%s,len=%d'%(pass_ticket,len(pass_ticket))
	return resp_data	

def webwxinit(base_uri,wx_data):
	print '2pass_ticket=%s,len=%d'%(wx_data['pass_ticket'],len(wx_data['pass_ticket']))

	url = base_uri + '/webwxinit?pass_ticket=%s&skey=%s&r=%s' % (wx_data['pass_ticket'], wx_data['skey'], int(time.time()))
	params = {
		'BaseRequest': wx_data['BaseRequest']
	}
	print 'request=',wx_data['BaseRequest']
	request = urllib2.Request(url = url, data = json.dumps(params))
	request.add_header('ContentType', 'application/json; charset=UTF-8')
	response = urllib2.urlopen(request)
	data = response.read()

	if DEBUG == True:
		f = open('./webwxinit.json', 'wb')
		f.write(data)
		f.close()

	# print data
	global ContactList, My
	dic = json.loads(data)
	ContactList = dic['ContactList']
	My = dic['User']

	ErrMsg = dic['BaseResponse']['ErrMsg']
	if len(ErrMsg) > 0:
		print ErrMsg

	Ret = dic['BaseResponse']['Ret']
	if Ret != 0:
		print 'web init fail...'
		return False
	print 'web init ok...'	
	return True
def webwxgetcontact(base_uri,wx_data):
	print '3pass_ticket=%s,len=%d'%(wx_data['pass_ticket'],len(wx_data['pass_ticket']))
	url = base_uri + '/webwxgetcontact?pass_ticket=%s&skey=%s&r=%s' % (wx_data['pass_ticket'], wx_data['skey'], int(time.time()))

	request = urllib2.Request(url = url)
	request.add_header('ContentType', 'application/json; charset=UTF-8')
	response = urllib2.urlopen(request)
	data = response.read()
	print 'url=',url
	if DEBUG == True:
		f = open('./webwxgetcontact.json', 'wb')
		f.write(data)
		f.close()

	# print data

	dic = json.loads(data)
	MemberList = dic['MemberList']
	print 'members=',MemberList
	SpecialUsers = ['newsapp', 'fmessage', 'filehelper', 'weibo', 'qqmail', 'fmessage', 'tmessage', 'qmessage', 'qqsync', 'floatbottle', 'lbsapp', 'shakeapp', 'medianote', 'qqfriend', 'readerapp', 'blogapp', 'facebookapp', 'masssendapp', 'meishiapp', 'feedsapp', 'voip', 'blogappweixin', 'weixin', 'brandsessionholder', 'weixinreminder', 'wxid_novlwrv3lqwv11', 'gh_22b87fa7cb3c', 'officialaccounts', 'notification_messages', 'wxid_novlwrv3lqwv11', 'gh_22b87fa7cb3c', 'wxitil', 'userexperience_alarm', 'notification_messages']
	for i in xrange(len(MemberList) - 1, -1, -1):
		Member = MemberList[i]
		if Member['VerifyFlag'] & 8 != 0: 
			MemberList.remove(Member)
		elif Member['UserName'] in SpecialUsers:
			MemberList.remove(Member)
		elif Member['UserName'].find('@@') != -1:
			MemberList.remove(Member)
		elif Member['UserName'] == My['UserName']: 
			MemberList.remove(Member)

	return MemberList,data

def createChatroom(base_uri,wx_data,UserNames):
	MemberList = []
	for UserName in UserNames:
		MemberList.append({'UserName': UserName})


	url = base_uri + '/webwxcreatechatroom?pass_ticket=%s&r=%s' % (wx_data['pass_ticket'], int(time.time()))
	params = {
		'BaseRequest': wx_data['BaseRequest'],
		'MemberCount': len(MemberList),
		'MemberList': MemberList,
		'Topic': '',
	}

	request = urllib2.Request(url = url, data = json.dumps(params))
	request.add_header('ContentType', 'application/json; charset=UTF-8')
	response = urllib2.urlopen(request)
	data = response.read()

	# print data
	print 'data=',data
	dic = json.loads(data)
	ChatRoomName = dic['ChatRoomName']
	MemberList = dic['MemberList']
	DeletedList = []
	for Member in MemberList:
		if Member['MemberStatus'] == 4: 
			DeletedList.append(Member['UserName'])

	ErrMsg = dic['BaseResponse']['ErrMsg']
	if len(ErrMsg) > 0:
		print ErrMsg

	return (ChatRoomName, DeletedList)

def deleteMember(base_uri,wx_data,ChatRoomName, UserNames):
	url = base_uri + '/webwxupdatechatroom?fun=delmember&pass_ticket=%s' % (wx_data['pass_ticket'])
	params = {
		'BaseRequest': wx_data['BaseRequest'],
		'ChatRoomName': ChatRoomName,
		'DelMemberList': ','.join(UserNames),
	}

	request = urllib2.Request(url = url, data = json.dumps(params))
	request.add_header('ContentType', 'application/json; charset=UTF-8')
	response = urllib2.urlopen(request)
	data = response.read()

	# print data

	dic = json.loads(data)
	ErrMsg = dic['BaseResponse']['ErrMsg']
	if len(ErrMsg) > 0:
		print ErrMsg

	Ret = dic['BaseResponse']['Ret']
	if Ret != 0:
		return False
		
	return True

def addMember(base_uri,wx_data,ChatRoomName, UserNames):
	url = base_uri + '/webwxupdatechatroom?fun=addmember&pass_ticket=%s' % (wx_data['pass_ticket'])
	params = {
		'BaseRequest': wx_data['BaseRequest'],
		'ChatRoomName': ChatRoomName,
		'AddMemberList': ','.join(UserNames),
	}

	request = urllib2.Request(url = url, data = json.dumps(params))
	request.add_header('ContentType', 'application/json; charset=UTF-8')
	response = urllib2.urlopen(request)
	data = response.read()

	# print data

	dic = json.loads(data)
	MemberList = dic['MemberList']
	DeletedList = []
	for Member in MemberList:
		if Member['MemberStatus'] == 4: 
			DeletedList.append(Member['UserName'])

	ErrMsg = dic['BaseResponse']['ErrMsg']
	if len(ErrMsg) > 0:
		print ErrMsg

	return DeletedList
def get_deleted_friends(base_uri,wx_data,MemberList):
	MAX_GROUP_NUM=100
	ChatRoomName = ''
	result = []
	MemberCount=len(MemberList)
	for i in xrange(0, int(math.ceil(MemberCount / float(MAX_GROUP_NUM)))):
		UserNames = []
		NickNames = []
		DeletedList = ''
		for j in xrange(0, MAX_GROUP_NUM):
			if i * MAX_GROUP_NUM + j >= MemberCount:
				break

			Member = MemberList[i * MAX_GROUP_NUM + j]
			UserNames.append(Member['UserName'])
			NickNames.append(Member['NickName'].encode('utf-8'))
                        
		print 'num%s...' % (i + 1)
		print ', '.join(NickNames)
		if ChatRoomName == '':
			print 'create chat room name'
			(ChatRoomName, DeletedList) = createChatroom(base_uri,wx_data,UserNames)
		else:
			print 'room name=',ChatRoomName
			DeletedList = addMember(base_uri,wx_data,ChatRoomName, UserNames)

		DeletedCount = len(DeletedList)
		if DeletedCount > 0:
			result += DeletedList

		print 'find %s friends that deleted you' % DeletedCount

		deleteMember(base_uri,wx_data,ChatRoomName, UserNames)

	resultNames = []
	for Member in MemberList:
		if Member['UserName'] in result:
			NickName = Member['NickName']
			if Member['RemarkName'] != '':
				NickName += '(%s)' % Member['RemarkName']
			resultNames.append(NickName.encode('utf-8'))

	print '---------- list ----------'
	print '\n'.join(resultNames)
	print '-----------------------------------'
	return resultNames
def save_csv_file(MemberList):
	with open('memberlist.csv', 'wb',encoding='utf-8') as csvfile:
		spamwriter = csv.writer(csvfile,dialect='excel')
		for Member in MemberList:
			spamwriter.writerow([Member['UserName'],Member['NickName'].encode('utf-8')])
			#NickNames.append(Member['NickName'].encode('utf-8'))
def check_login_status(request):
	MemberList=[]
	json_data={}
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
	urllib2.install_opener(opener)
	login_resp_data={}
	tip = 1
	uuid = request.GET.get("uuid")
	if uuid is None or len(uuid) == 0:
		return HttpResponse('require uuid')
	url = 'https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?tip=%s&uuid=%s&_=%s' % (tip, uuid, int(time.time()))

	request = urllib2.Request(url = url)
	response = urllib2.urlopen(request)
	data = response.read()
	
	# print data

	# window.code=500;
	regx = r'window.code=(\d+);'
	pm = re.search(regx, data)

	code = pm.group(1)

	if code == '201': 
		print 'scan success'
	elif code == '200': 
		regx = r'window.redirect_uri="(\S+?)";'
		pm = re.search(regx, data)
		redirect_uri = pm.group(1) + '&fun=new'
		base_uri = redirect_uri[:redirect_uri.rfind('/')]
		login_resp_data=wx_login(base_uri,redirect_uri)
		webwxinit(base_uri,login_resp_data)
		MemberList,json_data = webwxgetcontact(base_uri,login_resp_data)
		MemberCount = len(MemberList)
		dlist=[]
		#dlist=get_deleted_friends(base_uri,login_resp_data,MemberList)
		#print dlist
		return HttpResponse(json_data)
		t=loader.get_template('wx_show.html')
		c=Context({
			'members':MemberList,
			})
		return HttpResponse(t.render(c))
	elif code == '408': 
		pass
	# elif code == '400' or code == '500':
	return HttpResponse(code)

	
def wechat_delete_friend(request):
	uuid = getUUID()
	showQRImage(uuid)
	t=loader.get_template('show_image.html')
	users=User.objects.all()
	url="http://192.168.17.134/static/img/%s.jpg"%(uuid)
	data={}
	data['img_url']=url
	data['uuid']=uuid
	c=Context({
		'data':data,
			})
	return HttpResponse(t.render(c))
