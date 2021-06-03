from django.shortcuts import render
from .models import Student

# Create your views here.
def index(request):
    obj=Student.objects.all()
    context={
        "obj": obj,
    }
    return render(request, "index.html", context)