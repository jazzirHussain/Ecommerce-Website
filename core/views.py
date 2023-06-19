from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Item,Order,Filters,PromoCode,Profile,OrderItem,ProfileOther
import os
from django.contrib import messages
from string import *

# Create your views here.

def chck_out(request):
    if request.user.is_authenticated:
        user = request.user
        usr_id = user.id
        user_profile = ProfileOther.objects.filter(user_id=usr_id).first()
        if user_profile:
            dflt_adrs_id = user_profile.default_adres
            dflt_adrs = Profile.objects.filter(id=dflt_adrs_id).first()
            dflt_bool = True
        if request.method == 'POST':
            if 'redeem' in request.POST:
                code = request.POST['code']
                if PromoCode.objects.filter(name=code):
                    disc = PromoCode.objects.get(name=code).disc
                    code = PromoCode.objects.get(name=code).name
                    items = OrderItem.objects.filter(user_id=usr_id)
                    count = OrderItem.objects.filter(user_id=usr_id).count()
                    total = 0
                    for item in  items:
                        if item.citem.disc_price:
                            item_total = item.citem.disc_price * item.quant
                            total += item_total
                        else:
                            item_total = item.citem.price * item.quant
                            total += item_total
                    total -= disc
                    if user_profile:
                        return render(request, 'checkout-page.html',{'items':items, 'code':code, 'count':count,'total':total,'disc':disc, 'applied':True, 'vanish':True, 'user':user,'dflt_adrs':dflt_adrs})
                    else:
                        return render(request, 'checkout-page.html',{'items':items, 'code':code, 'count':count,'total':total,'disc':disc, 'applied':True, 'vanish':True, 'user':user})
                else:
                    user = request.user
                    items = OrderItem.objects.filter(user_id=usr_id)
                    count = OrderItem.objects.filter(user_id=usr_id).count()
                    total = 0
                    for item in  items:
                        if item.citem.disc_price:
                            item_total = item.citem.disc_price * item.quant
                            total += item_total
                        else:
                            item_total = item.citem.price * item.quant
                            total += item_total
                    if user_profile:
                        return render(request, 'checkout-page.html',{'items':items, 'count':count,'total':total, 'applied':False,'user':user,'dflt_adrs':dflt_adrs})
                    else:
                       return render(request, 'checkout-page.html',{'items':items, 'count':count,'total':total, 'applied':False,'user':user}) 
        else:
            user = request.user
            items = OrderItem.objects.filter(user_id=usr_id)
            count = OrderItem.objects.filter(user_id=usr_id).count()
            total = 0
            for item in  items:
                if item.citem.disc_price:
                    item_total = item.citem.disc_price * item.quant
                    total += item_total
                else:
                    item_total = item.citem.price * item.quant
                    total += item_total
            if user_profile:
                return render(request, 'checkout-page.html',{'items':items, 'count':count,'total':total, 'user':user,'dflt_adrs':dflt_adrs})
            else:
                return render(request, 'checkout-page.html',{'items':items, 'count':count,'total':total, 'user':user})
    else:
        return redirect('http://127.0.0.1:8000/accounts/login/')


def HomeView(request):
    user = request.user
    citems = OrderItem.objects.filter(user_id=user.id).count()
    items = Item.objects.all()
    filters = Filters.objects.all()
    if request.method =='POST':
        search_wrd = request.POST['search'].upper()
        search_obj = Filters.objects.filter(category=search_wrd).first()
        search = search_obj.id
        return render(request, 'home-filter.html', {'items':items, 'value':search,'filters': filters,'user':user,'citems_count':citems})
    else:
        return render(request, 'home-page.html', {'filters': filters, 'items':items,'user':user,'citems_count':citems})


   
def homefilview(request, **kwargs):
    user = request.user
    citems = OrderItem.objects.filter(user_id=user.id).count()
    items = Item.objects.all()
    filters = Filters.objects.all()
    if request.method =='POST':
        search = request.POST['search'].upper()              
        return render(request, 'home-filter.html', {'items':items, 'value':search,'filters': filters,'user':user,'citems_count':citems})
    else:
        url = request.get_full_path()
        urls = os.path.basename(url)
        urls = int(urls)
        return render(request, 'home-filter.html', {'items':items, 'value':urls,'filters': filters,'user':user,'citems_count':citems})


def ItemDetailView(request, **kwargs):
    user = request.user
    usr_id = user.id
    url = request.get_full_path()
    urls = os.path.basename(url)
    item = Item.objects.filter(slug=urls).first()  
    ditem = OrderItem.objects.filter(user_id=usr_id).filter(citem_id=item.id).first()
    if request.method == 'POST':  
        quant = request.POST['quantity']        
        if 'remove' in request.POST:  
            if int(quant) > 0:                   
                if ditem.quant > 1:
                    ditem.quant = int(ditem.quant) - int(quant)
                    ditem.save()
                    cart_count = ditem.quant
                    if ditem.quant <= 0:
                        ditem.delete()
                        return render(request, 'product-page.html', {'item':item, 'cart_item':False,'user':user}) 
                else:
                    ditem.delete()
                if ditem:
                    return render(request, 'product-page.html', {'item':item, 'cart_item':True, 'user':user, 'count':cart_count})
                else:
                    return render(request, 'product-page.html', {'item':item, 'cart_item':False,'user':user})
            else:
                if ditem:
                    cart_count = ditem.quant
                    return render(request, 'product-page.html', {'item':item, 'cart_item':True, 'user':user, 'count':cart_count})
                else:
                    return render(request, 'product-page.html', {'item':item, 'cart_item':False,'user':user})
        elif 'add' in request.POST:
            quant = request.POST['quantity']
            if int(quant) > 0:
                if ditem:
                    ditem.quant = int(ditem.quant) + int(quant)
                    ditem.save()
                    cart_count = ditem.quant
                    return render(request, 'product-page.html', {'item':item, 'cart_item':True,'user':user, 'count':cart_count})
                else:
                    new_item = OrderItem.objects.create(user=user,citem=item, quant=quant)
                    cart_count = new_item.quant
                    return render(request, 'product-page.html', {'item':item, 'cart_item':True,'user':user, 'count':cart_count})
            else:
                if ditem:
                    cart_count = ditem.quant
                    return render(request, 'product-page.html', {'item':item, 'cart_item':True,'user':user, 'count':cart_count})
                else:
                    return render(request, 'product-page.html', {'item':item, 'cart_item':False,'user':user})
    else:
            if ditem:
                cart_count = ditem.quant
                return render(request, 'product-page.html', {'item':item, 'cart_item':True,'user':user, 'count':cart_count})
            else:
                return render(request, 'product-page.html', {'item':item, 'cart_item':False,'user':user})


def cart(request):
    if request.user.is_authenticated:
        user = request.user
        usr_id = user.id
        items = OrderItem.objects.filter(user_id=usr_id)
        return render(request, 'cart.html', {'items':items,'user':user})
    else:
        return render(request, 'account/login.html')


def adress(request):
    user = request.user
    usr_id = user.id
    adresses = Profile.objects.filter(user_id=usr_id)
    count = OrderItem.objects.filter(user_id=usr_id).count()
    if request.method == 'POST':
        if 'dlt' in request.POST:
            adrs_id = request.POST['delete_adrs']
            dlt_adrs = Profile.objects.filter(pk=adrs_id)
            dlt_adrs.delete()
            return render(request, 'adress.html',{'adresses':adresses,'user':user,'count':count})
    else:
        return render(request, 'adress.html',{'adresses':adresses,'user':user,'count':count})



def adress_used(request, **kwargs):
    user = request.user
    usr_id = user.id
    url = request.get_full_path()
    urls = os.path.basename(url)
    adrs_obj = Profile.objects.filter(user_id = usr_id).filter(id=urls).first()
    items = OrderItem.objects.filter(user_id=usr_id)
    count = OrderItem.objects.filter(user_id=usr_id).count()
    if request.method == 'POST':
        if 'redeem' in request.POST:           
            code = request.POST['code']
            code_obj_chck = PromoCode.objects.filter(name=code)
            if code_obj_chck:
                code_obj = code_obj_chck.first()
                disc = code_obj.disc
                code = code_obj.name            
                total = 0
                for item in  items:
                    if item.citem.disc_price:
                        item_total = item.citem.disc_price * item.quant
                        total += item_total
                    else:
                        item_total = item.citem.price * item.quant
                        total += item_total
                total -= disc
                return render(request, 'checkout-page-adress.html',{'items':items, 'code':code, 'count':count,'total':total,'disc':disc, 'applied':True, 'vanish':True, 'user':user,'add_user':adrs_obj})
            else:
                total = 0
                for item in  items:
                    if item.citem.disc_price:
                        item_total = item.citem.disc_price * item.quant
                        total += item_total
                    else:
                        item_total = item.citem.price * item.quant
                        total += item_total
                return render(request, 'checkout-page-adress.html',{'items':items, 'count':count,'total':total, 'applied':False,'user':user,'add_user':adrs_obj})
    else:
        total = 0
        for item in  items:
            if item.citem.disc_price:
                item_total = item.citem.disc_price * item.quant
                total += item_total
            else:
                item_total = item.citem.price * item.quant
                total += item_total
        return render(request, 'checkout-page-adress.html',{'items':items, 'count':count,'total':total, 'user':user,'add_user':adrs_obj})


def profile(request):
    user = request.user
    count = OrderItem.objects.filter(user_id=user.id).count()
    if request.method == 'POST':
        if 'adrs_save' in request.POST:
            adrs = request.POST['adress_usr']
            if adrs:
                usr_cont = request.POST['cont_usr']
                usr_state = request.POST['state_usr']
                usr_zip_code = request.POST['zip_usr']
                usr_cont = usr_cont.capitalize()
                usr_state = usr_state.capitalize()
                adrs = capwords(adrs)
                adrs_obj = Profile.objects.create(user=request.user,add=adrs,cont=usr_cont,state=usr_state,zip_code=usr_zip_code)
                if request.POST.get('dflt_adrs',False):
                    chck_user = ProfileOther.objects.filter(user_id=user.id).first()
                    if chck_user:
                        chck_user.default_adres = adrs_obj.pk
                        chck_user.save()
                    else:
                        ProfileOther.objects.create(user=user,default_adres=adrs_obj.pk)
                return render(request, 'profile.html',{'user':user,'count':count})
            else:
                return render(request, 'profile.html',{'user':user,'count':count})
        if 'dtls_save' in request.POST:
            if not user.first_name:
                frst_nme = request.POST['first_name']
                user.first_name = frst_nme
                user.save()
            if not user.last_name:
                lst_nme = request.POST['last_name']
                user.last_name = lst_nme
                user.save()
            if not user.email:
                emile = request.POST['email_usr']
                user.email = emile
                user.save()
            return render(request, 'profile.html',{'user':user,'count':count})
    else:
        return render(request, 'profile.html',{'user':user,'count':count})























































































































































