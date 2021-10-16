from django import forms
from content.models import Post, Media

from django.forms import ClearableFileInput


class NewPostForm(forms.ModelForm):
    TYPE_CHOICES = (
        ("IMAGE", "image"),
        ("VIDEO", "video")
    )
    content = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=True)
    # media = forms.ModelChoiceField(queryset=Media.objects)
    # media = forms.FileField(widget={
    #     'media_type': forms.Select(attrs={'class': 'form-control col-sm-2'}),
    #     'image': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'placeholder': 'image'}),
    #     'video': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'placeholder': 'video'}),
    # })
    caption = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium'}), required=True)
    tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-medium'}), required=True)

    class Meta:
        model = Post
        fields = ('content', 'caption', 'tags')
