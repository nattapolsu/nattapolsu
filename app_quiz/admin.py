from django.contrib import admin
from app_quiz.models import Quiz,Question,StudentAnswer

# Register your models here.
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(StudentAnswer)