from django.urls import path,include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
  path('',views.accommodationloginview,name='accommodationloginview'),#root url

  

  path('accommodationformview',views.accommodationformview,name='accommodationformview'),

  path('accommodationaccountview',views.accommodationaccountview,name='accommodationaccountview'),

]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)