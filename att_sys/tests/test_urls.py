from django.test import SimpleTestCase
from django.urls import reverse,resolve
from .views import *


class TestUrls (SimpleTestCase):

    def test_list_urls (self):
        att_sys = 'added'
        print(att_sys)
        url = reverse ('index')
        print (resolve (url))
