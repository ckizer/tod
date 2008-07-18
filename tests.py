from django.test import TestCase
from django.test.client import Client
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.core import management
from BeautifulSoup import BeautifulSoup


class UserTestCase(TestCase):
    """Tests that users can register, login and logout
    """
    def setUp(self):
        self.client = Client()

    def test_register(self):
        """ Alice is new and wants to play truth or dare.  She doesn't have an account yet
        She should...
        """
        # come to the home page and click teh create a new game link
        response = self.client.get("/")
        doc = BeautifulSoup(response.content)
        self.failUnlessEqual(doc.find(id="index_create_game").find("a")["href"], "/game/create/", "Could not find create game link on the home page")
        # see a login page, but realize she doesn't have an account, so she clicks the register link
        # click register before filling out any info, cause she's so excited
        # fill out laura, but realize that name is taken because the error tells her so
        # fill out alice, but forget to fill out a username
        # fill out valid info and see the create game page
