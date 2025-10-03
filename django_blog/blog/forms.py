from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Post,Tag
from .models import Comment
from taggit.forms import TagWidget

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required.')
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post title', 'class': 'input'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your post...', 'class': 'textarea', 'rows': 8}),
            'tags': TagWidget(),   # ✅ this is the key requirement
        }
    
    # Provide a single text field for tags (comma-separated)
    tags_field = forms.CharField(
        required=False,
        label='Tags (comma-separated)',
        widget=forms.TextInput(attrs={'placeholder': 'tag1, tag2, tag3'})
    )    
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags_field']

    def __init__(self, *args, **kwargs):
        # If editing an existing post, prefill tags_field
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['tags_field'].initial = ', '.join([t.name for t in self.instance.tags.all()])

    def clean_tags_field(self):
        value = self.cleaned_data.get('tags_field', '')
        # normalize: split by comma and strip whitespace, drop empties
        tags = [t.strip() for t in value.split(',') if t.strip()]
        return tags    
    
        
class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'})
    )

    class Meta:
        model = Comment
        fields = ['content']        