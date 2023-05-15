from django.urls import path

import core.views

urlpatterns = [
    path("", core.views.index, name="index"),
    path("index", core.views.index, name="index"),

    path("customers/functional", core.views.customers, name="customers_func"),
    path("customers/class", core.views.CustomerList.as_view(), name="customers_class"),
    path("customers/create", core.views.CustomerCreate.as_view(), name="customers_create"),
    path("customers/update/<int:pk>", core.views.CustomerUpdate.as_view(), name="customers_update", ),
    path("customers/del/<int:pk>", core.views.CustomerDelete.as_view(), name="customers_del", ),

    path("sellers/functional", core.views.sellers, name="sellers_func"),
    path("sellers/class", core.views.SellerList.as_view(), name="sellers_class"),
    path("sellers/create", core.views.SellerCreate.as_view(), name="sellers_create"),
    path("sellers/update/<int:pk>", core.views.SellerUpdate.as_view(), name="sellers_update", ),
    path("sellers/del/<int:pk>", core.views.SellerDelete.as_view(), name="sellers_del"),

    path("items/functional", core.views.items, name="items_func"),
    path("items/class", core.views.ItemList.as_view(), name="items_class"),
    path("items/create", core.views.ItemCreate.as_view(), name="items_create"),
    path("items/update/<int:pk>", core.views.ItemUpdate.as_view(), name="items_update"),
    path("items/del/<int:pk>", core.views.ItemDelete.as_view(), name="items_del"),

    path("orders/functional", core.views.orders, name="orders_func"),
    path("orders/class", core.views.OrderList.as_view(), name="orders_class"),
    path("orders/create", core.views.OrderCreate.as_view(), name="orders_create"),
    path("orders/update/<int:pk>", core.views.OrderUpdate.as_view(), name="orders_update"),
    path("orders/del/<int:pk>", core.views.OrderDelete.as_view(), name="orders_del"),
]
