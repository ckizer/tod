from django.test import TestCase
from django.test.client import Client
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.core import management
from BeautifulSoup import BeautifulSoup

from tod.prompt.models import Prompt
from tod.prompt.forms import PromptForm

class PromptTest(TestCase):
    """Tests the creation of the prompt objects
    """
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
        """Tests the creation of a prompt with no input
        """
        datum = self.data[0]
        prompt= Prompt(**datum)
        self.assertRaises(IntegrityError, prompt.save) 

    def test_create_minimal(self):
        """Tests the creation of a prompt with minimum input
        """
        datum = self.data[1]
        prompt = Prompt(**datum)
        prompt.save()
        
        self.failUnlessEqual(prompt.name, datum['name'])
        self.failUnlessEqual(prompt.truth, datum['truth'])
        self.failUnlessEqual(prompt.dare, datum['dare'])
        self.failUnlessEqual(prompt.difficulty, datum['difficulty'])
        self.failUnlessEqual(prompt.owner, datum['owner'])


    def test_create_maximal(self):
        """Tests the creation of a prompt with maximum input

        TODO - (defer) add tags to the creation of the prompt
        """
        datum = self.data[2]
        prompt = Prompt(**datum)
        prompt.save()
        self.failUnlessEqual(prompt.name, datum['name'])
        self.failUnlessEqual(prompt.truth, datum['truth'])
        self.failUnlessEqual(prompt.dare, datum['dare'])
        self.failUnlessEqual(prompt.difficulty, datum['difficulty'])

class PromptViewTest(TestCase):
    """Tests that prompt functionality is accessible from http
    """

    fixtures = ["prompt_view"]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username="laura")
        self.client.login(username="laura", password='laura')

    def test_viewPromptIndex(self):
        """User goes to the prompt index. They should...
        """
        # See a list of prompts
        response = self.client.get('/prompt/')
        self.assertTemplateUsed(response, 'prompt/index.html')
        self.assertContains(response, 'prompt_list')
        # See the name of a prompt in the list
        self.assertContains(response, 'one')

    def test_promptDelete(self):
        prompt=Prompt.objects.get()
        self.failUnlessEqual(Prompt.objects.count(), 1)
        response = self.client.post(prompt.get_absolute_url()+'delete/')
        self.failUnlessEqual(Prompt.objects.count(), 0)

    def test_promptForm(self):
        """Tests that the prompt detail returns the prompt form
        """
        response = self.client.get('/prompt/create/')
        self.assertContains(response, "Name:")
        self.assertContains(response, "Dare:")
        self.assertContains(response, "Truth:")
        self.assertContains(response, "Difficulty:")
        self.assertTemplateUsed(response, "prompt/prompt_detail.html")

    def test_promptCreate(self):
        """Tests that a post in the prompt form creates a prompt object
        """
        response = self.client.post('/prompt/create/', {'name': 'TestName', 'truth': 'TestTruth', 'dare': 'TestDare', 'difficulty': 1})
        prompt = Prompt.objects.get(name = "TestName")
        self.failUnlessEqual(prompt.truth, "TestTruth")
        self.failUnlessEqual(prompt.dare, "TestDare")
        self.failUnlessEqual(prompt.difficulty, 1)

    def test_promptOwnerFilter(self):
        """Tests that a user's prompt list displays public prompts and only that user's private prompts
        """
        management.call_command('loaddata', 'all_difficulties.json', verbosity=0)
        self.failUnlessEqual(Prompt.objects.count(), 16)
        response = self.client.get('/prompt/')
        prompts = response.context[0].get('prompts')
        self.failUnlessEqual(len(prompts), 14)
        self.assertTemplateUsed(response, 'prompt/index.html')

class PromptFormTest(TestCase):
    """Tests that the prompt form correctly handles user inputs
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username="laura")
        self.client.login(username="laura", password='laura')
    
    fixtures = ["prompt_view"]

    def test_promptUniqueName(self):
        """Tests that making two prompts with different names does not give an error
        """
        form = PromptForm({'name': 'TestName', 'truth': 'TestTruth', 'dare': 'TestDare', 'difficulty': 1}, owner=self.user)
        if form.is_valid():
            current_prompt=form.save()
        prompt = Prompt.objects.get(name = "TestName")
        self.failUnlessEqual(prompt.truth, "TestTruth")
        self.failUnlessEqual(prompt.dare, "TestDare")
        self.failUnlessEqual(prompt.difficulty, 1)
        form = PromptForm({'name': 'TestName2', 'truth': 'TestTruth', 'dare': 'TestDare', 'difficulty': 1}, owner=self.user)
        if form.is_valid():
            current_prompt=form.save()
        prompt = Prompt.objects.get(name = "TestName2")
        self.failUnlessEqual(prompt.truth, "TestTruth")
        self.failUnlessEqual(prompt.dare, "TestDare")
        self.failUnlessEqual(prompt.difficulty, 1)

    def test_promptDuplicateName(self):
        """Tests that making two prompts with the same name gives an error
        """
        form = PromptForm({'name': 'TestName', 'truth': 'TestTruth', 'dare': 'TestDare', 'difficulty': 1}, owner=self.user)
        if form.is_valid():
            current_prompt=form.save(commit=False)
            current_prompt.owner=self.user
            current_prompt.save()
        prompt = Prompt.objects.get(name = "TestName")
        self.failUnlessEqual(prompt.truth, "TestTruth")
        self.failUnlessEqual(prompt.dare, "TestDare")
        self.failUnlessEqual(prompt.difficulty, 1)
        form = PromptForm({'name': 'TestName', 'truth': 'TestTruth', 'dare': 'TestDare', 'difficulty': 1}, owner=self.user)
        if form.is_valid():
            self.assertRaises(forms.ValidationError, form.save)
        

class ImmutablePromptTest(TestCase):
    """Tests that users can only delete their own prompts
    """
    fixtures = ['all_difficulties']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username="laura")
        self.client.login(username="laura", password='laura')

    def test_appropriateDeleteButtons(self):
        """Tests that user only sees delete buttons next to their own prompts
        """
        #Get list of prompts from the database
        prompts = Prompt.objects.exclude(private=True) | Prompt.objects.filter(owner=self.user)
        #Get list of prompt rows from the page
        response = self.client.get('/prompt/')
        doc = BeautifulSoup(response.content)

        prompt_rows = doc.find(id = "prompt_list").findAll("li")
        #Loop over the zipped prompts and prompt rows
        self.failUnlessEqual(prompts.count(), len(prompt_rows))
        for prompt, row in zip(prompts, prompt_rows):
            #Determine if the prompt rows are appropriately displaying delete buttons
            delete_input = row.find("input", {'alt': 'delete'})
            if prompt.owner == self.user:
                self.failUnless(delete_input, 'delete button not shown for %s but prompt belongs to user %s' % (row, self.user))
            else:
                self.failUnless(not delete_input, 'delete button shown for %s but does not belong to user %s' % (row, self.user))


    def test_postingOnlyDeletesOwnPrompts(self):
        """Tests that a post can only delete the user's own prompts
        """
        #Get one prompt owned by the current user and one owned by another user
        deleteable_prompt = Prompt.objects.get(id=10)
        immutable_prompt = Prompt.objects.get(id=11)
        #Send a post to delete the current user's prompt
        self.client.post(deleteable_prompt.get_absolute_url()+'delete/')
        #Confirm that the prompt is deleted
        self.failUnless(not Prompt.objects.filter(id=deleteable_prompt.id), 'users own prompt %s was not successfully deleted' % deleteable_prompt)
        #Send a post to delete a prompt that does not belong to the current user
        self.client.post(immutable_prompt.get_absolute_url()+'delete/')
        #Confirm that the prompt is not deleted
        self.failUnless(Prompt.objects.filter(id=immutable_prompt.id), 'public prompt %s was deleted by user' % immutable_prompt)


class BeginningPromptTest(TestCase):
    """Tests the creation of the prompt objects
    """
    fixtures = ["beginning_prompts"]

    def test_beginningPrompts(self):
        all_prompts = Prompt.objects.all()
        self.failUnlessEqual(all_prompts.count(), 40)
        for prompt in all_prompts:
            self.failUnlessEqual(prompt.private, False, "%s prompt (id=%d) is private but should be public" % (prompt, prompt.id))
