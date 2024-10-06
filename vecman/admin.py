from django.contrib import admin
from .models import File


class FileAdmin(admin.ModelAdmin):
    actions = ["process_files"]

    @admin.action(description="Process files")
    def process_files(self, request, queryset):
        for file in queryset:
            data = File.encode_embedding(file.text_data)
            file.save_embedding(data)


admin.site.register(File, FileAdmin)
