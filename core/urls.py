from django.urls import path
from .views import HomeView,chck_out,ItemDetailView,homefilview,adress,adress_used,profile
from .views import cart

app_name = 'core'
urlpatterns = [
    path('', HomeView, name='item_list'),
    path('<slug:slug>', homefilview, name='homefilter'),
    path('chck_out/', chck_out, name='chck_out'),
    path('cart/', cart , name='cart'),
    path('prdcts/<slug>', ItemDetailView, name='prdcts'),
    path('adress/', adress, name='adress'),
    path('chck_out/<slug>',adress_used, name='adress_used'),
     path('profile/',profile, name='profile')
]






































