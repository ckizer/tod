from django.test import TestCase
from django.test.client import Client
from django.db import IntegrityError
from django.contrib.auth.models import User

from tod.prompt.models import Prompt

class PromptTest(TestCase):
    def setUp(self):
        self.data = [
            {},
            {
                'name': 'Test Dare',
                'truth': 'Tell something embarassing',
                'dare': 'do something embarassing',
                'difficulty': 5,
            },
            {
                'name': 'Test Dare',
                'truth': 'Tell something embarassing',
                'dare': 'do something embarassing',
                'difficulty': 5,
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

    def test_create_maximal(self):
        datum = self.data[2]
        prompt = Prompt(**datum)
        prompt.save()
        self.failUnlessEqual(prompt.name, datum['name'])
        self.failUnlessEqual(prompt.truth, datum['truth'])
        self.failUnlessEqual(prompt.dare, datum['dare'])
        self.failUnlessEqual(prompt.difficulty, datum['difficulty'])
