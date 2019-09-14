from django import forms
from django.contrib import admin
from .models import Message
# Register your models here.
# from django_zora_messages.utils import cache_clear


class LocationForm(forms.Form):
    fields = {"location": forms.CharField()}


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        widgets = {
            'dev_instructions': forms.Textarea,
            'locations': forms.ModelMultipleChoiceField,

        }
        exclude = []


class MessageAdmin(admin.ModelAdmin):
    form = MessageForm
    list_display = ('key', 'language', 'value', 'detailed',
                    'dev_instructions')
    list_editable = ('value', 'detailed', 'dev_instructions')
    list_filter = ('language', )
    ordering = ['language', 'key']
    search_fields = ['key', 'value', 'detailed']
    readonly_fields = ('locations',)

    fieldsets = (
        (None, {'fields': ('key', 'language')}),

        ("Translation", {
            'fields': ('value', 'detailed'),

        }),

        ("Instructions", {
            'fields': ('dev_instructions', 'locations',),
        }),


    )

    def get_readonly_fields(self, request, obj=None):
        """ can't change key and language of a message """

        if obj:
            return self.readonly_fields + ('key', 'language')

        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        super(MessageAdmin, self).save_model(request, obj, form, change)


admin.site.register(Message, MessageAdmin)
