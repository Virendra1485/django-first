from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from . import models
from myapp import models as myapp_models


#middleware to check session for admin routes
def sessioncheckmyadmin_middleware(get_response):
	def middleware(request):
		if request.path=='/myadmin/' or request.path=='/myadmin/manageusers/' or request.path=='/myadmin/manageuserstatus/' or request.path=='/myadmin/addcategory/' or request.path=='/myadmin/addsubcategory/':
			if request.session['sunm']==None or request.session['srole']!="admin":
				response = redirect('/login/')
			else:
				response = get_response(request)
		else:
			response = get_response(request)		
		return response	
	return middleware


# Create your views here.

def adminhome(request):
 return render(request,"adminhome.html",{"sunm":request.session["sunm"]})

def manageusers(request):
 userDetails=myapp_models.Register.objects.filter(role='user')         
 return render(request,"manageusers.html",{"userDetails":userDetails,"sunm":request.session["sunm"]})

def manageuserstatus(request):
 regid=request.GET.get("regid")    
 s=request.GET.get("s")
 
 if s=="block":
  myapp_models.Register.objects.filter(regid=int(regid)).update(status=0)
 elif s=="verify":
  myapp_models.Register.objects.filter(regid=int(regid)).update(status=1)
 else:
  myapp_models.Register.objects.filter(regid=int(regid)).delete()        
 
 
 return redirect("/myadmin/manageusers/")


def addcategory(request):
 if request.method=="GET":
  return render(request,"addcategory.html",{"output":"","sunm":request.session["sunm"]})
 else:
  catnm=request.POST.get("catnm")
  caticon=request.FILES['caticon']
  fs = FileSystemStorage()
  filename = fs.save(caticon.name,caticon)
  p=models.Category(catnm=catnm,caticonname=filename)
  p.save()
  return render(request,"addcategory.html",{'output':'Category Added Successfully',"sunm":request.session["sunm"]})

def addsubcategory(request):
 clist=models.Category.objects.all()    
 if request.method=="GET":
  return render(request,"addsubcategory.html",{"clist":clist,"output":"","sunm":request.session["sunm"]})
 else:
  catnm=request.POST.get("catnm")
  subcatnm=request.POST.get("subcatnm")
  caticon=request.FILES['caticon']
  fs = FileSystemStorage()
  filename = fs.save(caticon.name,caticon)
  p=models.SubCategory(catnm=catnm,subcatnm=subcatnm,subcaticonname=filename)
  p.save()
  return render(request,"addsubcategory.html",{"clist":clist,"output":'Sub Category Added Successfully',"sunm":request.session["sunm"]})                       

def cpmyadmin(request):
  if request.method=="GET":
    return render(request,"cpmyadmin.html",{"sunm":request.session["sunm"],"output":""})
  else:
    opass=request.POST.get("opass")
    npass=request.POST.get("npass")
    cnpass=request.POST.get("cnpass")    
    res=myapp_models.Register.objects.filter(username=request.session["sunm"],password=opass).exists()
    if res:
      if npass==cnpass:
        myapp_models.Register.objects.filter(username=request.session["sunm"],password=opass).update(password=cnpass)
        return render(request,"cpmyadmin.html",{"sunm":request.session["sunm"],"output":"password changed successfully , please login again"})
      else:
        return render(request,"cpmyadmin.html",{"sunm":request.session["sunm"],"output":"New & Confirm new password mismatch , try again"})    
    else:  
      return render(request,"cpmyadmin.html",{"sunm":request.session["sunm"],"output":"Invalid old password , please try again"})






