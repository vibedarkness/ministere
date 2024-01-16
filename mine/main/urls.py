from django.urls import path
from main import views,HodViews,StaffViews

urlpatterns = [
    path('',views.LoginPage,name="show_login"),
    path('doLogin',views.doLogin,name="do_login"),
    path('logout_user',views.logout_user,name="logout"),

    #==============Admin urls=======================
    path("administrateur",views.adminhome,name='admin_home'),
    path('add_staff',HodViews.add_staff,name="add_staff"),
    path('add_staff_save',HodViews.add_staff_save,name="add_staff_save"),
    path('staff_list',HodViews.list_staff,name="staff_list"),
    path('facture_admin/<int:pk>', HodViews.InvoiceVisualizationView.as_view(), name='facture_view_admin'),
    path('attestation/<int:pk>', HodViews.AttestationVisualizationView.as_view(), name='attestation_view_admin'),
    path('bordereau_admin/<int:pk>', HodViews.BordereauAdminVisualizationView.as_view(), name='bordereau_view_admin'),
    path("list_facture_admin",HodViews.list_facture,name='list_facture_admin'),
    path('facture_pdf_admin/<int:id>',HodViews.get_invoice_final_pdf, name="facture_pdf_admin"),
    path('attestation_pdf_admin/<int:id>',HodViews.get_attestation_final_pdf, name="attestation_pdf_admin"),
    path('bordereau_admin_pdf/<int:id>',HodViews.get_bordereau_admin_final_pdf, name="bordereau_admin_pdf"),
    path("client_list_admin",HodViews.client_list,name='client_list_admin'),
    path("list_ba_admin",HodViews.list_ba,name='list_ba_admin'),
    path('generate-attestation-qr/<int:attestation_id>/', HodViews.generate_attestation_qr, name='generate_attestation_qr'),


    #==============Staff Urls========================
    path("staff",views.staffhome,name='staff_home'),
    path("client_list",views.client_list,name='client_list'),
    path('add_client',StaffViews.add_client, name="add_client"),
    path('add_client_save',StaffViews.add_client_save, name="add_client_save"),
    path('add_facture', StaffViews.get_demande,name="add_facture"),
    path("list_facture",StaffViews.list_facture,name='list_facture'),
    path("list_ba",StaffViews.list_ba,name='list_ba'),
    path("add_ba",StaffViews.get_ba,name='add_ba'),
    path('facture/<int:pk>', StaffViews.InvoiceVisualizationView.as_view(), name='facture_view'),
    path('bordereau/<int:pk>', StaffViews.BordereauVisualizationView.as_view(), name='bordereau'),
    path('generate-qr/<int:invoice_id>/', StaffViews.generate_qr, name='generate_qr'),
    path('facture_pdf/<int:id>', StaffViews.get_invoice_final_pdf, name="facture_pdf"),
    path('bordereau_pdf/<int:id>', StaffViews.get_bordereau_final_pdf, name="bordereau_pdf")

]
