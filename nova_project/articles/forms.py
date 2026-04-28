from django import forms

from . import models


class ArticleForm(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ['title', 'body', 'thumbnail']
        labels = {
            "title": "Title",
            "body": "text",
            "thumbnail": "Thumbnail"
        }
        widgets = {
            "title": forms.TextInput(attrs={'placeholder': 'Write article title', 'class': 'form-control mb-3'}),
            "body": forms.TextInput(attrs={'placeholder': 'Write article text', 'class': 'form-control mb-3'}),
            "thumbnail": forms.ClearableFileInput(attrs={'class': 'form-control mb-3'}),
        }