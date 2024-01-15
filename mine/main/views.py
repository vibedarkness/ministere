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
from django.db.models import Count,Sum,F
from django.db.models.functions import TruncYear,TruncMonth

from decimal import Decimal
from main.models import *
import logging
import locale

# Définir la localisation en français
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

logger = logging.getLogger(__name__)

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
    client = Client.objects.all().count()
    facture = Invoice.objects.all().count()
    ba = BordereauAdministratif.objects.all().count()
    clients_with_invoice_count = Client.objects.annotate(num_invoices=Count('invoice')).order_by('-num_invoices')

    # Graphique clients facturés
    labels = [client.prenom for client in clients_with_invoice_count]
    data = [client.num_invoices for client in clients_with_invoice_count]

    # Graphique par année
    invoices_by_year = (
    Invoice.objects
    .exclude(date_creation__isnull=True)  # Exclure les factures sans date de création
    .annotate(year=TruncYear('date_creation'))
    .values('year')
    .annotate(num_invoices=Count('id'))
    .order_by('year')
)

    labelyear = [invoice['year'].year if 'year' in invoice else None for invoice in invoices_by_year]
    datayear = [invoice['num_invoices'] for invoice in invoices_by_year]
    # Graphique par mois
    invoices_by_month = (
        Invoice.objects.annotate(month=TruncMonth('date_creation'))
        .values('month')
        .annotate(num_invoices=Count('id'))
        .order_by('month')
    )

    # Formater le nom du mois en français
    labelmonth = [invoice['month'].strftime('%B %Y') for invoice in invoices_by_month]
    datamonth = [invoice['num_invoices'] for invoice in invoices_by_month]
    # Rétablir la localisation par défaut
    locale.setlocale(locale.LC_TIME, '')
    

    # Graphique total par mois
    # prices_by_month = (
    #     Article.objects.annotate(month=TruncMonth('invoice__date_creation'))
    #     .values('month')
    #     .annotate(total_prices=Sum(F('unit_price') * F('quantity')))
    #     .order_by('month')
    # )

    # labelmonthprices = [price['month'].strftime('%B %Y') for price in prices_by_month]
    # datamonthprices = [Decimal(price['total_prices'] or 0) for price in prices_by_month]

    total = 0

    for objet in Invoice.objects.all():
        total += objet.total

    context = {
        'client': client,
        'facture': facture,
        'argent': total,
        'ba': ba,

        'clients': clients_with_invoice_count,
        'labels': labels,
        'data': data,

        'labelyear': labelyear,
        'datayear': datayear,

        'labelmonth': labelmonth,
        'datamonth': datamonth,

        # 'labelmonthtotal': labelmonthprices,
        # 'datamonthtotal': datamonthprices,

        
    }

    return render(request, 'adminpage/index.html', context)



@login_required(login_url='/')
def staffhome(request):
    client = Client.objects.all().count()
    facture = Invoice.objects.all().count()
    ba = BordereauAdministratif.objects.all().count()
    clients_with_invoice_count = Client.objects.annotate(num_invoices=Count('invoice')).order_by('-num_invoices')

    # Graphique clients facturés
    labels = [client.prenom for client in clients_with_invoice_count]
    data = [client.num_invoices for client in clients_with_invoice_count]

    # Graphique par année
    invoices_by_year = (
    Invoice.objects
    .exclude(date_creation__isnull=True)  # Exclure les factures sans date de création
    .annotate(year=TruncYear('date_creation'))
    .values('year')
    .annotate(num_invoices=Count('id'))
    .order_by('year')
)

    labelyear = [invoice['year'].year if 'year' in invoice else None for invoice in invoices_by_year]
    datayear = [invoice['num_invoices'] for invoice in invoices_by_year]
    # Graphique par mois
    invoices_by_month = (
        Invoice.objects.annotate(month=TruncMonth('date_creation'))
        .values('month')
        .annotate(num_invoices=Count('id'))
        .order_by('month')
    )

    # Formater le nom du mois en français
    labelmonth = [invoice['month'].strftime('%B %Y') for invoice in invoices_by_month]
    datamonth = [invoice['num_invoices'] for invoice in invoices_by_month]
    # Rétablir la localisation par défaut
    locale.setlocale(locale.LC_TIME, '')

    total = 0

    for objet in Invoice.objects.all():
        if isinstance(objet.total, (int, float)):
            total += objet.total

    context = {
        'client': client,
        'facture': facture,
        'argent': total,
        'ba': ba,

        'clients': clients_with_invoice_count,
        'labels': labels,
        'data': data,

        'labelyear': labelyear,
        'datayear': datayear,

        'labelmonth': labelmonth,
        'datamonth': datamonth,
    }

    return render(request,"staffpage/index.html",context)



@login_required(login_url='/')
def client_list(request):

    client = Client.objects.all()

    context = {
        'client': client,
    }

    return render(request,"staffpage/list_client.html", context)


