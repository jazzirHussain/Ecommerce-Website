from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser,User
from phone_field import PhoneField
from django.dispatch import receiver
from django.db.models.signals import post_save
#from .forms import CustomSignupForm
CATEGORY_CHOICES = (
    ('S', 'SHIRT'),
    ('SW', 'SPORTWARE'),
    ('OW', 'OUTWARE'),
    ('EC', 'ELECTRONICS'),
    ('HA', 'HOMEAPPLIANCES'),
    ('FW', 'FOOTWARE')
)
  
LABEL_CHOICES = (
    ('N', 'NEW'),
    ('BS', 'BestSeller')
)

class Filters(models.Model):
    category = models.CharField(max_length=20)
    

    def __str__(self):
        return self.category

    def get_value(self):
        return reverse('core:homefilter', kwargs={'slug': self.pk})

class Item(models.Model):
    tittle = models.CharField(max_length=20)
    price = models.FloatField()
    disc_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Filters, on_delete=models.CASCADE)
    label = models.CharField(choices=LABEL_CHOICES, max_length=2, blank=True, null=True)
    slug = models.SlugField(unique=True)
    desc = models.TextField()
    img = models.ImageField(upload_to='itemimage')


    def __str__(self):
        return self.tittle

    def get_absolute_url(self):
        return reverse('core:prdcts', kwargs={'slug': self.slug})






class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    citem = models.ForeignKey(Item, on_delete=models.CASCADE)
    quant = models.IntegerField()
    

    def __str__(self):
        return self.citem.tittle


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    orederd = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    def __str__(self):
        return self.user.username
    

class PromoCode(models.Model):
    name = models.CharField(max_length=20, unique=True)
    disc = models.IntegerField()
    
    
    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    add = models.TextField(blank=True,null=True)
    cont = models.CharField(max_length=50,blank=True,null=True)
    state = models.CharField(max_length=50,blank=True,null=True)
    zip_code = models.IntegerField(blank=True,null=True)
    def __str__(self):
        return self.user.username
    def get_unique_id(self):
            return reverse('core:adress_used', kwargs={'slug': self.pk})

class ProfileOther(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_adres = models.IntegerField(null=True,blank=True)
    phone_number = PhoneField(blank=True,null=True)

    def __str__(self):
        return self.user.username



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
         ProfileOther.objects.create(user=instance)
    instance.profileother.save()














 








