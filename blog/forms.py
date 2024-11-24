from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        labels = {'body': ''}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Add a comment...',
            'rows': '3',
            'cols': '65',
        })