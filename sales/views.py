from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Sale, Position, CSV
from .forms import SalesSearchForm
from reports.forms import ReportForm
from .utils import get_customer_from_id, get_salesman_from_id, get_chart
from profiles.models import Profile
from products.models import Product
from customers.models import Customer
import pandas as pd

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import csv
from django.utils.dateparse import parse_date

@login_required
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


class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sales/main.html'

    # "object_list" by default
    context_object_name = "sales"

# Equivalent in function :
# def sale_list_view(request):
#     qs = Sale.objects.all()
#     return render(request, 'sales/main.html', {'sales':qs})

class SaleDetailView(LoginRequiredMixin, DetailView):
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

class UploadTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'sales/from_file.html'

@login_required
def csv_upload_view(request):
    if request.method == "POST":
        csv_file_name = request.FILES.get('file').name
        csv_file = request.FILES.get('file')

        # Prevent a file that has the same name from uploading again
        obj, created = CSV.objects.get_or_create(file_name=csv_file_name)

        if created:
            obj.csv_file = csv_file
            obj.save()
            with open(obj.csv_file.path, 'r') as f:
                reader = csv.reader(f)
                reader.__next__()
                for row in reader:
                    # print(row)
                    # data = "".join(row)
                    # data = data.split(',')
                    # print(data)
                    # data.pop()
                    # print(row)
                    
                    transaction = row[0]
                    product = row[1]
                    quantity = int(row[2])
                    customer = row[3]
                    date = parse_date(row[4])

                    print("##################")
                    print(transaction)
                    print(product)
                    print(quantity)
                    print(customer)
                    print(date)
                    print("##################")

                    try:
                        product_obj = Product.objects.get(name__iexact=product)
                    except Product.DoesNotExist:
                        product_obj = None

                    if product_obj is not None:
                        # _ in the bool that says if the object has been created or not
                        customer_obj, _ = Customer.objects.get_or_create(name=customer)
                        salesman_obj = Profile.objects.get(user=request.user)
                        position_obj = Position.objects.create(product=product_obj, quantity=quantity, created=date)

                        sale_obj, _ = Sale.objects.get_or_create(
                                    transaction=transaction, 
                                    customer=customer_obj, 
                                    salesman=salesman_obj, 
                                    created=date)
                        sale_obj.positions.add(position_obj)
                        sale_obj.save()

        # to be sent to upload.js for the alert box
        return JsonResponse({'ex': created})

    return HttpResponse()