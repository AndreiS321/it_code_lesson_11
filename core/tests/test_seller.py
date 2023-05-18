from bs4 import BeautifulSoup
from django.test import TestCase, Client
from django.urls import reverse

from core import factories, models


class SellerTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_list(self):
        seller = factories.SellerFactory()
        resp = self.client.get(reverse("core:sellers_list"))
        self.assertEqual(resp.status_code, 200)
        bs = BeautifulSoup(resp.content, "html.parser")
        self.assertListEqual(bs.tbody.tr.text.split(), ['1', seller.name, "Обновить", "Удалить"])

    def test_create(self):
        seller = factories.SellerFactory.build()
        resp = self.client.post(reverse("core:sellers_create"), {"name": seller.name}, follow=True)
        self.assertEqual(resp.status_code, 200)
        seller_db = models.Seller.objects.first()
        self.assertEqual(seller_db.name, seller.name)

    def test_update(self):
        seller = factories.SellerFactory()
        new_name = "Иван123"
        resp = self.client.post(reverse("core:sellers_update", args=(seller.pk,)), {"name": new_name}, follow=True)
        self.assertEqual(resp.status_code, 200)
        seller_db = models.Seller.objects.first()
        self.assertEqual(seller_db.name, new_name)

    def test_delete(self):
        seller = factories.SellerFactory()
        resp = self.client.post(reverse("core:sellers_del", args=(seller.pk,)), follow=True)
        self.assertEqual(resp.status_code, 200)
        seller_db = models.Seller.objects.first()
        self.assertEqual(seller_db, None)
