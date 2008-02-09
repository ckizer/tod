from django.newforms.models import ModelForm
from tod.prompt.models import Prompt

class PromptForm(ModelForm):
    class Meta:
        model = Prompt
