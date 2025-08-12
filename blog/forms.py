from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'preview', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_title'  # Стандартный ID Django
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'id': 'id_content'
            }),
            'preview': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'id_preview'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_is_published'
            }),
        }

