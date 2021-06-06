from django.shortcuts import render
from django.views.generic import ListView
from .models import Sale

# Create your views here.
def home(request):
    return render(request, 'sales/home.html', {})


class SaleListView(ListView):
    model = Sale
    template_name = 'sales/main.html'
    
    # "object_list" by default
    context_object_name = "Sales"