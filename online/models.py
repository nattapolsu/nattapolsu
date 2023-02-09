from django.db import models
from froala_editor.fields import FroalaField

# Create your models here.
class Course(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=False, unique=True)
    studentKey = models.IntegerField(null=False, unique=True)
    facultyKey = models.IntegerField(null=False, unique=True)

    class Meta:
        unique_together = ('code','name')
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.name


class Announcement(models.Model):
    course_code = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    datetime = models.DateTimeField(auto_now_add=True, null=False)
    description = FroalaField(theme="dark", null=True,blank=True)

    class Meta:
        verbose_name_plural = "Announcements"
        ordering = ['-datetime']

    def __str__(self):
        return self.datetime.strftime("%d-%b-%y, %I:%M %p")

    def post_date(self):
        return self.datetime.strftime("%d-%b-%y, %I:%M %p")



class Assignment(models.Model):
    course_code = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    datetime = models.DateTimeField(auto_now_add=True, null=False)
    deadline = models.DateTimeField(null=False)
    file = models.FileField(upload_to='assignments/', null=True, blank=True)
    marks = models.DecimalField(max_digits=6, decimal_places=2, null=False)

    class Meta:
        verbose_name_plural = "Assignments"
        ordering = ['-datetime']

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    def post_date(self):
        return self.datetime.strftime("%d-%b-%y, %I:%M %p")

    def due_date(self):
        return self.deadline.strftime("%d-%b-%y, %I:%M %p")