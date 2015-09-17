# coding: utf-8

from unittest import TestCase
import os

from bottle import debug

from webtest import TestApp

from bottle_app import application, DB_PATH
from dbhelper import initialize_database

debug(True)


class LagesonumTests(TestCase):
    def setUp(self):
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        initialize_database(DB_PATH)
        self.app = TestApp(application)

    def test_about(self):
        response = self.app.get('/about')
        self.assertEqual(response.status, '302 Found')
        response = self.app.get('/en_US/about')
        self.assertEqual(response.status, '200 OK')
        self.assertTrue(
            "This website was created by volunteers" in response.body)

    def test_impressum(self):
        response = self.app.get('/impressum')
        self.assertEqual(response.status, '302 Found')
        response = self.app.get('/en_US/impressum')
        self.assertEqual(response.status, '200 OK')
        self.assertTrue(
            "Datenschutzerklärung gem. §13 Telemediengesetz" in response.body)

    def test_redirect(self):
        response = self.app.get('/')
        self.assertEqual(response.status, '302 Found')
        response = self.app.get('/query')
        self.assertEqual(response.status, '302 Found')

    def test_startpage(self):
        response = self.app.get('/en_US/')
        self.assertEqual(response.status, '200 OK')
        self.assertTrue("Please help by typing in all numbers" in response.body)

    def test_querypage(self):
        response = self.app.get('/en_US/query')
        self.assertEqual(response.status, '200 OK')
        self.assertTrue("Search Your Number" in response.body)

    def test_insert(self):
        response = self.app.post('/en_US/', {'numbers': 'A123'})
        self.assertEqual(response.status, '200 OK')
        self.assertTrue("entered" in response.body)
        self.assertTrue("A123" in response.body)

    def test_insert_wrong(self):
        response = self.app.post('/en_US/', {'numbers': '123'})
        self.assertEqual(response.status, '200 OK')
        self.assertTrue("INVALID INPUT" in response.body)

    def test_insert_two(self):
        response = self.app.post('/en_US/', {'numbers': 'A123\nB456'})
        self.assertEqual(response.status, '200 OK')
        self.assertTrue("A123" in response.body)
        self.assertTrue("B456" in response.body)

        # assert self.app.get('/admin').status == '200 OK'        # fetch a page successfully
        # app.reset()                                        # drop the cookie
