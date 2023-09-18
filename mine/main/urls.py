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
    path('generate-qr/', StaffViews.generate_qr, name='generate_qr'),




]
