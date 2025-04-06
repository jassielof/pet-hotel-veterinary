from django.contrib import admin
from .models import *
from django.apps import apps
from django.utils import timezone


models = apps.get_app_config("core").get_models()

for model in models:
    admin.site.register(model)

admin.site.unregister(Estadia)


@admin.register(Estadia)
class EstadiaAdmin(admin.ModelAdmin):
    list_display = Estadia.DisplayFields
    search_fields = Estadia.SearchableFields
    list_filter = Estadia.FilterFields
