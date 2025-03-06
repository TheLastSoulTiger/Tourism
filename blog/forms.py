from django import forms
from .models import Post
from .models import Review
from .models import Tour


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'review']


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Imię i nazwisko'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Twój email'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Treść wiadomości'})
    )

    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message) < 10:
            raise forms.ValidationError("Wiadomość musi zawierać co najmniej 10 znaków.")
        return message

class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['title', 'description', 'organizational_details', 'tour_type', 'price', 'departure_date']
        widgets = {
            'short_description': forms.TextInput(attrs={'maxlength': '100'}),
            'departure_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

# class TourForm(forms.ModelForm):
#     class Meta:
#         model = Tour
#         fields = ['title', 'description', 'images']  # Dodaj inne pola według potrzeb
#         widgets = {
#             'images': forms.ClearableFileInput(attrs={'multiple': True}),
#         }
