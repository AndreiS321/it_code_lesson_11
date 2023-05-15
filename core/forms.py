from django import forms

from core import models


class CustomerForm(forms.ModelForm):
    name = forms.CharField(label="Имя")

    class Meta:
        model = models.Customer
        fields = "__all__"


class SellerForm(forms.ModelForm):
    name = forms.CharField(label="Имя")

    class Meta:
        model = models.Seller
        fields = "__all__"


class ItemForm(forms.ModelForm):
    name = forms.CharField(label="Название")
    price = forms.IntegerField(label="Цена", min_value=0)
    currency = forms.ChoiceField(label="Валюта", choices=models.Item.currency_choices)
    seller = forms.ModelChoiceField(
        queryset=models.Seller.objects.all(), label="Продавец"
    )

    class Meta:
        model = models.Item
        fields = "__all__"


class OrderForm(forms.ModelForm):
    customer = forms.ModelChoiceField(
        queryset=models.Customer.objects.all(), label="Покупатель"
    )
    items = forms.ModelMultipleChoiceField(
        queryset=models.Item.objects.all(), label="Товары"
    )
    finished = forms.BooleanField(label="Завершён ли заказ", required=False)

    class Meta:
        model = models.Order
        fields = "__all__"
