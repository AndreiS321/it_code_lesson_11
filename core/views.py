from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.forms import CustomerForm, SellerForm, ItemForm, OrderForm
from core.models import Customer, Item, Seller, Order


# Create your views here.


def index(request):
    return render(request, template_name="index.html")


def customers(request):
    customers = Customer.objects.all()
    return render(
        request,
        template_name="customer/customers_list.html",
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
        template_name="seller/sellers_list.html",
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
        template_name="item/items_list.html",
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
        template_name="order/orders_list.html",
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
    template_name = "customer/customers_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table_title"] = "Покупатели"
        context["table_headers"] = ("№", "Имя")
        return context


class SellerList(ListView):
    model = Seller
    template_name = "seller/sellers_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table_title"] = "Продавцы"
        context["table_headers"] = ("№", "Имя")
        return context


class ItemList(ListView):
    model = Item
    template_name = "item/items_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table_title"] = "Товары"
        context["table_headers"] = ("№", "Название", "Стоимость", "Валюта", "Продавец")
        return context


class OrderList(ListView):
    model = Order
    template_name = "order/orders_list.html"

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


class CustomerCreate(CreateView):
    model = Customer
    template_name = "customer/customer_add.html"
    form_class = CustomerForm
    success_url = reverse_lazy("customers_class")


class CustomerUpdate(UpdateView):
    model = Customer
    template_name = "customer/customer_update.html"
    form_class = CustomerForm
    success_url = reverse_lazy("customers_class")


class CustomerDelete(DeleteView):
    model = Customer
    template_name = "customer/customer_delete.html"
    success_url = reverse_lazy("customers_class")


class SellerCreate(CreateView):
    model = Seller
    template_name = "seller/seller_add.html"
    form_class = SellerForm
    success_url = reverse_lazy("sellers_class")


class SellerUpdate(UpdateView):
    model = Seller
    template_name = "seller/seller_update.html"
    form_class = SellerForm
    success_url = reverse_lazy("sellers_class")


class SellerDelete(DeleteView):
    model = Seller
    template_name = "seller/seller_delete.html"
    success_url = reverse_lazy("sellers_class")


class ItemCreate(CreateView):
    model = Item
    template_name = "item/item_add.html"
    form_class = ItemForm
    success_url = reverse_lazy("items_class")


class ItemUpdate(UpdateView):
    model = Item
    template_name = "item/item_update.html"
    form_class = ItemForm
    success_url = reverse_lazy("items_class")


class ItemDelete(DeleteView):
    model = Item
    template_name = "item/item_delete.html"
    success_url = reverse_lazy("items_class")


class OrderCreate(CreateView):
    model = Order
    template_name = "order/order_add.html"
    form_class = OrderForm
    success_url = reverse_lazy("orders_class")


class OrderUpdate(UpdateView):
    model = Order
    template_name = "order/order_update.html"
    form_class = OrderForm
    success_url = reverse_lazy("orders_class")


class OrderDelete(DeleteView):
    model = Order
    template_name = "order/order_delete.html"
    success_url = reverse_lazy("orders_class")
