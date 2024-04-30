from django.urls import path,include
from . import views
#from packages.views import prefer
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
  path('',views.signupview,name='signup'),#root url
  path('signup',views.signupview,name='signup'),
  path('login',views.loginview,name='login'),
  path('profileupdationview',views.profileupdationview,name='profileupdationview'),
  #path('packages/',include('packages.urls')),
]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)