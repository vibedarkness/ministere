from django.shortcuts import render
import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from main.EmailBackEnd import EmailBackEnd
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required


from main.models import *

# from main.forms import *



#========================================Login Logout Start=====================================


def LoginPage(request):
    return render(request,"main/loginSite.html")

def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user=EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type=="1":
                return redirect(reverse("admin_home"))
            elif user.user_type=="2":
                return redirect(reverse("staff_home"))
        else:
            messages.error(request,"Erreur sur l'email ou le mot de passe")
            return redirect(reverse("show_login"))


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")



@login_required(login_url='/')
def adminhome(request):
    client=Client.objects.all().count()
    facture=Invoice.objects.all().count()
    ba=BordereauAdministratif.objects.all().count()

    objets = Invoice.objects.all()

    total = 0

    for objet in objets:
        total += objet.total

    context={
        'client':client,
        'facture':facture,
        'argent':total,
        'ba':ba,
    }

    return render(request,'adminpage/index.html',context)



@login_required(login_url='/')
def staffhome(request):
    client=Client.objects.all().count()
    facture=Invoice.objects.all().count()
    ba=BordereauAdministratif.objects.all().count()

    objets = Invoice.objects.all()

    total = 0

    for objet in objets:
        total += objet.total

    context={
        'client':client,
        'facture':facture,
        'argent':total,
        'ba':ba,
    }

    return render(request,"staffpage/index.html",context)



@login_required(login_url='/')
def client_list(request):

    client = Client.objects.all()

    context = {
        'client': client,
    }

    return render(request,"staffpage/list_client.html", context)


