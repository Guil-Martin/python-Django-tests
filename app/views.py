from django.db import reset_queries
from django.shortcuts import render, redirect
from rest_framework.serializers import Serializer
from .models import Student

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Third party imports
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
##

from .forms import CustomUserCreationForm

# API
from .serializer import StudentSerializer
from .models import Student

# Studens
class TestView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        qs = Student.objects.all()
        student = qs.first() # Get first element of student
        serializer = StudentSerializer(qs, many=True)
        # To return only one student :
        # serializer = StudentSerializer(student)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid(): # check if format of data is valid else return error as json
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

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
    qs=Student.objects.all()
    context = {"students": qs, 'title': title}
    return render(request, "index.html", context)


# def test_view(request):
#     data = {
#         'name':'jean',
#         'age':34
#     }
#     return JsonResponse(data)