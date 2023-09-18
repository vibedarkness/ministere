from django.shortcuts import render ,get_object_or_404, redirect, reverse
from main.models import *

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from main.forms import *
from django.contrib.auth.decorators import login_required


@login_required(login_url='/')
def add_staff(request):
    return render(request,"adminpage/add_staff.html")
@login_required(login_url='/')
def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        form=AddStaffForm(request.POST,request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            address=form.cleaned_data["address"]
            phone_number=form.cleaned_data["phone_number"]
            sexe=form.cleaned_data["sexe"]

            try:
                user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
                user.staff.address=address
                user.staff.phone_number=phone_number
                user.staff.sexe=sexe
                user.save()
                messages.success(request,"Staff Ajouter avec Success")
                return HttpResponseRedirect(reverse("add_staff"))
            except:
                messages.error(request,"Echec de l'ajout")
                return HttpResponseRedirect(reverse("add_staff"))
        else:
            form=AddStaffForm(request.POST)
            return render(request, "adminpage/add_staff.html", {"form": form})


@login_required(login_url='/')
def list_staff(request):

    staff = CustomUser.objects.filter(user_type=2)

    context = {
        'staff': staff,
    }

    return render(request,"adminpage/list_staff.html", context)