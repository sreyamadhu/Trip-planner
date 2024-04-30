from django.shortcuts import render
from users.models import CustomUser
from .models import Accommodationdetailstable
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def accommodationloginview(request):
  global user_profile
  global accommodation
  user_profile=request.user
  if Accommodationdetailstable.objects.filter(user=user_profile).exists():
    
    accommodation=Accommodationdetailstable.objects.get(user=user_profile)
    return accommodationaccountview(request)
  else:
    
    return accommodationformview(request)
    
@login_required  
def accommodationformview(request):
  user_profile=request.user
  global accommodation

  if Accommodationdetailstable.objects.filter(user=user_profile).exists():
    
    accommodation=Accommodationdetailstable.objects.get(user=user_profile)
    
    #***********************
    if request.method == "POST":
      name=request.POST.get("accommodation_name")
      accommodation_district=request.POST.get("accommodation_district")
      accommodation_location=request.POST.get("accommodation_location")
      accommodation_lowest_price=request.POST.get("accommodation_lowest_price")
      accommodation_highest_price=request.POST.get("accommodation_highest_price")
      accommodation_restaurant = request.POST.get('accommodation_restaurant')
      image1 = request.FILES.get('accommodation_image1')
      image2 = request.FILES.get('accommodation_image2')
      if accommodation_restaurant is not None and accommodation_restaurant=='on':
        restaurant=True
      else:
        restaurant=False
      
      if name:
        if Accommodationdetailstable.objects.exclude(id=accommodation.id).filter(name=name).exists():
          print("restaurant with same already exists")
          messages.error(request, "Name already exists")
          accommodation_django_messages = messages.get_messages(request)
          return render(request,"acco-form2.html",{'accommodation':accommodation,'user_profile':user_profile,'accommodation_django_messages':accommodation_django_messages})
        else:
          accommodation.name = name
      if accommodation_district:
        accommodation.district = accommodation_district
      if accommodation_location:
        accommodation.location = accommodation_location
      if accommodation_lowest_price:
        accommodation.lowest_rate = accommodation_lowest_price
      if accommodation_highest_price:
        accommodation.highest_rate = accommodation_highest_price
      if restaurant:
        accommodation.restaurant = restaurant
      if image1:
        accommodation.accommodation_image1 = image1
      if image2:
        accommodation.accommodation_image2 = image2

      accommodation.save()
      print("profile updated succcesfully")
      accommodation=Accommodationdetailstable.objects.get(user=user_profile)
      return render(request,"acco-profile.html",{'accommodation':accommodation,'user_profile':user_profile})
    else:
      return render(request,"acco-form2.html",{'accommodation':accommodation,'user_profile':user_profile})

    #***********************

  elif request.method == "POST":
    name=request.POST.get("accommodation_name")
    accommodation_district=request.POST.get("accommodation_district")
    accommodation_location=request.POST.get("accommodation_location")
    accommodation_lowest_price=request.POST.get("accommodation_lowest_price")
    accommodation_highest_price=request.POST.get("accommodation_highest_price")
    accommodation_restaurant = request.POST.get('accommodation_restaurant')
    image1 = request.FILES.get('accommodation_image1')
    image2 = request.FILES.get('accommodation_image2')
    if accommodation_restaurant is not None and accommodation_restaurant=='on':
      restaurant=True
    else:
      restaurant=False
    accommodation=Accommodationdetailstable(
            user=request.user,  
            name=name,
            district=accommodation_district,
            location=accommodation_location,
            lowest_rate=accommodation_lowest_price,
            highest_rate=accommodation_highest_price,
            restaurant=restaurant,
            accommodation_image1=image1,
            accommodation_image2=image2,
    )
    accommodation.save()
    accommodation=Accommodationdetailstable.objects.get(user=user_profile)
    return render(request,"acco-profile.html",{'accommodation':accommodation,'user_profile':user_profile})
  
    
  else:
    return render(request,"acco-form.html",{'user_profile':user_profile})
  
@login_required 
def accommodationaccountview(request):
  global accommodation
  return render(request, "acco-profile.html", {'accommodation': accommodation,'user_profile':user_profile})
  try:
      accommodation = Accommodationdetailstable.objects.get(user=user)
      print("accommodation->", accommodation)
      return render(request, "homeaccommodation.html", {'accommodation': accommodation})
  except Accommodationdetailstable.DoesNotExist:
      print("Accommodation details not found for this user.")
      return render(request, "homeaccommodation.html", {'accommodation': None})
  


'''
name=request.POST["name"]
    district=request.POST["district"]
    location=request.POST["location"]
    lowest_rate=request.POST["lowest_rate"]
    highest_rate=request.POST["highest_rate"]
    restaurant = request.POST.get('restaurant')
    image1 = request.FILES.get('image1')
    image2 = request.FILES.get('image2')
'''