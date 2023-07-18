from django.contrib import admin

from .models import Student,Session,Semester,Record,CustomUser,Department
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model

User = get_user_model()
LogEntry._meta.get_field('user').remote_field.model = User

class StudentAdmin(admin.ModelAdmin):
    list_display = ('reg_no', 'first_name', 'level','created_on')
    list_filter = ("level",)
    search_fields = ['reg_no', 'last_name']
    prepopulated_fields = {}

admin.site.register(Student, StudentAdmin)
admin.site.register(Session)
admin.site.register(Semester)
admin.site.register(Record)
admin.site.register(CustomUser)
admin.site.register(Department)
