from BeautifulSoup import BeautifulSoup
from soupselect import select

from django.test import TestCase
from django.test.client import Client
from django.db import IntegrityError
from django.contrib.auth.models import User

from tod.comment.models import Comment

class CommentTestCase(TestCase):
    """Tests the Comment app
    """
    fixtures = ["all_difficulties"]
    def setUp(self):
        self.client = Client()
        self.client.login(username="laura", password="laura")

    def test_commentForm(self):
        """ User sees a problem and wants to notify us.  They should...
        """
        # See a button at the bottom of every page that shows them a form for submitting a comment
        pages = [
            '/game/',
            '/prompt/',
            ]
        for page in pages:
            response = self.client.get(page)
            self.findTextarea('#comment_form', response.content, 'description')
            self.findInput('#comment_form', response.content, 'email')
            self.findInput('#comment_form', response.content, 'page', page)

            # submit the form
            form = self.get_section('#comment_form', response.content).form
            action = form.get('action')
            self.failUnlessEqual(Comment.objects.filter(page=page).count(), 0)
            self.client.post(action, {'description': 'testing', 'page': page, 'email': 'test@emlprime.com'})
            self.failUnlessEqual(Comment.objects.filter(page=page).count(), 1)
        
            
    def get_section(self, selector, content):
        doc = BeautifulSoup(content)
        selection = select(doc, selector)
        self.failUnless(selection, "Could not find " + selector + " in content")
        info = selection[0]
        return info
    
    def findInput(self, selector, content, input_name, value=None):
        """Find an input in a document
        """
        info = self.get_section(selector, content)
        input = info.find('input', {'name': input_name})
        self.failUnless(input, "Could not find an input named " + input_name + "  in: " + str(info))

        if input and value:
            found_value = input.get('value')
            input = info.find('input', {'name': input_name, 'value': value}) 
            self.failUnless(input, "Could not find an input named " + input_name + " with value: " + value + " found value: " + found_value)
            
        return input

    def findTextarea(self, selector, content, input_name, value=None):
        """Find a textarea input in a document
        """
        info = self.get_section(selector, content)
        input = info.find('textarea', {'name': input_name})
        self.failUnless(input, "Could not find an input named " + input_name + "  in: " + str(info))

        if input and value:
            found_value = input.text
            input = info.find('input', {'name': input_name, 'value': value}) 
            self.failUnless(input, "Could not find an input named " + input_name + " with value: " + value + " found value: " + found_value)
            
        return input

    def findLabel(self, selector, content, label_for):
        """Find a label for a particular input in a document
        """
        info = self.get_section(selector, content)
        label = info.find('label', {'for': label_for})
        self.failUnless(label, "Could not find an label for " + label_for)
        return label

    def findText(self, selector, content, text):
        """Find a text for a particular input in a document
        """
        info = self.get_section(selector, content)
        self.failUnless(text in str(info), "Could not find " + text + " in: " + str(info))
        return info
