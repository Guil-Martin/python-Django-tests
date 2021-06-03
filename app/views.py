from django.shortcuts import render, redirect
from .models import Student

from django.contrib.auth import authenticate, login

# Create your views here.

def login_page(request):
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

    return render(request, "login_register.html")
    
def index(request):
    obj=Student.objects.all()
    context={
        "obj": obj,
    }
    return render(request, "index.html", context)