from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "published_date"]

    # Example of extra validation (prevent extremely long titles)
    def clean_title(self):
        title = self.cleaned_data.get("title", "").strip()
        if len(title) > 300:
            raise forms.ValidationError("Title too long.")
        return title


class SearchForm(forms.Form):
    q = forms.CharField(max_length=100, required=False, strip=True)



class ExampleForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        label="Your Name",
        widget=forms.TextInput(attrs={"placeholder": "Enter your name"})
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email"})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Type your message"}),
        required=False,
        label="Message"
    )