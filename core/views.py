from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core import forms, models


# Create your views here.


def index(request):
    return render(request, template_name="index.html")


class CustomerList(ListView):
    model = models.Customer
    template_name = "customer/customers_list.html"

    def get_queryset(self):
        name = self.request.GET.get("name")
        if name:
            return self.model.objects.filter(name__icontains=name).all()
        return self.model.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = forms.CustomerSearch(self.request.GET or None)
        context["table_title"] = "Покупатели"
        context["table_headers"] = ("№", "Имя")
        return context


class SellerList(ListView):
    model = models.Seller
    template_name = "seller/sellers_list.html"

    def get_queryset(self):
        name = self.request.GET.get("name")
        if name:
            return self.model.objects.filter(name__icontains=name).all()
        return self.model.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = forms.SellerSearch(self.request.GET or None)
        context["table_title"] = "Продавцы"
        context["table_headers"] = ("№", "Имя")
        return context


class ItemList(ListView):
    model = models.Item
    template_name = "item/items_list.html"

    def get_queryset(self):
        name = self.request.GET.get("name")
        price = self.request.GET.get("price")
        currency = self.request.GET.get("currency")
        seller = self.request.GET.get("seller")
        filters = {
            "name__icontains": name,
            "price__gte": price,
            "currency": currency,
            "seller": seller,
        }
        filters = {key: value for key, value in filters.items() if value}
        queryset = self.model.objects.all()
        if filters:
            return queryset.filter(**filters)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = forms.ItemSearch(self.request.GET or None)
        context["table_title"] = "Товары"
        context["table_headers"] = ("№", "Название",
                                    "Стоимость", "Валюта",
                                    "Продавец")
        return context


class OrderList(ListView):
    model = models.Order
    template_name = "order/orders_list.html"

    def get_queryset(self):
        customer = self.request.GET.get("name")
        items = self.request.GET.get("items")
        finished = self.request.GET.get("finished")
        filters = {
            "customer": customer,
            "items": items,
            "finished": bool(finished),
        }
        filters = {key: value for key, value in filters.items() if value}
        queryset = self.model.objects.all()
        if filters:
            return queryset.filter(**filters)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = forms.OrderSearch(self.request.GET or None)
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
    model = models.Customer
    template_name = "customer/customer_add.html"
    form_class = forms.CustomerForm
    success_url = reverse_lazy("core:customers_list")


class CustomerUpdate(UpdateView):
    model = models.Customer
    template_name = "customer/customer_update.html"
    form_class = forms.CustomerForm
    success_url = reverse_lazy("core:customers_list")


class CustomerDelete(DeleteView):
    model = models.Customer
    template_name = "customer/customer_delete.html"
    success_url = reverse_lazy("core:customers_list")


class SellerCreate(CreateView):
    model = models.Seller
    template_name = "seller/seller_add.html"
    form_class = forms.SellerForm
    success_url = reverse_lazy("core:sellers_list")


class SellerUpdate(UpdateView):
    model = models.Seller
    template_name = "seller/seller_update.html"
    form_class = forms.SellerForm
    success_url = reverse_lazy("core:sellers_list")


class SellerDelete(DeleteView):
    model = models.Seller
    template_name = "seller/seller_delete.html"
    success_url = reverse_lazy("core:sellers_list")


class ItemCreate(CreateView):
    model = models.Item
    template_name = "item/item_add.html"
    form_class = forms.ItemForm
    success_url = reverse_lazy("core:items_list")


class ItemUpdate(UpdateView):
    model = models.Item
    template_name = "item/item_update.html"
    form_class = forms.ItemForm
    success_url = reverse_lazy("core:items_list")


class ItemDelete(DeleteView):
    model = models.Item
    template_name = "item/item_delete.html"
    success_url = reverse_lazy("core:items_list")


class OrderCreate(CreateView):
    model = models.Order
    template_name = "order/order_add.html"
    form_class = forms.OrderForm
    success_url = reverse_lazy("core:orders_list")


class OrderUpdate(UpdateView):
    model = models.Order
    template_name = "order/order_update.html"
    form_class = forms.OrderForm
    success_url = reverse_lazy("core:orders_list")


class OrderDelete(DeleteView):
    model = models.Order
    template_name = "order/order_delete.html"
    success_url = reverse_lazy("core:orders_list")
