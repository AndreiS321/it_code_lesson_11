from django.shortcuts import render
from django.views.generic import ListView

from core.models import Customer, Item, Seller, Order


# Create your views here.


def index(request):
    return render(request, template_name="index.html")


def customers(request):
    customers = Customer.objects.all()
    return render(
        request,
        template_name="customers_list.html",
        context={
            "object_list": customers,
            "table_title": "Покупатели",
            "table_headers": ("№", "Имя"),
        },
    )


def sellers(request):
    sellers = Seller.objects.all()
    return render(
        request,
        template_name="sellers_list.html",
        context={
            "object_list": sellers,
            "table_title": "Продавцы",
            "table_headers": ("№", "Имя"),
        },
    )


def items(request):
    items = Item.objects.all()
    return render(
        request,
        template_name="items_list.html",
        context={
            "object_list": items,
            "table_title": "Товары",
            "table_headers": ("№", "Название", "Стоимость", "Валюта", "Продавец"),
        },
    )


def orders(request):
    orders = Order.objects.all()
    all_items = tuple(
        ", ".join(item.name for item in order.items.all()) for order in orders
    )
    return render(
        request,
        template_name="orders_list.html",
        context={
            "object_list": tuple(
                dict(order=order, items=items)
                for order, items in zip(orders, all_items)
            ),
            "table_title": "Заказы",
            "table_headers": ("№", "Покупатель", "Товары", "Дата создания", "Статус"),
        },
    )


class CustomerList(ListView):
    model = Customer
    template_name = "customers_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table_title"] = "Покупатели"
        context["table_headers"] = ("№", "Имя")
        return context


class SellerList(ListView):
    model = Seller
    template_name = "sellers_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table_title"] = "Продавцы"
        context["table_headers"] = ("№", "Имя")
        return context


class ItemList(ListView):
    model = Item
    template_name = "items_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table_title"] = "Товары"
        context["table_headers"] = ("№", "Название", "Стоимость", "Валюта", "Продавец")
        return context


class OrderList(ListView):
    model = Order
    template_name = "orders_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        all_items = tuple(
            ", ".join(item.name for item in order.items.all())
            for order in context["object_list"]
        )
        context["object_list"] = tuple(
            dict(order=order, items=items)
            for order, items in zip(context["object_list"], all_items)
        )
        context["table_title"] = "Заказы"
        context["table_headers"] = (
            "№",
            "Покупатель",
            "Товары",
            "Дата создания",
            "Статус",
        )
        return context
