from django.db import models


class Person(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Seller(Person):
    pass


class Customer(Person):
    pass


class Item(models.Model):
    currency_choices = (
        ("RUB", "Russian Ruble"),
        ("EUR", "Euro"),
        ("USD", "US Dollar"),
    )
    name = models.CharField(max_length=255)
    price = models.FloatField()
    currency = models.CharField(max_length=3, choices=currency_choices)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} for {self.price} {self.currency}, Seller: {self.seller}"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    creation_date = models.DateTimeField(auto_now_add=True)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return f"Customer: {self.customer}, Created: {self.creation_date},Finished: {self.finished}"
