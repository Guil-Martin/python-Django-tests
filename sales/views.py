from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from .models import Sale

# Create your views here.
def home(request):
    return render(request, 'sales/home.html', {})


class SaleListView(ListView):
    model = Sale
    template_name = 'sales/main.html'

    # "object_list" by default
    context_object_name = "sales"

# Equivalent in function :
# def sale_list_view(request):
#     qs = Sale.objects.all()
#     return render(request, 'sales/main.html', {'sales':qs})

class SaleDetailView(DetailView):
    model = Sale
    template_name = 'sales/detail.html'

    # "object" by default
    context_object_name = "sale" 

# Equivalent in function :
# def sale_detail_view(request, pk):
#     sale = Sale.objects.get(pk=pk)
#               or
#     sale = get_object_or_404(Sale, pk=pk)
#     return render(request, 'sales/detail.html', {'sale':sale})