from django.shortcuts import render,redirect
from django.conf import settings
from django.http import HttpResponse

from . import encryption_api
from . import decryption_api
from . import sendEmail
from . import smsapi

from . import models
from myadmin import models as myadmin_models
import time

media_url=settings.MEDIA_URL


#middleware to check session for mainapp routes
def sessioncheck_middleware(get_response):
	def middleware(request):
		if request.path=='' or request.path=='/home/' or request.path=='/about/' or request.path=='/contact/' or request.path=='/login/' or request.path=='/service/' or request.path=='/register/':
			request.session['sunm']=None
			request.session['srole']=None
			
			response = get_response(request)
				
		else:
			response = get_response(request)		
		return response	
	return middleware

	

def home(request):
	clist=myadmin_models.Category.objects.all()	
	return render(request,"home.html",{"clist":clist,"media_url":media_url})

def viewsubcategory(request):
	catnm=request.GET.get("catnm")
	clist=myadmin_models.Category.objects.all()
	sclist=myadmin_models.SubCategory.objects.filter(catnm=catnm)
	return render(request,"viewsubcategory.html",{"catnm":catnm,"clist":clist,"sclist":sclist,"media_url":media_url})

def checkEmailAvaibility(request):
	v=request.GET.get("v")
	res=models.Register.objects.filter(username__startswith=v).exists()
	if res:
		msg="EmailId already exists , please choose new"
	else:
		msg="EmailId available"		
	return HttpResponse(msg)

def about(request):
	return render(request,"about.html",{})

def contact(request):
	return render(request,"contact.html",{})

def service(request):
	return render(request,"service.html",{})

def register(request):
	if request.method=="GET":
		return render(request,"register.html",{"output":""})
	else:
		name=request.POST.get("name")
		username=request.POST.get("username")
		password=request.POST.get("password")
		mobile=request.POST.get("mobile")
		address=request.POST.get("address")
		city=request.POST.get("city")
		gender=request.POST.get("gender")
		info=time.asctime()

		#To send verification link via email
		sendEmail.mymail(username,password)

		#To send SMS
		smsapi.sendSMS(mobile)	

		p=models.Register(name=name,username=username,password=password,mobile=mobile,address=address,city=city,gender=gender,role="user",status=0,info=info)
		p.save()

		return render(request,"register.html",{"output":"User registered successfully...."})		

def verifyuser(request):
	email=request.GET.get("email")
	models.Register.objects.filter(username=email).update(status=1)
	return redirect("/login/")

def login(request):
	cunm=""
	cpass=""
	if request.COOKIES.get("cunm")!=None:
		cunm=request.COOKIES.get("cunm")
		cencpassword=request.COOKIES.get("cpass")
		l=list(cencpassword)
		l.pop(0)
		l.pop(0)
		l.pop(len(l)-1)
		s=""
		for x in l:
			s+=x
		cencpassword_byte=bytes(s,'utf-8')	
		cpass=decryption_api.decrypt_message(cencpassword_byte)

	if request.method=="GET":
		return render(request,"login.html",{"output":"","cunm":cunm,"cpass":cpass})
	else:
		username=request.POST.get("username")
		password=request.POST.get("password")
		userDetails=models.Register.objects.filter(username=username,password=password,status=1)
		
		if len(userDetails)>0:

			# To store details in session
			request.session["sunm"]=userDetails[0].username			
			request.session["srole"]=userDetails[0].role

			if userDetails[0].role=="admin":
				response=redirect("/myadmin/")
			else:
				response=redirect("/user/")

			# To store details in cookies
			if request.POST.get("chk")=="remember":
				encrypted_message=encryption_api.encrypt_message(userDetails[0].password)
				response.set_cookie("cunm",userDetails[0].username,3600*24)
				response.set_cookie("cpass",encrypted_message,3600*24) 
			return response
		else:
			return render(request,"login.html",{"output":"Invalid user , please check authentication...","cunm":cunm,"cpass":cpass})	 		
