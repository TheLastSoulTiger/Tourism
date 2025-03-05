from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from .models import Post, Tour, TourImage, HeaderCarouselImage, TourForm, Tag
from django import forms

class HeaderCarouselImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date')
    search_fields = ('title', 'content')

class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 1

class TourAdminForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Używamy CKEditor dla organizational_details oraz expectations (sekcja: "Что вас ожидает")
        self.fields['organizational_details'].widget = CKEditorWidget()
        self.fields['expectations'].widget = CKEditorWidget()  # Jeśli chcesz formatować marzrutę

class TourAdmin(admin.ModelAdmin):
    form = TourAdminForm
    inlines = [TourImageInline]
    # Pola, które mają być widoczne w liście widoku w adminie
    list_display = ('title', 'short_description', 'price', 'duration', 'starting_point', 'tour_type')
    # Pola dostępne w widoku edycji, w tym dodane 'tour_type'
    fields = (
        'title',
        'short_description',
        'description',
        'expectations',  # Секция: "Что вас ожидает"
        'price',
        'duration',
        'starting_point',  # Możliwość dodawania linków
        'image',  # Główne zdjęcie
        'organizational_details',  # Szczegóły organizacyjne z CKEditor
        'included_in_price',
        'additional_fees',
        'notes',
    )
    search_fields = ('title', 'description', 'expectations', 'tour_type')  # Dodano możliwość wyszukiwania według typu wycieczki

    # Konfiguracja dla CKEditor
    formfield_overrides = {
        RichTextField: {'widget': CKEditorWidget()},
    }

admin.site.register(Tour, TourAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(HeaderCarouselImage, HeaderCarouselImageAdmin)
    