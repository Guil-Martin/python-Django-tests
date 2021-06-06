from django.urls import path
from .views import (
    home,
    SaleListView
) 

app_name = 'sales'

urlpatterns = [
    path('', home, name='home'),
    path('list/', SaleListView.as_view(), name='list'),
]