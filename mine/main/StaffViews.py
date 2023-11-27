from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from main.forms import *
from django.shortcuts import get_object_or_404, redirect, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import transaction 
from main.sup import *
import qrcode

import random
import string
from main.models import *
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from main.models import *
import datetime
from django.template.loader import get_template
import json
from django.contrib.auth.decorators import login_required

import pdfkit




@login_required(login_url='/')
def add_client(request):
    return render(request,"staffpage/add_client.html")


@login_required(login_url='/')
# @method_decorator(login_required(login_url='show_login'))
def add_client_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        form=AddClientForm(request.POST,request.FILES)
        if form.is_valid():
            nom=form.cleaned_data["nom"]
            prenom=form.cleaned_data["prenom"]
            adresse=form.cleaned_data["adresse"]
            telephone=form.cleaned_data["telephone"]
            email=form.cleaned_data["email"]
            sexe=form.cleaned_data["sexe"]
            num_aggregation=form.cleaned_data["num_aggregation"]
            staff= get_object_or_404(Staff, admin_id=request.user.id)
            try:
                client=Client(staff=staff,nom=nom,prenom=prenom,adresse=adresse,telephone=telephone,email=email,sexe=sexe,num_aggregation=num_aggregation)
                client.save()
                messages.success(request,"Client Ajouté avec Succés")
                return HttpResponseRedirect(reverse("add_client"))
            except Exception as e:
                messages.error(request,"Echec de l'ajout" + str(e))
                return HttpResponseRedirect(reverse("add_client"))
        else:
            form=AddClientForm(request.POST)
            return render(request, "staffpage/add_client.html", {"form": form})



@login_required(login_url='/')
@transaction.atomic()
def get_demande(request):
        
        client = Client.objects.all()
        context = {
        'client': client,
            }
        
        if request.method=="GET":
            return render(request, 'staffpage/add_facture.html', context)

        elif request.method=="POST":
        
            items = []

            try:

                client = request.POST.get('client')

                date_creation = request.POST.get('date_creation')
                
                date_fin = request.POST.get('date_fin')

                articles = request.POST.getlist('article')

                qties = request.POST.getlist('qty')

                titre_en_caract = request.POST.getlist('titre_en_caract')

                units = request.POST.getlist('unit')

                total_a = request.POST.getlist('total-a')

                total = request.POST.get('total')

                with transaction.atomic():
                

                    user= get_object_or_404(Staff, admin_id=request.user.id)
                    

                    invoice_object = {
                        'client_id': client,

                        'date_creation':date_creation,

                        'date_fin':date_fin,
                        
                        'user':user,
                        
                        'total': total,
                        
                        
                    }

                    invoice = Invoice.objects.create(**invoice_object)

                    for index, article in enumerate(articles):

                        data = Article(
                            invoice_id = invoice.id,
                            name = article,
                            titre_en_caract = titre_en_caract[index],
                            quantity=qties[index],
                            unit_price = units[index],
                            total = total_a[index],
                        )

                        items.append(data)

                    created = Article.objects.bulk_create(items)   
                    
                    if created:
                        messages.success(request, "Facture ajouter avec Success.") 
                    else:
                        messages.error(request, "Desolé echec de l'enregistrement veuillez verifier les données saisits.")    
                        
            except Exception as e:
                messages.error(request, f"Erreur: {e}.")   

        return  render(request, 'staffpage/add_facture.html', context)


@login_required(login_url='/')
def list_facture(request):

    invoice = Invoice.objects.all()

    context = {
        'invoice': invoice,
    }

    return render(request,"staffpage/list_facture.html", context)




class InvoiceVisualizationView(View):

    template_name = 'staffpage/facture_view.html'

    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')

        context = get_invoice(pk)

        return render(request, self.template_name, context)




@login_required(login_url='/')
def get_ba(request):
        
        client = Client.objects.all()
        context = {
        'client': client,
            }
        
        if request.method=="GET":
            return render(request, 'staffpage/add_ba.html', context)

        elif request.method=="POST":

                client_id = request.POST.get('client')

                parametre = request.POST.get('parametre')

                lettre_majuscule = random.choice(string.ascii_uppercase)
                chiffres = ''.join(random.choices(string.digits, k=5))
                numero_ordre = lettre_majuscule + chiffres

                type_echantillon = request.POST.get('type_echantillon')

                user= get_object_or_404(Staff, admin_id=request.user.id)

                try:
                    ba=BordereauAdministratif(user=user,type_echantillon=type_echantillon,parametre=parametre,numero_ordre=numero_ordre,client_id=client_id)
                    ba.save()
                    messages.success(request,"Bordereau Ajouter avec Success")
                    return HttpResponseRedirect(reverse("add_client"))
                except Exception as e:
                    messages.error(request,"Echec de l'ajout" + str(e))
                    return HttpResponseRedirect(reverse("add_ba"))    

        return  render(request, 'staffpage/add_ba.html', context)



@login_required(login_url='/')
def list_ba(request):

    ba = BordereauAdministratif.objects.all()

    context = {
        'ba': ba,
    }

    return render(request,"staffpage/list_ba.html", context)




def generate_qr(request):
    values_from_database = Article.objects.all()

    qr_codes = []  # Stockez les codes QR générés

    for index, article in enumerate(values_from_database):
        qr_code_data = f"Demandeur: {article.invoice.client.prenom} {article.invoice.client.nom}\nAdresse: {article.invoice.client.adresse}\nTelephone: {article.invoice.client.telephone}\nTitre en Caracts:{article.titre_en_caract}\nQuantite:{article.quantity}\nTotal:{article.get_total}"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_code_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Stockez l'image ou envoyez-la directement au client si nécessaire
        qr_codes.append(img)

    # Vous pouvez renvoyer les codes QR générés dans une seule réponse ou les stocker
    # pour une utilisation ultérieure, en fonction de vos besoins.
    response = HttpResponse(content_type="image/png")
    qr_codes[0].save(response, "PNG")  # Vous pouvez ajuster cela en fonction de votre logique.

    return response




def get_invoice_final_pdf(request, *args, **kwargs):
    """ generate pdf file from html file """

    id = kwargs.get('id')

    context = get_invoice(id)

    context['date'] = datetime.datetime.today()

    # get html file
    template = get_template('staffpage/facture_pdf.html')

    # render html with context variables

    html = template.render(context)

    # options of pdf format

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        "enable-local-file-access":True,
        
    }

    # generate pdf
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    pdf = pdfkit.from_string(html, False, options=options,configuration=config)


    response = HttpResponse(pdf, content_type='application/pdf')

    response['Content-Disposition'] = "attachement"

    return response


class BordereauVisualizationView(View):

    template_name = 'staffpage/bordereau.html'


    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')

        context = get_invoice(pk)

        

        return render(request, self.template_name, context)



def get_bordereau_final_pdf(request, *args, **kwargs):
    """ generate pdf file from html file """

    id = kwargs.get('id')

    context = get_invoice(id)

    context['date'] = datetime.datetime.today()

    # get html file
    template = get_template('staffpage/bordereau_pdf.html')

    # render html with context variables

    html = template.render(context)

    # options of pdf format

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        "enable-local-file-access":True,
        
    }

    # generate pdf
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    pdf = pdfkit.from_string(html, False, options=options,configuration=config)


    response = HttpResponse(pdf, content_type='application/pdf')

    response['Content-Disposition'] = "attachement"

    return response
