from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from .models import Sale
from .forms import SalesSearchForm
from reports.forms import ReportForm
from .utils import get_customer_from_id, get_salesman_from_id, get_chart
import pandas as pd


# Create your views here.
def home(request):
    search_form = SalesSearchForm(request.POST or None)
    report_form = ReportForm()
    sales_df = None
    positions_df = None
    merged_df = None
    df = None
    chart = None
    sales = None    
    no_data = None

    if request.method == "POST":
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        results_by = request.POST.get('results_by')
        
        sales = Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from)
        if len(sales) > 0:
            sales_df = pd.DataFrame(sales.values()) # Dictionnary
                     # pd.DataFrame(sales.values_list()) # Tuples
            sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id)
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_salesman_from_id)
            sales_df['created'] = sales_df['created'].apply(lambda x: x.strftime('%Y-%m-%d'))
            sales_df.rename({   'id': 'sales_id', 
                                'customer_id': 'Customer', 
                                'salesman_id': 'Salesman'}, 
                                axis=1, inplace=True)

            position_data = []
            for sale in sales:
                for pos in sale.get_positions():
                    obj = {
                        'position_id': pos.id,
                        'product': pos.product,
                        'quantity': pos.quantity,
                        'price': pos.price,
                        'sales_id': pos.get_sales_id(),
                    }
                    position_data.append(obj)

            positions_df = pd.DataFrame(position_data)
            merged_df = pd.merge(sales_df, positions_df, on='sales_id') 
            # "on" option needs to be the same key name for both the dataframes!

            df = merged_df.groupby('transaction', as_index=False)['price'].agg('sum')

            chart = get_chart(chart_type, sales_df, results_by)

            sales_df = sales_df.to_html()
            positions_df = positions_df.to_html()
            merged_df = merged_df.to_html()
            df = df.to_html()

        else:
            no_data = "No data is available in this date range"

    context = {
        'search_form': search_form,
        'report_form': report_form,
        'sales_df': sales_df,
        'positions_df': positions_df,
        'merged_df': merged_df,
        'df': df,
        'chart': chart,
        'sales': sales,
        'no_data': no_data,
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