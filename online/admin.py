from django.contrib import admin
from online.models import Course, Announcement, Assignment
# Register your models here.
admin.site.register(Course)
admin.site.register(Announcement)
admin.site.register(Assignment)