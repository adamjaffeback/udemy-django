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

  def test_book_detail(self):
      resp = self.client.get('/store/book/1/')
      self.assertEqual(resp.status_code, 200)
      self.assertEqual(resp.context['book'].pk, 1)
      self.assertEqual(resp.context['book'].title, 'My Life')
      resp = self.client.get('/store/book/2/')
      self.assertEqual(resp.status_code, 404)