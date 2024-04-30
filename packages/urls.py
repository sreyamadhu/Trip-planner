from django.urls import path,include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
  path('',views.home,name='home'),#root url
  path('home',views.home,name='home'),
  path('logoutview',views.logoutview,name='logoutview'),
  path('packageview',views.packageview,name='packageview'),
  path('accountview',views.accountview,name='accountview'),
  path('aboutview',views.aboutview,name='aboutview'),
  path('landscapeview',views.landscapeview,name='landscapeview'),
  path('itineraryviewagain',views.itineraryviewagain,name='itineraryviewagain'),
  path('spotdetailsview/<str:spotname_copy>/',views.spotdetailsview,name='spotdetailsview'),
  path('mapview/<str:day_key_value>/',views.mapview,name='mapview'),
  #path('createpackageview',views.createpackageview,name='createpackageview'),
  path('listofaccommodationsview/<str:district>/',views.listofaccommodationsview,name='listofaccommodationsview'),
  #path('budgetview',views.budgetview,name='budgetview'),#budgetview=is path given in url,name=budgetviewpackages=is name used to refer it in other places
  #path('destinationview',views.destinationview,name='destinationview'),
]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)