from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.contrib import messages

from user_profile.models import Profile

def home(request):
    if request.user.is_authenticated:
        # If user is logged in, redirect to recipes page
        return redirect('recipe:view_recipes')
    else:
        # If user is not logged in, show the home page
        return render(request, 'main/home.html', {
            'title': 'Home'
        })

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            # A backend authenticated the credentials.
            auth.login(request, user)
            messages.success(request, 'Login Successful. Welcome back!')
            print('Login Successful. Welcome back!')
            return redirect('recipe:view_recipes')
        else:
            # No backend authenticated the credentials.
            messages.error(request, 'User does not exist. Please check your username and password!')
            print('User does not exist. Please check your password and username!')
            return redirect('recipe:signin')

    return render(request, 'main/signin.html', {
        'title': "Signin"
    })

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.warning(request, 'The Email already exist')
                print("The Email already exist")
                return redirect('main:signup')
            elif User.objects.filter(username=username).exists():
                messages.warning(request, 'The Username already taken')
                print("The Username already taken")
                return redirect('main:signup')
            else: 
                #Create the user
                new_user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                new_user.save()
                #Log the user using credentials.
                user_credentials = auth.authenticate(username=username, password=password)
                auth.login(request, user_credentials)
                #Create a Profile for the new user
                get_new_user = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=get_new_user)
                new_profile.save()
                #Redirect the user.
                messages.success(request, 'Account created successfully. Welcome to Community!')
                print("Account created successfully. Welcome to Community!")
                return redirect('recipe:view_recipes')
        else:
            messages.error(request, "The password don't match.")
            print("The password don't match")
            return redirect('main:signup')
    return render(request, 'main/signup.html', {
        'title': "Signup"
    })

def signout(request):
    auth.logout(request)
    messages.success(request, 'Logout Successful. Have a nice day!')
    print("Logout Successful. Have a nice day!")
    return redirect('main:signin')