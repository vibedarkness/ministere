from main.models import *


def get_invoice(pk):
    obj = Invoice.objects.get(pk=pk)
    super_users = AdminHOD.objects.filter(admin__user_type=1).values_list('admin__email', flat=True)

    articles = obj.article_set.all()

    context = {
        'obj': obj,
        'articles': articles,
        'email_admin': super_users
    }

    return context


# def get_invoice_final(id):

#     validate = Invoice.objects.get(id=id)
#     invoice = Invoice.objects.all()




#     articles = validate.purchase_recept.article_set.all()

#     context = {
#         'invoice': invoice,
#         'articles': articles,
#         'validate':validate,


#     }

#     return context