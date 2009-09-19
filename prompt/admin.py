from django.contrib import admin
from tod.prompt.models import Prompt

class PromptAdmin(admin.ModelAdmin):
    pass
admin.site.register(Prompt, PromptAdmin)
