from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from .models import Sale
from .forms import SalesSearchForm


# Create your views here.
def home(request):
    form = SalesSearchForm(request.POST or None)

    if request.method == "POST":
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')

        qs = Sale.objects.filter(created__date=date_from)

    context = {
        'form': form,
    }
    return render(request, 'sales/home.html', context)


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