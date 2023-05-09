from django.urls import path

import core.views

urlpatterns = [
    path("index", core.views.index, name="index"),
    path("customers/functional", core.views.customers, name="customers_func"),
    path("customers/class", core.views.CustomerList.as_view(), name="customers_class"),
    path("sellers/functional", core.views.sellers, name="sellers_func"),
    path("sellers/class", core.views.SellerList.as_view(), name="sellers_class"),
    path("items/functional", core.views.items, name="items_func"),
    path("items/class", core.views.ItemList.as_view(), name="items_class"),
    path("orders/functional", core.views.orders, name="orders_func"),
    path("orders/class", core.views.OrderList.as_view(), name="orders_class"),
]
