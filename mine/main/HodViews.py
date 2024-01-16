from django.shortcuts import render ,get_object_or_404, redirect, reverse
from main.models import *

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from main.forms import *
from django.contrib.auth.decorators import login_required
from main.sup import *
from django.views import View
import pdfkit
import datetime
from django.template.loader import get_template
import qrcode


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



@login_required(login_url='/')
def list_facture(request):

    invoice = Invoice.objects.all()

    context = {
        'invoice': invoice,
    }

    return render(request,"adminpage/list_facture.html", context)


class InvoiceVisualizationView(View):

    template_name = 'adminpage/facture_view.html'

    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')

        context = get_invoice(pk)

        return render(request, self.template_name, context)
    



class AttestationVisualizationView(View):

    template_name = 'adminpage/attestation_facture.html'


    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')

        context = get_invoice(pk)

        

        return render(request, self.template_name, context)





def get_invoice_final_pdf(request, *args, **kwargs):
    """ generate pdf file from html file """

    id = kwargs.get('id')

    context = get_invoice(id)

    context['date'] = datetime.datetime.today()

    # get html file
    template = get_template('adminpage/facture_pdf.html')

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



def generate_attestation_qr(request,attestation_id):
    values_from_database = Article.objects.filter(invoice__id=attestation_id)

    # Assurez-vous qu'il y a au moins un article lié à la facture
    if not values_from_database.exists():
        return HttpResponse("Aucun article trouvé pour cette facture.")

    # Sélectionnez le premier article pour générer le code QR
    article = values_from_database.first()

    qr_code_data = f" Demandeur: {article.invoice.client.prenom} {article.invoice.client.nom}\n Adresse: {article.invoice.client.adresse}\n Telephone: {article.invoice.client.telephone}\n Numero Aggrement: {article.invoice.client.num_aggregation}\n Date Aggrement: {article.invoice.client.date_aggregation}\n Titre en Caracts:{article.titre_en_caract}\n Quantite:{article.quantity}\n Total:{article.get_total}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_code_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Renvoyez l'image du code QR dans la réponse
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")

    return response


def get_attestation_final_pdf(request, *args, **kwargs):
    """ generate pdf file from html file """

    id = kwargs.get('id')

    context = get_invoice(id)

    context['date'] = datetime.datetime.today()

    # get html file
    template = get_template('adminpage/attestation_facture_pdf.html')

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




@login_required(login_url='/')
def client_list(request):

    client = Client.objects.all()

    context = {
        'client': client,
    }

    return render(request,"adminpage/list_client.html", context)


@login_required(login_url='/')
def list_ba(request):

    ba = BordereauAdministratif.objects.all()

    context = {
        'ba': ba,
    }

    return render(request,"adminpage/list_ba.html", context)




class BordereauAdminVisualizationView(View):

    template_name = 'adminpage/bordereau_admin.html'


    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')

        context = get_invoice(pk)

        

        return render(request, self.template_name, context)


def get_bordereau_admin_final_pdf(request, *args, **kwargs):
    """ generate pdf file from html file """

    id = kwargs.get('id')

    context = get_invoice(id)

    context['date'] = datetime.datetime.today()

    # get html file
    template = get_template('adminpage/bordereau_admin_pdf.html')

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
