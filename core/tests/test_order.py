from bs4 import BeautifulSoup
from django.test import TestCase, Client
from django.urls import reverse

from core import factories, models


class OrderTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_list(self):
        factories.OrderFactory.create(
            items=factories.ItemFactory.create_batch(3)
        )
        resp = self.client.get(reverse("core:orders_list"))
        self.assertEqual(resp.status_code, 200)
        order_db = models.Order.objects.first()
        bs = BeautifulSoup(resp.content, "html.parser")
        order_bs = [i.text.strip() for i in bs.tbody.tr if i.text.strip()]
        order_bs.pop(3)
        self.assertListEqual(
            order_bs,
            [
                "1",
                order_db.customer.name,
                ", ".join(item.name for item in order_db.items.all()),
                "Завершён" if order_db.finished else "В процессе",
                "Обновить",
                "Удалить",
            ],
        )

    def test_create(self):
        customer = factories.CustomerFactory.create()
        items = factories.ItemFactory.create_batch(3)

        order = factories.OrderFactory.build(customer=customer, items=items)
        resp = self.client.post(
            reverse("core:orders_create"),
            {
                "customer": order.customer.pk,
                "items": [item.pk for item in items],
                "finished": order.finished,
            },
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        order_db = models.Order.objects.first()
        self.assertListEqual(
            [order.customer.name, [item for item in items], order.finished],
            [
                order_db.customer.name,
                [item for item in order_db.items.all()],
                order_db.finished,
            ],
        )

    def test_update(self):
        order = factories.OrderFactory.create(
            items=factories.ItemFactory.create_batch(3)
        )
        customer_new = factories.CustomerFactory.create(name="Иван123")
        resp = self.client.post(
            reverse("core:orders_update", args=(order.pk,)),
            {
                "customer": customer_new.pk,
                "items": [item.pk for item in order.items.all()],
                "finished": order.finished,
            },
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        order_db = models.Order.objects.first()
        self.assertListEqual(
            [
                order_db.customer.name,
                [item for item in order_db.items.all()],
                order_db.finished,
            ],
            [customer_new.name,
             [item for item in order.items.all()],
             order.finished],
        )

    def test_delete(self):
        order = factories.OrderFactory.create(
            items=factories.ItemFactory.create_batch(3)
        )
        resp = self.client.post(
            reverse("core:orders_del", args=(order.pk,)), follow=True
        )
        self.assertEqual(resp.status_code, 200)
        order_db = models.Order.objects.first()
        self.assertEqual(order_db, None)
