from django.shortcuts import render, redirect
from .models import Student

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm

# Create your views here.

def login_user(request):
    page = 'login'
    title = 'Login'
    if request.method == 'POST':
        # Get info from form in templates.login_register.html
        username = request.POST['username']
        password = request.POST['password']

        # Use django authenticate function to ckeck if user exists
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If user exists use django login function
            login(request, user)
            return redirect('index')    # Redirect to the route index by its name 
                                        # return so it dosen't render and don't redirect

    return render(request, "login_register.html", {'page': page, 'title': title})

def logout_user(request):
    logout(request)
    return redirect('login')

def register_user(request):
    page = 'register'
    title = 'Register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # commit to false to be able to save at a later time
            user.save() # Save user in database

            user = authenticate(
                request, username=user.username, password=request.POST['password1'])

            if user is not None:
                # If user exists use django login function
                login(request, user)
                return redirect('index')    # Redirect to the route index by its name 
                                            # return so it dosen't render and don't redirect

    context = {'form': form, 'page': page, 'title': title}
    return render(request, 'login_register.html', context)

# Prevent index to be displayed and redirect to login page by name if a user is not authenticated
@login_required(login_url='login')
def index(request):
    title = 'Index'
    obj=Student.objects.all()
    context = {"obj": obj, 'title': title}
    return render(request, "index.html", context)