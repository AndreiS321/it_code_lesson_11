from bs4 import BeautifulSoup
from django.test import TestCase, Client
from django.urls import reverse

from core import factories, models


class ItemTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_list(self):
        factories.ItemFactory.create()
        resp = self.client.get(reverse("core:items_list"))
        self.assertEqual(resp.status_code, 200)
        item_db = models.Item.objects.first()
        bs = BeautifulSoup(resp.content, "html.parser")
        self.assertListEqual(bs.tbody.tr.text.split(),
                             ['1', item_db.name, str(item_db.price), item_db.currency, item_db.seller.name, "Обновить",
                              "Удалить"])

    def test_create(self):
        seller = factories.SellerFactory()
        item = factories.ItemFactory.build(seller=seller)
        resp = self.client.post(reverse("core:items_create"),
                                {"name": item.name, "price": item.price, "currency": item.currency,
                                 "seller": seller.pk}, follow=True)
        self.assertEqual(resp.status_code, 200)
        item_db = models.Item.objects.first()
        self.assertListEqual([item_db.name, item_db.price, item_db.currency, item_db.seller.name],
                             [item.name, item.price, item.currency, item.seller.name])

    def test_update(self):
        item = factories.ItemFactory()
        new_name = "Товар123"
        new_price = 321.54
        resp = self.client.post(reverse("core:items_update", args=(item.pk,)),
                                {"name": new_name, "price": new_price, "currency": item.currency,
                                 "seller": item.seller.pk},
                                follow=True)
        self.assertEqual(resp.status_code, 200)
        item_db = models.Item.objects.first()
        self.assertListEqual([item_db.name, item_db.price, item_db.currency, item_db.seller.name],
                             [new_name, new_price, item.currency, item.seller.name])

    def test_delete(self):
        item = factories.ItemFactory()
        resp = self.client.post(reverse("core:items_del", args=(item.pk,)), follow=True)
        self.assertEqual(resp.status_code, 200)
        item_db = models.Item.objects.first()
        self.assertEqual(item_db, None)
