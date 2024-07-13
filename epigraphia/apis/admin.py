from django.contrib import admin
from apis import models
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from django import forms
from datetime import datetime
from django.forms import models as forms_models
from mapwidgets.widgets import GooglePointFieldWidget
import django.contrib.gis.db.models as gis_models

# Register your models here.


class SourceTextAdminForm(forms.ModelForm):
    # Special form for SourceTextAdmin since form needs to display an extra-model field
    source_text_publication_year = forms.CharField(max_length=4, required=False,
                                                   help_text='Enter year in YYYY format, 0000 if not known')

    def __init__(self, *args, **kwargs):
        # Converting publication_date to publication_year
        if 'instance' in kwargs and kwargs['instance']:
            source_text_instance = kwargs['instance']
            source_text_initial = forms_models.model_to_dict(instance=source_text_instance, exclude=['source_text_publication_date', ])
            source_text_initial['source_text_publication_year'] = \
                self.get_publication_year_from_date(source_text_instance.source_text_publication_date)
            kwargs['initial'] = source_text_initial
        super().__init__(*args, **kwargs)

    def get_publication_year_from_date(self, publication_date):
        if not publication_date:
            return '0000'
        return str(publication_date.year)

    def get_publication_date_from_year(self, publication_year='0000'):
        publication_ymd = "{}-01-01".format(publication_year)
        return datetime.strptime(publication_ymd, '%Y-%m-%d')

    def clean(self):
        # Converting publication_year to publication_date
        if self.cleaned_data['source_text_publication_year']:
            publication_year = self.cleaned_data['source_text_publication_year']
            self.instance.source_text_publication_date = self.get_publication_date_from_year(publication_year)
        super().clean()

    class Meta:
        model = models.SourceText
        # These fields are not user editable and will be updated programmatically
        exclude = ('source_text_publication_date', 'created_by', 'last_modified_by', 'created_at', 'last_modified_at')


class SourceTextAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_number_of_chapters')
    list_filter = ('source_text_series', )
    list_per_page = 25
    search_fields = ('source_text_title', 'source_text_series')
    form = SourceTextAdminForm

    @admin.display(description='Number of Chapters')
    def get_number_of_chapters(self, obj):
        # For displaying in list page
        count = models.SourceTextChapter.objects.filter(source_text_id=obj.source_text_id).count()
        url = reverse('admin:apis_sourcetextchapter_changelist') + '?' + \
              urlencode({'source_text__source_text_id': f"{obj.source_text_id}"})
        return format_html('<a href={}>{}</a>', url, count)

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        # Save created by and modified by information
        if request.user.is_authenticated:
            user = request.user.username

            if not change:
                obj.created_by = user
            obj.last_modified_by = user
            super().save_model(request, obj, form, change)


class SourceTextChapterAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_number_of_inscriptions')
    list_per_page = 25
    search_fields = ('source_text_chapter_title', 'source_text__source_text_title', 'source_text__source_text_series')
    exclude = ('created_by', 'last_modified_by', 'created_at', 'last_modified_at')

    @admin.display(description='Number of Inscriptions')
    def get_number_of_inscriptions(self, obj):
        # For displaying in list page
        count = models.Inscription.objects.filter(source_text_chapter_id=obj.source_text_chapter_id).count()
        url = reverse('admin:apis_inscription_changelist') + '?' + \
              urlencode({'source_text_chapter__source_text_chapter_id': f"{obj.source_text_chapter_id}"})
        return format_html('<a href={}>{}</a>', url, count)

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        # Save created by and modified by information
        if request.user.is_authenticated:
            user = request.user.username

            if not change:
                obj.created_by = user
            obj.last_modified_by = user
            super().save_model(request, obj, form, change)


class InscriptionTextInline(admin.StackedInline):
    model = models.InscriptionText
    max_num = 1
    exclude = ('created_by', 'last_modified_by', 'created_at', 'last_modified_at')

    def save_model(self, request, obj, form, change):
        if request.user.is_authenticated:
            user = request.user.username

            if not change:
                obj.created_by = user
            obj.last_modified_by = user
            super().save_model(request, obj, form, change)


class TranslationInline(admin.StackedInline):
    model = models.Translation
    max_num = 1
    exclude = ('created_by', 'last_modified_by', 'created_at', 'last_modified_at')

    def save_model(self, request, obj, form, change):
        if request.user.is_authenticated:
            user = request.user.username

            if not change:
                obj.created_by = user
            obj.last_modified_by = user
            super().save_model(request, obj, form, change)


class TransliterationInline(admin.StackedInline):
    model = models.Transliteration
    max_num = 1
    exclude = ('created_by', 'last_modified_by', 'created_at', 'last_modified_at')

    def save_model(self, request, obj, form, change):
        if request.user.is_authenticated:
            user = request.user.username

            if not change:
                obj.created_by = user
            obj.last_modified_by = user
            super().save_model(request, obj, form, change)


class InscriptionAdminForm(forms.ModelForm):
    # Special form for Inscription to have SourceText selector
    source_text = forms.ModelChoiceField(queryset=models.SourceText.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        # For populating the source text in the form when model is being changed
        if 'instance' in kwargs:
            inscription_instance = kwargs['instance']
            if inscription_instance:
                initial = forms_models.model_to_dict(instance=inscription_instance)
                initial['source_text'] = models.SourceText.objects.get(source_text_id=inscription_instance.source_text_chapter.source_text.source_text_id);
                kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.Inscription
        fields = ('source_text', 'source_text_chapter', 'location', 'source_text_inscription_number')
        exclude = ('created_by', 'last_modified_by', 'created_at', 'last_modified_at')


class InscriptionAdmin(admin.ModelAdmin):
    inlines = [InscriptionTextInline, TransliterationInline, TranslationInline]
    list_display = ('get_text_title', 'get_chapter_title', 'source_text_inscription_number', 'location')
    search_fields = ('source_text_chapter__source_text__source_text_title',
                     'source_text_chapter__source_text_chapter_title', 'source_text_inscription_number')
    list_per_page = 25
    list_filter = ('source_text_chapter__source_text__source_text_title',)
    # Autocomplete for source text chapter for ease of use
    autocomplete_fields = ('source_text_chapter', 'location')
    form = InscriptionAdminForm

    @admin.display(description='Source Text')
    def get_text_title(self, obj):
        return obj.source_text_chapter.source_text.source_text_title

    @admin.display(description='Chapter')
    def get_chapter_title(self, obj):
        return obj.source_text_chapter.source_text_chapter_title

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if request.user.is_authenticated:
            user = request.user.username

            if not change:
                obj.created_by = user
            obj.last_modified_by = user
            super().save_model(request, obj, form, change)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    list_per_page = 25
    search_fields = ('location_name',)
    exclude = ('created_by', 'last_modified_by', 'created_at', 'last_modified_at')
    formfield_overrides = {
        gis_models.PointField: {"widget": GooglePointFieldWidget(settings={
            "GooglePointFieldWidget": (
                                        ("zoom", 5),
                                        ("mapCenterLocationName", "india"),
                                        ("GooglePlaceAutocompleteOptions", {'componentRestrictions': {'country': 'in'}}),
                                        ("markerFitZoom", 12),
                                        ("scrollWheel", False),
                                        ("streetViewControl", False),
                                      )
        })}
    }

    def save_model(self, request, obj, form, change):
        # Save created by and modified by information
        if request.user.is_authenticated:
            user = request.user.username

            if not change:
                obj.created_by = user
            obj.last_modified_by = user
            super().save_model(request, obj, form, change)


admin.site.register(models.SourceText, SourceTextAdmin)
admin.site.register(models.SourceTextChapter, SourceTextChapterAdmin)
admin.site.register(models.Inscription, InscriptionAdmin)
admin.site.register(models.Location, LocationAdmin)
# Disable model object deletion from admin across all models
admin.site.disable_action('delete_selected')
