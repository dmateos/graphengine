from django.contrib import admin
from .models import InferenceModel, InferenceCache

admin.site.register(InferenceModel)
admin.site.register(InferenceCache)
