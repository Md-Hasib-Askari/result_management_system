from django.contrib import admin

from .models import Student, Subject

# @admin.register(Class)
# class ClassAdmin(admin.ModelAdmin):
#     list_display = ['name', 'created_at', 'updated_at']

# @admin.register(Section)
# class SectionAdmin(admin.ModelAdmin):
#     list_display = ['name', 'created_at', 'updated_at']

admin.site.site_header = "Rasulpur High School"
admin.site.site_title = 'Rasulpur High School'
admin.site.index_title = 'Student Management System'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'roll', 'student_class', 'section', 'group', 'admission_date', 'created_at', 'updated_at']
    list_filter = ['student_class', 'section', 'group']
    search_fields = ['name', 'phone', 'roll']
    list_editable = ['student_class', 'section', 'group']
    fieldsets = [
        ('Personal Information', 
            { 'fields': ('name', 'father_name', 'mother_name', 'dob', 'gender')}),
        ('Academic Information', 
            { 'fields': ('roll', 'student_class', 'section', 'group', 'admission_date')}),
    ]
        

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'group', 'optional', 'student_class', 'created_at', 'updated_at']
    list_filter = ['group', 'student_class', 'optional']
    

# @admin.register(Teacher)
# class TeacherAdmin(admin.ModelAdmin):
#     list_display = ['name', 'phone', 'subject', 'student_class', 'section', 'created_at', 'updated_at']
#     search_fields = ['name', 'phone']
#     list_filter = ['subject', 'join_date', 'student_class', 'section']
#     fieldsets = [
#         ('Personal Information', 
#             { 'fields': ('name', 'phone', 'email')}),
#         ('Academic Information',
#             { 'fields': ('designation', 'join_date',)}),
#         ('Subject Information', 
#             { 'fields': ('subject', ('student_class', 'section'))}),
#     ]