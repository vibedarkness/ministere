from main.models import *


def get_invoice(pk):

    obj = Invoice.objects.get(pk=pk)

    articles = obj.article_set.all()

    context = {
        'obj': obj,
        'articles': articles
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