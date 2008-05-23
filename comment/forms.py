from django.newforms.models import ModelForm

from tod.comment.models import Comment

class CommentForm(ModelForm):
    """Provides the form for the comments
    """
    class Meta:
        model = Comment

