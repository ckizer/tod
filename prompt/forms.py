from django.newforms.models import ModelForm
from django.newforms import forms

from tod.prompt.models import Prompt

class PromptForm(ModelForm):
    """Provides the form for the prompt object
    """
    class Meta:
        model = Prompt
    def clean_name(self):
        """Ensures that prompt names are unique
        """
        name=self.cleaned_data['name']
        if Prompt.objects.filter(name=name).count():
            raise forms.ValidationError("Prompt name not unique")
        return name
