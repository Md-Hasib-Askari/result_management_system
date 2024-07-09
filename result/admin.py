from django.contrib import admin

from .models import Result

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'exam_type', 'cq', 'mcq', 'practical', 'project']
    list_filter = ['student', 'subject', 'exam_type']
    search_fields = ['student__name', 'subject__name']