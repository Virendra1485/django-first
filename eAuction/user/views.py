from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.conf import settings

from myadmin import models as myadmin_models
from . import models
media_url=settings.MEDIA_URL
import time

#middleware to check session for admin routes
def sessioncheckuser_middleware(get_response):
	def middleware(request):
		if request.path=='/user/' or request.path=='/user/addproduct/':
			if request.session['sunm']==None or request.session['srole']!="user":
				response = redirect('/login/')
			else:
				response = get_response(request)
		else:
			response = get_response(request)		
		return response	
	return middleware


# Create your views here.

def userhome(request):
 return render(request,"userhome.html",{"sunm":request.session["sunm"]})

def addproduct(request):
 clist=myadmin_models.Category.objects.all()
 if request.method=="GET":
  return render(request,"addproduct.html",{"output":"","clist":clist,"sunm":request.session["sunm"]}) 
 else:
  title=request.POST.get('title')
  category=request.POST.get('category')	
  subcategory=request.POST.get('subcategory')
  description=request.POST.get('description')
  bprice=request.POST.get('bprice')

  file1=request.FILES['file1']
  fs = FileSystemStorage()
  file1name = fs.save(file1.name,file1)

  if request.POST.get('file2')=="":
   file2name="logo.jpeg"
  else:
   file2=request.FILES['file2']
   fs = FileSystemStorage()
   file2name = fs.save(file2.name,file2)

  if request.POST.get('file3')=="":
   file3name="logo.jpeg"
  else:
   file3=request.FILES['file3']
   fs = FileSystemStorage()
   file3name = fs.save(file3.name,file3)

  if request.POST.get('file4')=="":
   file4name="logo.jpeg"
  else:
   file4=request.FILES['file4']
   fs = FileSystemStorage()
   file4name = fs.save(file4.name,file4)		

  p=models.Product(title=title,category=category,subcategory=subcategory,description=description,bprice=bprice,file1=file1name,file2=file2name,file3=file3name,file4=file4name,status=0,uid=request.session['sunm'],info=time.time())
  p.save()	 
  return render(request,"addproduct.html",{"output":"Product added successfully....","clist":clist,"sunm":request.session["sunm"]})	 


def fetchSubCategoryAJAX(request):
 cnm=request.GET.get("cnm")   
 sclist=myadmin_models.SubCategory.objects.filter(catnm=cnm) 
 sclist_options="<option>Select sub category</option>"
 for row in sclist:
     sclist_options+=("<option>"+row.subcatnm+"</option>")
 return HttpResponse(sclist_options)


def viewproductuser(request):
 paypalURL="https://www.sandbox.paypal.com/cgi-bin/webscr"
 paypalID="sb-pkvs75521974@business.example.com"
 #sb-azxwm5529177@personal.example.com
 plist=models.Product.objects.filter(uid=request.session["sunm"])
 return render(request,"viewproductuser.html",{"plist":plist,"sunm":request.session["sunm"],"paypalURL":paypalURL,"paypalID":paypalID})


def payment(request):
 pid=request.GET.get("pid")  
 uid=request.GET.get("uid")
 amount=request.GET.get("amount")
 info=time.asctime()

 p=models.Payment(pid=int(pid),uid=uid,amount=int(amount),info=info)
 p.save()

 models.Product.objects.filter(pid=int(pid)).update(status=1,info=time.time())

 return redirect("/user/success/")

def success(request):
 return render(request,"success.html",{"sunm":request.session["sunm"]})  

def cancel(request):
 return render(request,"cancel.html",{"sunm":request.session["sunm"]})

def bidproduct(request):
 plist=models.Product.objects.filter(~Q(uid=request.session["sunm"])) 
 return render(request,"bidproduct.html",{"sunm":request.session["sunm"],"plist":plist,"media_url":media_url}) 

def bidproductview(request):
  pid=int(request.GET.get("pid"))
  bprice=int(request.GET.get("bprice"))

  bidlist=models.Bidding.objects.filter(pid=pid)
  if len(bidlist)>0:
    bidDetails=models.Bidding.objects.filter(pid=pid)      
    cprice=bidDetails[len(bidDetails)-1].bidamount
  else:
    cprice=bprice  

  pDetails=models.Product.objects.filter(pid=pid)
  if (time.time()-float(pDetails[0].info))>172800:
    bstatus=False
  else:
    bstatus=True  
  return render(request,"bidproductview.html",{"sunm":request.session["sunm"],"bstatus":bstatus,"pid":pid,"bprice":bprice,"cprice":cprice})   

def mybid(request):
  pid=request.POST.get("pid")
  bprice=request.POST.get("bprice")
  cprice=request.POST.get("cprice")
  bidprice=request.POST.get("bidprice")  

  p=models.Bidding(pid=pid,uid=request.session["sunm"],bidamount=bidprice,info=time.asctime())

  p.save()

  return redirect("/user/bidproductview/?pid="+str(pid)+"&bprice="+str(bprice))


def bidhistory(request):
  pid=int(request.GET.get("pid"))
  bidDetails=models.Bidding.objects.filter(pid=pid) 
  return render(request,"bidhistory.html",{"sunm":request.session["sunm"],"bidDetails":bidDetails})