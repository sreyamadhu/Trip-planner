from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from accommodations.models import Accommodationdetailstable
from usercontribution.models import Review
from geopy.geocoders import ArcGIS,Nominatim
from geopy import distance
from django.conf import settings
from .models import Destination,Tourpackage

# Create your views here.

def logoutview(request):
    auth.logout(request)
    print("logged out")
    return redirect('/')

@login_required
def accountview(request):
    user_profile=request.user
    return render(request,'pages-profile.html',{'user_profile':user_profile})

@login_required
def aboutview(request):
    user_profile=request.user
    return render(request,'pages-about.html',{'user_profile':user_profile})

#home page view to select preferences
@login_required
def home(request):
  user_profile=request.user
  if request.method=="POST":
    return packageview(request)
    
  else:
    #pricelist=['under 5000','5000-10000','10000-15000','above 15000']
    daylist={'1':'1daypackage','2':'2daypackage','3':'3daypackage','4':'4daypackage','5':'5daypackage','6':'6daypackage','7':'7daypackage'}
    destinationlist=['Kozhikode','Wayanad',]
    return render(request,"pages-blank.html",{'daylist':daylist,'destinationlist':destinationlist,'user_profile':user_profile})
  

mainpackagedict=dict()
temppackagedict=dict()
mainpackagedictcopy=dict()
temppackagedictcopy=dict()
choosen_package_dict=dict()

#package generation 
@login_required
def packageview(request):
  global user_profile
  user_profile=request.user
  global day
  global destination
  global listoflandscapes
  listoflandscapes=['Beach','Temple','Mosque','Market','Pond','Shopping Centre','Park','Museum','Waterfall','Reservoir','Dam','Amusement park','Planetarium','Tourist attractions','Cinema theatre','Bird watching area','Fort','Hill station','Zoo','Garden','Wildlife park','View point','Island','Water bodies','River','Church','Palace','Animal park']
  if 'itinerary' in request.POST:
      return itineraryview(request, mainpackagedict)
  elif 'filterform' in request.POST:
      print("entering inside FILTERFORM in packageview elif1")
      return landscapefilter(request,mainpackagedictcopy,temppackagedictcopy,day)
  elif 'choiceform' in request.POST:
    print("entering inside CHOICEFORM in packageview elif2")
    day=request.POST.get('day')
    destination = request.POST.get('destination', '')
    mainpackagedict.clear()
    temppackagedict.clear()
    mainpackagelist=Tourpackage.objects.filter(district=destination,packagecategory=day).select_related('spotname').all() #to select all items fro tourpackage table where Tourpackage.spotname=Destination.spotname
    mainspotnamelist=[]
    for package in mainpackagelist:
      number=str(package.packagenumber)
      count=package.district+number
      key=count
      packagelist=[
                      package.id,                       #0
                      package.district,                 #1
                      package.packagenumber,            #2
                      package.daynumber,                #3
                      package.spottime,                 #4 
                      package.spotname,                 #5
                      package.spotname.location,        #6
                      package.spotname.landscape,       #7
                      package.spotname.cafespot,        #8
                      package.spotname.description,     #9
                      package.spotname.img,             #10
                      package.spotname.latitude,        #11
                      package.spotname.longitude,       #12
                      ]
      if key not in mainpackagedict:
        mainpackagedict[key]=[]
      mainpackagedict[key].append(packagelist)
      if key not in temppackagedict:
         temppackagedict[key]=[]
         temppackagedict[key].append(packagelist)
      else:
         continue
         
    return render(request,'tour-packages.html',{'mainpackagedict':mainpackagedict,'day':day,'temppackagedict':temppackagedict,'user_profile':user_profile,'district':destination,'listoflandscapes':listoflandscapes},)
  
  else:
    return render(request,'tour-packages.html',{'mainpackagedict':mainpackagedict,'day':day,'temppackagedict':temppackagedict,'user_profile':user_profile,'district':destination,'listoflandscapes':listoflandscapes})

#itinerary generation (view again)
@login_required
def itineraryviewagain(request): 
    user_profile=request.user 
    return render(request,'itinerary.html',{'choosen_package_dict':choosen_package_dict,'user_profile':user_profile,'district':destination,'listoflandscapes':listoflandscapes,'mainpackagedictcopy':mainpackagedictcopy,'mainpackagedict':mainpackagedict,})
  
#itinerary generation
@login_required
def itineraryview(request, mainpackagedict,):
    if request.method == "POST":
        package_code = request.POST.get('package_code')
        global choosen_package_list
        choosen_package_list=mainpackagedict[package_code]
        no_of_days=len(choosen_package_list)//3
        choosen_package_dict.clear()
        inner_dict=dict()     
        for inner_list in choosen_package_list:
          time_key=inner_list[4]
          inner_dict[time_key]=inner_list
          if len(inner_dict)<3:
            pass
          else :
            for i in range(1,no_of_days+1):
              day_key='DAY'+str(i)
              if day_key not in choosen_package_dict:
                choosen_package_dict[day_key]=dict(inner_dict)
                inner_dict.clear()
                break
              else:
                continue

    return render(request,'itinerary.html',{'choosen_package_dict':choosen_package_dict,'user_profile':user_profile,'district':destination,'listoflandscapes':listoflandscapes,'mainpackagedictcopy':mainpackagedictcopy,'mainpackagedict':mainpackagedict,})

#landscape filtered packages generation (view again)
@login_required                 
def landscapeview(request):
   user_profile=request.user
   return render(request,'landscape-packages.html',{'mainpackagedictcopy':mainpackagedictcopy,'day':day,'landscapelist':landscapelist,'temppackagedictcopy':temppackagedictcopy,'mainpackagedict':mainpackagedict,'temppackagedict':temppackagedict,'user_profile':user_profile,'district':destination,'listoflandscapes':listoflandscapes})

#landscape filtered packages generation 
@login_required
def landscapefilter(request,mainpackagedictcopy,temppackagedictcopy,day):
    if request.method == "POST":
      global landscapelist
      landscapelist=request.POST.getlist('filter')
      if not landscapelist:
         return redirect("packageview")
      else:
        mainpackagedictcopy.clear()
        temppackagedictcopy.clear()
        
        for item in landscapelist:
          for key,dictitems in mainpackagedict.items():
              if key not in mainpackagedictcopy:
                    for innerdictitems in dictitems:
                      if item in innerdictitems:
                          mainpackagedictcopy[key]=dictitems
                          for key,innerdictitems in mainpackagedictcopy.items():    
                             for insideitems in innerdictitems:
                              if key not in temppackagedictcopy:
                                temppackagedictcopy[key]=[]
                                temppackagedictcopy[key].append(insideitems)
                              break
       
        return render(request,'landscape-packages.html',{'mainpackagedictcopy':mainpackagedictcopy,'day':day,'landscapelist':landscapelist,'temppackagedictcopy':temppackagedictcopy,'mainpackagedict':mainpackagedict,'temppackagedict':temppackagedict,'user_profile':user_profile,'district':destination,'listoflandscapes':listoflandscapes})

#spotdetails showing function
@login_required      
def spotdetailsview(request,spotname_copy,):
   global spotdetails_spotname
   spotdetails_spotname=spotname_copy
   user_profile=request.user
   spotdetailslist=Destination.objects.get(spotname=spotdetails_spotname)
   spotdetailsdict=dict()
   spotdetailsdict={
      'spotname':spotdetailslist.spotname,
      'spotdistrict':spotdetailslist.spotdistrict,
      'location':spotdetailslist.location,
      'landscape':spotdetailslist.landscape,
      'cafespot':spotdetailslist.cafespot,
      'description':spotdetailslist.description,
      'img':spotdetailslist.img,
   }
   
   spotdetails_spotdistrict=spotdetailsdict['spotdistrict']
   spotreviewdetailsdict=dict()
   spotdetails_spotname_instance = Destination.objects.get(spotname=spotdetails_spotname)
   spotreviewdetailslist=Review.objects.filter(spotname=spotdetails_spotname_instance,spotdistrict=spotdetails_spotdistrict).all()
   number=0
   for review in spotreviewdetailslist:
      number=number+1
      reviewkey="Review"+str(number)
      reviewlist=[
                      review.id,            #0
                      review.user,          #1
                      review.spotname,      #2           
                      review.spotdistrict,  #3    
                      review.content,       #4
                      review.review_image1, #5    
                      review.review_image2, #6      
                      ]
      spotreviewdetailsdict[reviewkey]=reviewlist
  
   return render(request,"itinerary-spot-details.html",{'spotdetails_spotname':spotdetails_spotname,'user_profile':user_profile,'spotdetailsdict':spotdetailsdict,'spotreviewdetailsdict':spotreviewdetailsdict,'district':destination})

#map of itinerary generation
@login_required 
def mapview(request,day_key_value):
  user_profile=request.user
  map_package_dict=choosen_package_dict[day_key_value]
  
  lat_long_list=[]
  value=0
  for key,items in map_package_dict.items():
     print("value now:",value)
     loc1=items[5]
     print("Latitude",items[5],"=",items[11])
     lat=items[11]
     print("Longitude",items[5],"=",items[12])
     long=items[12]
     spotname=items[5].spotname
     lat_long_dict={'spotname':items[5].spotname,'latitude':lat,'longitude':long}
     lat_long_list.append(lat_long_dict)
     print("lspotname",spotname)
     print("listappended",lat_long_dict)
     value=value+1
     if value==3:
        break

  return render(request,"maps.html",{'day_key_value':day_key_value,'choosen_package_dict':choosen_package_dict,'map_package_list':map_package_dict,'user_profile':user_profile,'lat_long_list':lat_long_list})

#accommodation list of a district generation    
@login_required  
def listofaccommodationsview(request,district):
  listoflandscapes=['Beach','Temple','Mosque','Market','Pond','Shopping centre','Park','Museum','Waterfall','Reservoir','Dam','Amusement park','Planetarium','Tourist attractions','Cinema theatre','Bird watching area','Fort','Hill station','Zoo','Garden','Wildlife park','View point','Island','Water bodies','River','Church','Palace','Animal park']
  accommodation_district = district
  user_profile=request.user
  accommodationdetailsdict=dict()
  accommodationdetailslist=Accommodationdetailstable.objects.filter(district=accommodation_district).all()
  number=0
  for accommodationcenter in accommodationdetailslist:
    number=number+1
    accommodationkey="Accommodation"+str(number)
    accommodationdetailstempdict=[
        accommodationcenter.name,                 #0
        accommodationcenter.district,             #1  
        accommodationcenter.location,             #2
        accommodationcenter.lowest_rate,          #3
        accommodationcenter.highest_rate,         #4
        accommodationcenter.accommodation_image1, #5
        accommodationcenter.accommodation_image2, #6
        accommodationcenter.restaurant,           #7
    ]
    accommodationdetailsdict[accommodationkey]=accommodationdetailstempdict
  return render(request,"acco-list.html",{'accommodation_district':accommodation_district,'user_profile':user_profile,'accommodationdetailsdict':accommodationdetailsdict,'listoflandscapes':listoflandscapes,'mainpackagedictcopy':mainpackagedictcopy,'mainpackagedict':mainpackagedict,'choosen_package_dict':choosen_package_dict,})






'''

def createpackageview(request):
   selected_place_from_destinations=Destination.objects.filter(spotdistrict=destination).all()
   if request.method=="POST":
      create_package_selected_list=request.POST.getlist('create_package_selected_list')
      return render(request,"create_package.html",{'day':day,'destination':destination,'create_package_selected_list':create_package_selected_list})
   else:
      return render(request,"create_package.html",{'day':day,'destination':destination,'selected_place_from_destinations':selected_place_from_destinations})


#import json
#from .utils import serialize_destination
#from django.http import JsonResponse
#from django.core.serializers import serialize

#geocoder=Nominatim(user_agent="tpw")
  #gcode=ArcGIS()
  #loc1="Kozhikode Beach"
  #loc2="Thikkodi drive-in beach"
  
  gcode=ArcGIS()
  place_name="Kozhikode Beach"
  place_name_details=gcode.geocode('modinagar')
  print("place_name_details:",place_name_details)
  print("place__details:",gcode.geocode('modinagar'))
  print("place__details_lat:",gcode.geocode(place_name).latitude)
  print("********************************")
  geocoder=Nominatim(user_agent="tpw")
  loc1="Kozhikode Beach"
  loc2="Mananchira Square"
  loc3="mananchira square"
  cordinate1=geocoder.geocode(loc1)
  cordinate2=geocoder.geocode(loc2)
  cordinate3=geocoder.geocode(loc3)
  print("cord1 Koz:",cordinate1)
  print("cord2 Man:",cordinate2)
  print("cord3 man:",cordinate3)
  print("cord1 lat and long KOZ:",cordinate1.latitude,cordinate1.longitude)
  print("cord3 lat and long man:",cordinate3.latitude,cordinate3.longitude)
  print("cord2 lat and long Man:",cordinate2.latitude,cordinate2.longitude)
  lat1,long1=(cordinate1.latitude),(cordinate1.longitude)
  lat2,long2=(cordinate2.latitude),(cordinate2.longitude)
  place1=(lat1,long1)
  place2=(lat2,long2)
  print("distance:",distance.distance(place1,place2))
   #gmap=googlemaps.Client(key=settings.GOOGLE_MAP_API)
   #print("gmap value",gmap)
   #place_name_details=gmap.geocode(place_name)
   #print("place_name_details",place_name_details)



  map_package_dict={
      'spotname':map_package_list
  }

    if day == '1': #day is in string format
        mainpackagedict.clear()
        mainpackagelist=Onedaypackage.objects.filter(district=destination).select_related('spotname').all()
        mainspotnamelist=[]
        for package in mainpackagelist:
          number=str(package.packagenumber)
          count=package.district+number
          print(count,"\n")
          key=count
          packagelist=[package.id,                      #0
                      package.district,                 #1
                      package.packagenumber,            #2
                      package.daynumber,                #3
                      package.spottime,                 #4 
                      package.spotname,                 #5
                      package.spotname.location,        #6
                      package.spotname.landscape,       #7
                      package.spotname.cafespot,        #8
                      package.spotname.description,     #9
                      package.spotname.img              #10
                      ]
          print("packagelist->",packagelist,"\n")
          if key not in mainpackagedict:
            mainpackagedict[key]=[]
          mainpackagedict[key].append(packagelist)

    elif day == '2': #day is in string format
        mainpackagedict.clear()
        mainpackagelist=Twodaypackage.objects.filter(district=destination).select_related('spotname').all()
        mainspotnamelist=[]
        for package in mainpackagelist:
          number=str(package.packagenumber)
          count=package.district+number
          print(count,"\n")
          key=count
          packagelist=[package.id,                      #0
                      package.district,                 #1
                      package.packagenumber,            #2
                      package.daynumber,                #3
                      package.spottime,                 #4 
                      package.spotname,                 #5
                      package.spotname.location,        #6
                      package.spotname.landscape,       #7
                      package.spotname.cafespot,        #8
                      package.spotname.description,     #9
                      package.spotname.img              #10
                      ]
          print("packagelist->",packagelist,"\n")
          if key not in mainpackagedict:
            mainpackagedict[key]=[]
          mainpackagedict[key].append(packagelist)

    elif day == '5': #day is in string format
        mainpackagedict.clear()
        mainpackagelist=Threedaypackage.objects.filter(district=destination).select_related('spotname').all()
        mainspotnamelist=[]
        for package in mainpackagelist:
          number=str(package.packagenumber)
          count=package.district+number
          print(count,"\n")
          key=count
          packagelist=[package.id,                      #0
                      package.district,                 #1
                      package.packagenumber,            #2
                      package.daynumber,                #3
                      package.spottime,                 #4 
                      package.spotname,                 #5
                      package.spotname.location,        #6
                      package.spotname.landscape,       #7
                      package.spotname.cafespot,        #8
                      package.spotname.description,     #9
                      package.spotname.img              #10
                      ]
          print("packagelist->",packagelist,"\n")
          if key not in mainpackagedict:
            mainpackagedict[key]=[]
          mainpackagedict[key].append(packagelist)

    
    elif day == '7': #day is in string format
        mainpackagedict.clear()
        mainpackagelist=Sevendaypackage.objects.filter(district=destination).select_related('spotname').all()
        mainspotnamelist=[]
        for package in mainpackagelist:
          number=str(package.packagenumber)
          count=package.district+number
          print(count,"\n")
          key=count
          packagelist=[package.id,                      #0
                      package.district,                 #1
                      package.packagenumber,            #2
                      package.daynumber,                #3
                      package.spottime,                 #4 
                      package.spotname,                 #5
                      package.spotname.location,        #6
                      package.spotname.landscape,       #7
                      package.spotname.cafespot,        #8
                      package.spotname.description,     #9
                      package.spotname.img              #10
                      ]
          print("packagelist->",packagelist,"\n")
          if key not in mainpackagedict:
            mainpackagedict[key]=[]
          mainpackagedict[key].append(packagelist)
    
    '''