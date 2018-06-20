from django.test import TestCase
from .models import Book, Author
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from decimal import Decimal

class StoreViewsTestCase(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(
      username='Adam',
      email='email@email.com',
      password='password',
    )
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

  def test_add_to_cart(self):
    self.logged_in = self.client.login(username='Adam', password='password')
    self.assertTrue(self.logged_in)
    self.client.get('/store/add/1/')
    resp = self.client.get('/store/cart/')
    self.assertEqual(resp.context['total'], Decimal('42.00'))
    self.assertEqual(resp.context['count'], 1)
    self.assertEqual(resp.context['cart'].count(), 1)
    self.assertEqual(resp.context['cart'].get().quantity, 1)
