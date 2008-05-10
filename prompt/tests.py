from django.test import TestCase
from django.test.client import Client
from django.db import IntegrityError
from django.contrib.auth.models import User

from tod.prompt.models import Prompt

class PromptTest(TestCase):
    def setUp(self):
        self.laura = User.objects.create_user(username="laura", password="laura", email="laura.m.madsen@gmail.com")
        self.data = [
            {},
            {
                'name': 'Test Dare',
                'truth': 'Tell something embarassing',
                'dare': 'do something embarassing',
                'difficulty': 5,
                'owner': self.laura,
            },
            {
                'name': 'Test Dare',
                'truth': 'Tell something embarassing',
                'dare': 'do something embarassing',
                'difficulty': 5,
                'owner': self.laura,
            },
            ]

    def test_create_blank(self):
        datum = self.data[0]
        prompt= Prompt(**datum)
        self.assertRaises(IntegrityError, prompt.save) 

    def test_create_minimal(self):
        datum = self.data[1]
        prompt = Prompt(**datum)
        prompt.save()
        
        self.failUnlessEqual(prompt.name, datum['name'])
        self.failUnlessEqual(prompt.truth, datum['truth'])
        self.failUnlessEqual(prompt.dare, datum['dare'])
        self.failUnlessEqual(prompt.difficulty, datum['difficulty'])
        self.failUnlessEqual(prompt.owner, datum['owner'])


    def test_create_maximal(self):
        datum = self.data[2]
        prompt = Prompt(**datum)
        prompt.save()
        self.failUnlessEqual(prompt.name, datum['name'])
        self.failUnlessEqual(prompt.truth, datum['truth'])
        self.failUnlessEqual(prompt.dare, datum['dare'])
        self.failUnlessEqual(prompt.difficulty, datum['difficulty'])

class PromptViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.laura = User.objects.create_user(username="Laura", password="laura", email="laura.m.madsen@gmail.com")
        self.prompt = Prompt.objects.create(name="Test Dare", truth="Tell something embarassing", dare="Do something embarassing", difficulty=5, owner=self.laura)
        self.urls = {
            '/prompt/': 200,
            }
    
    def test_unauthenticated(self):
        for url, status_code in self.urls.items():
            response = self.client.get(url)
            self.assertRedirects(response, 'http://testserver/accounts/login/?next='+url, status_code=302, target_status_code=200)

    def test_authenticated(self):
        self.client.login(username="Laura", password="laura")
        for url, status_code in self.urls.items():
            response = self.client.get(url)
            self.failUnlessEqual(response.status_code, status_code)
