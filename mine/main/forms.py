from django import forms

from main.models import *


# class CustomImageWidget(forms.FileInput):
#     def __init__(self, attrs=None, *args, **kwargs):
#         default_attrs = {'class': 'form-control'}
#         if attrs:
#             default_attrs.update(attrs)
#         super().__init__(default_attrs, *args, **kwargs)



class DateInput(forms.DateInput):
    input_type = "date"



class AddStaffForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    password=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="Prenom",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Nom",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    address=forms.CharField(label="Adresse",max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}))
    phone_number=forms.CharField(label="Numero Telephone",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))


    gender_choice=(
        ("Masculin","Masculin"),
        ("Feminin","Feminin"),
        ("Autres","Autres"),
    )
    sexe=forms.ChoiceField(label="Sexe",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))



class AddClientForm(forms.Form):
    prenom=forms.CharField(label="Prenom",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    nom=forms.CharField(label="Nom",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    adresse=forms.CharField(label="Adresse",max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}))
    telephone=forms.CharField(label="Numero Telephone",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    num_aggregation=forms.CharField(label="Numero Aggrement",max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}))
    date_aggregation = forms.DateField(label="Date Aggrement", widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))
    gender_choice=(
        ("Masculin","Masculin"),
        ("Feminin","Feminin"),
        ("Autres","Autres"),
    )
    sexe=forms.ChoiceField(label="Sexe",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))







