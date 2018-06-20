from django.test import TestCase
from .models import Book, Author
from django.core.urlresolvers import reverse


class StoreViewsTestCase(TestCase):
  def setUp(self):
    author = Author.objects.create(first_name='Adam', last_name='JB')
    book = Book.objects.create(
      title='My Life',
      author=author,
      description='Something',
      price=42,
      stock=1
    )

  def test_index(self):
    resp = self.client.get('/store/')
    self.assertEqual(resp.status_code, 200)
    self.assertTrue('books' in resp.context)
    self.assertTrue(resp.context['books'].count() > 0)

  def test_cart(self):
    resp = self.client.get('/store/cart/')
    self.assertEqual(resp.status_code, 302)
