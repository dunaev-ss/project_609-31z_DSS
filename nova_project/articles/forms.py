from django import forms

from . import models


class ArticleForm(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ['title', 'body', 'thumbnail']
        labels = {
            "title": "Заголовок",
            "body": "Текст статьи",
            "thumbnail": "Обложка"
        }
        widgets = {
            "title": forms.TextInput(attrs={'placeholder': 'Введите заголовок статьи...', 'class': 'form-control mb-3'}),
            "body": forms.TextInput(attrs={'placeholder': 'Введите текст статьи...', 'class': 'form-control mb-3'}),
            "thumbnail": forms.ClearableFileInput(attrs={'class': 'form-control mb-3'}),
        }