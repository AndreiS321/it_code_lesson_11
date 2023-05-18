from bs4 import BeautifulSoup
from django.test import TestCase, Client
from django.urls import reverse

from core import factories, models


class CustomerTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_list(self):
        customer = factories.CustomerFactory()
        resp = self.client.get(reverse("core:customers_list"))
        self.assertEqual(resp.status_code, 200)
        bs = BeautifulSoup(resp.content, "html.parser")
        self.assertListEqual(bs.tbody.tr.text.split(), ['1', customer.name, "Обновить", "Удалить"])

    def test_create(self):
        customer = factories.CustomerFactory.build()
        resp = self.client.post(reverse("core:customers_create"), {"name": customer.name}, follow=True)
        self.assertEqual(resp.status_code, 200)
        customer_db = models.Customer.objects.first()
        self.assertEqual(customer_db.name, customer.name)

    def test_update(self):
        customer = factories.CustomerFactory()
        new_name = "Иван123"
        resp = self.client.post(reverse("core:customers_update", args=(customer.pk,)), {"name": new_name}, follow=True)
        self.assertEqual(resp.status_code, 200)
        customer_db = models.Customer.objects.first()
        self.assertEqual(customer_db.name, new_name)

    def test_delete(self):
        customer = factories.CustomerFactory()
        resp = self.client.post(reverse("core:customers_del", args=(customer.pk,)), follow=True)
        self.assertEqual(resp.status_code, 200)
        customer_db = models.Customer.objects.first()
        self.assertEqual(customer_db, None)
