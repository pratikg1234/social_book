from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='signin')
def index(request):
    # Object of currently logged in user
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user = user_object)
    return render(request,'index.html',{'user_profile':user_profile})

@login_required(login_url='signin')
def upload(request):
    return HttpResponse('<h1> Upload View </h1>')
@login_required(login_url='signin')
def settings(request):
    # getting the currently logged in users profile object
    user_profile = Profile.objects.get(user = request.user)
    
    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        return redirect('settings')
    return render(request, 'setting.html', {'user_profile':user_profile})
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        # User is default django model
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already exists')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username already exists')
                return redirect('signup')
            else:#If everything is correct then storing the credentials to User model by creating new user
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                
                #Log user in and redirect to settings page
                auth.login(request,user_login)
                user_login = auth.authenticate(username=username, password = password)
                #create a profile object for new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user = user_model, id_user = user_model.id)
                new_profile.save()#saving the info to the database
                return redirect('settings')
        else:
            messages.info(request, 'Password Not matching')
            return redirect(signup)
    else:
        return render(request, 'signup.html')
        
        
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username,password=password)
        
        # If user is present in database
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Credentials Invalid')
            return redirect('signin') 
    else:
        return render(request, 'signin.html')
 
@login_required(login_url='signin')   
def logout(request):
    auth.logout(request)
    return redirect('signin')