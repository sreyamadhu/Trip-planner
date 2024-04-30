from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from . models import CustomUser

#user signup
def signupview(request):
  if request.method=='POST':
    username=request.POST['username']
    email=request.POST['email']
    password1=request.POST['password']
    password2=request.POST['confirmpassword']

    if username=="" or email=="" or password1=="" or password2=="":
        print('columns can;t be empty')
        messages.error(request,"Columns can't be empty")
        return redirect("/")
    if password1==password2:
      if CustomUser.objects.filter(username=username).exists():
        print('user name exist already')
        messages.error(request,"Username exist")
        return redirect("/")
      else:
        if CustomUser.objects.filter(email=email).exists():
          print('email exist already')
          messages.error(request,"Email exist")
          return redirect("/")
        else:
          user=CustomUser.objects.create_user(username=username,password=password1,email=email)
          user.save()
          print('user created')
          messages.success(request,"Account created")
          return redirect("login")
    else:
      messages.error(request,"Password not matching")
      print("password not matching")
      return redirect("/")
    
  else:
    user_django_messages = messages.get_messages(request)
    return render(request,"signup.html",{'user_django_messages': user_django_messages})
  
#user login
def loginview(request):
  if request.method=='POST':
    username=request.POST["username"]
    password=request.POST["password"]
    if username==""  or password=="" :
        print('columns can;t be empty')
        messages.error(request, 'Invalid credentials')
        return redirect('login')
    user=auth.authenticate(username=username,password=password)
    if user is not None:
      auth.login(request,user)
      if request.user.is_authenticated and request.user.is_accommodation:
        print("accommodation user logged in")
        return redirect('/accommodations')
      else:
        print("regular user logged in")
        messages.success(request,"")
        return redirect('/packages')
    else:
      print("invalid credentials")
      messages.error(request, 'Invalid credentials')
      return redirect('login')
    
  else:
    user_django_messages = messages.get_messages(request)
    print('user_django_messages:',user_django_messages)
    return render(request,"login.html",{'user_django_messages': user_django_messages})

#user profile updation function
def profileupdationview(request):
  user_profile=request.user
  if request.method=="POST" and 'updateprofile' in request.POST: 
    username = request.POST.get('username')
    email = request.POST.get('email')
    first_name = request.POST.get('firstname')
    last_name = request.POST.get('lastname')
    user_image = request.FILES.get('userimage')

    if username:
      if CustomUser.objects.exclude(id=user_profile.id).filter(username=username).exists():
            messages.error(request, "Username already exists.")
            user_profile_updation_django_messages = messages.get_messages(request)
            return render(request,"pages-profile-update.html",
            {'user_profile':user_profile,'user_profile_updation_django_messages':user_profile_updation_django_messages})
      else:
                user_profile.username = username

    if email:
        if CustomUser.objects.exclude(id=user_profile.id).filter(email=email).exists():
          messages.error(request, "Email already exists.")
          user_profile_updation_django_messages = messages.get_messages(request)
          return render(request,"pages-profile-update.html",
            {'user_profile':user_profile,'user_profile_updation_django_messages':user_profile_updation_django_messages})
        else:
          user_profile.email = email

    if first_name:
      user_profile.first_name = first_name

    if last_name:
      user_profile.last_name = last_name

    if user_image:
      user_profile.user_image = user_image

    user_profile.save()
    print("profile updated succcesfully")
    user_profile=request.user
    return render(request,'pages-profile.html',{'user_profile':user_profile})
  else:
    return render(request,"pages-profile-update.html",{'user_profile':user_profile})


# Create your views here.
'''
def index(request):
  if request.method=="POST":
    if 'login' in request.POST:
      return loginview(request)
    elif 'signup' in request.POST:
      return signupview(request)
  else:
    django_messages = messages.get_messages(request)
    return render(request,"index.html", {'django_messages': django_messages})
'''