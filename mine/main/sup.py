from main.models import *


def get_invoice(pk):

    obj = Invoice.objects.get(pk=pk)

    articles = obj.article_set.all()

    context = {
        'obj': obj,
        'articles': articles
    }

    return context