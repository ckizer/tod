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
        create_game_href = doc.find(id="index_create_game").find("a")["href"]
        test_href = "/game/create/"
        self.failUnlessEqual(create_game_href, test_href, "Could not find create game link on the home page (%s != %s)" % (create_game_href, test_href))
        response = self.client.get(create_game_href)

        # see a login page, but realize she doesn't have an account, so she clicks the register link
        self.assertRedirects(response, "/accounts/login/?next=%s" % create_game_href, status_code=302, target_status_code=200)
        response = self.client.get("/accounts/login/")
        self.assertContains(response, "/accounts/register/")

        # click register before filling out any info, cause she's so excited
        response = self.client.get("/accounts/register/")
        doc = BeautifulSoup(response.content)
        register_div = doc.find(id="register")
        self.failUnless(register_div, "Could not find the register form.")
        for input in [input for input in register_div.findAll("input") if input.get("name", None)]:
            self.failUnless(input["name"] in ["username", "password"])
        response = self.client.post("/accounts/register/")
        self.assertFormError(response, "registration_form", "username", "This field is required.")
        self.assertFormError(response, "registration_form", "password", "This field is required.")
        # fill out valid info and see the create game page
        self.client.post("/accounts/register/", {'username': 'peter', 'password': 'test'})
        # fill out laura, but realize that name is taken because the error tells her so
        response = self.client.post("/accounts/register/", {'username': 'peter', 'password': 'test'})
        self.assertFormError(response, "registration_form", "username", "That username is taken.  Please choose a different one.")
