from django.contrib import admin
from .models import UniversalTag, Schedule, AWSAccessDetails, AzureAccessDetails

admin.site.register(UniversalTag)
admin.site.register(Schedule)
admin.site.register(AWSAccessDetails)
admin.site.register(AzureAccessDetails)
