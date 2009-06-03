from django.forms.models import ModelForm

from tod.comment.models import Comment

class CommentForm(ModelForm):
    """Provides the form for the comments
    """

    def __init__(self, *args, **kwargs):
        self.page = kwargs.pop('page') if kwargs.has_key("page") else "/"
        super(self.__class__, self).__init__(*args, **kwargs)
    
    class Meta:
        model = Comment

    def save(self, commit=True):
        object = super(self.__class__, self).save(commit=False)
        object.page = self.page
        if commit:
            object.save()

        return object
