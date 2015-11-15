from django.shortcuts import render
from django.http import HttpResponse
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
	