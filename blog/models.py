from django.db import models
from django.utils import timezone
from django import forms
from ckeditor.fields import RichTextField
import datetime

class HeaderCarouselImage(models.Model):
    image = models.ImageField(upload_to='carousel_images/')
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title or "Image without title"

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tour(models.Model):
    TOUR_TYPE_CHOICES = [
        ('bike', 'На вело'),
        ('car', 'На машине'),
        ('other', 'Иной странспорт'),
        ('walk', 'Пешком'),
        ('boat', 'На лодке')
    ]
    
    title = models.CharField(max_length=255)
    short_description = models.CharField(max_length=100, blank=True)
    description = models.TextField(default="")
    expectations = RichTextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    departure_date = models.DateField(default=timezone.now)
    duration = models.IntegerField(default=1)
    starting_point = models.CharField(max_length=200, default="")
    image = models.ImageField(upload_to='tours/')
    organizational_details = RichTextField(blank=True, null=True)
    available_dates = models.JSONField(default=list, blank=True)
    additional_fees = RichTextField(blank=True, null=True)
    tour_type = models.CharField(max_length=10, choices=TOUR_TYPE_CHOICES, default='other') 
    included_in_price = RichTextField(blank=True, null=True)
    extra_charges = RichTextField(blank=True, null=True)
    notes = RichTextField(blank=True, null=True)
    
    def __str__(self):
        return self.title


class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['title', 'short_description', 'tour_type']
        widgets = {
            'short_description': forms.TextInput(attrs={'maxlength': '100'}),
        }


class TourImage(models.Model):
    image = models.ImageField(upload_to='tour_images/')
    tour = models.ForeignKey(Tour, related_name='tour_images', on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.tour.title}"

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Review(models.Model):
    name = models.CharField(max_length=100)
    review = models.TextField()
    tour = models.ForeignKey(Tour, related_name='reviews', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.tour.title}'
