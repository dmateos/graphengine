from django.contrib import admin
from .models import ETLJob, ETLInput, ETLOutput

admin.site.register(ETLJob)
admin.site.register(ETLInput)
admin.site.register(ETLOutput)
