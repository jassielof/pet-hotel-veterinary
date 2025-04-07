from django.contrib import admin

from django.apps import apps
from django.utils import timezone
# from core import models

models = apps.get_app_config("core").get_models()


for model in models:
    admin.site.register(model)

# admin.site.unregister(Stay)


# @admin.register(Stay)
# class StayAdmin(admin.ModelAdmin):
#     list_display = Stay.DisplayFields
#     search_fields = Stay.SearchableFields
#     list_filter = Stay.FilterFields
