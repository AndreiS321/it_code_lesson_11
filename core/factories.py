import factory
from faker import Factory

from core import models

factory_ru = Factory.create("ru-Ru")


class CustomerFactory(factory.django.DjangoModelFactory):
    name = factory_ru.first_name()

    class Meta:
        model = models.Customer


class SellerFactory(factory.django.DjangoModelFactory):
    name = factory_ru.first_name()

    class Meta:
        model = models.Seller


class ItemFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda x: f"Item{x}")
    price = factory_ru.random_int(min=1)
    currency = factory_ru.random_element(elements=tuple(i for i, _ in models.Item.currency_choices))
    seller = factory.SubFactory(SellerFactory)

    class Meta:
        model = models.Item


class OrderFactory(factory.django.DjangoModelFactory):
    customer = factory.SubFactory(CustomerFactory)
    finished = False

    class Meta:
        model = models.Order

    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for item in extracted:
                self.items.add(item)
