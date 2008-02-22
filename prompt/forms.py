from django.newforms.models import ModelForm
from tod.prompt.models import Prompt
from django.newforms import forms

class PromptForm(ModelForm):
    class Meta:
        model = Prompt
    def clean_name(self):
        name=self.cleaned_data['name']
        if Prompt.objects.filter(name=name).count():
            raise forms.ValidationError("Prompt name not unique")
        return name
