from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from num2words import num2words

class CustomUser(AbstractUser):
    user_type_data=((1,"HOD"),(2,"Staff"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)

class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Staff(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address=models.TextField()
    phone_number= models.CharField(max_length = 150)
    sexe= models.CharField(max_length = 150)
    status= models.CharField(max_length = 150, default=1, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Client(models.Model):
    nom= models.CharField(max_length=200)
    prenom= models.CharField(max_length=200)
    adresse= models.CharField(max_length=200)
    telephone=models.CharField(max_length=200,unique=True)
    email=models.CharField(max_length=200,unique=True)
    sexe=models.CharField(max_length=200)
    staff=models.ForeignKey(Staff, on_delete=models.CASCADE)

    def sexechange(self):
        if self.sexe=="Masculin":
            return "Monsieur"
        elif self.sexe=="Feminin":
            return "Madame"


class Invoice(models.Model):
    client=models.ForeignKey(Client, on_delete=models.PROTECT)
    total = models.DecimalField(max_digits=1000, decimal_places=2,null=True, default=0)
    date_creation = models.DateTimeField(auto_now=False, auto_now_add=True,null=True, )
    status = models.SmallIntegerField(default=0, null=True)
    user=models.ForeignKey(Staff,on_delete=models.PROTECT, related_name="secretary_rept", null=True, default=2)



    @property
    def get_total(self):
        articles = self.article_set.all()   
        total = sum(article.get_total for article in articles)
        return total

    def numwords(self):
        articles = self.article_set.all()
        total = sum(article.get_total for article in articles)

        return num2words(total, lang='fr')






class Article(models.Model):
    
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

    name = models.CharField(max_length=32)
    
    titre_en_caract=models.IntegerField()

    quantity = models.IntegerField()

    unit_price = models.DecimalField(max_digits=1000, decimal_places=2)

    total = models.DecimalField(max_digits=1000, decimal_places=2)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    @property
    def get_total(self):
        total = self.quantity * self.unit_price   
        return total 


class BordereauAdministratif(models.Model):
    client=models.ForeignKey(Client, on_delete=models.CASCADE)
    parametre=models.CharField(max_length=200)
    date=models.DateField(auto_now_add=True)
    numero_ordre=models.CharField(max_length=200,null=True,default="")
    type_echantillon=models.CharField(max_length=500)
    user=models.ForeignKey(Staff, on_delete=models.CASCADE,null=True, default=2)




@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type==2:
            Staff.objects.create(admin=instance,address="",sexe="",phone_number="", status=1)
        
@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.staff.save()
           
