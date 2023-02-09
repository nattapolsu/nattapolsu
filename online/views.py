from django.shortcuts import render, redirect
from django.contrib import messages
from online.models import Course,Announcement
from .forms import AnnouncementForm
from django.http import HttpResponse
# Create your views here.

def ElerningPage(request):
    courses = Course.objects.all()
    return render(request,"elerning.html",{"courses":courses})

def course_page(request,code):
    #try:
        course = Course.objects.get(code = code)
        announcements = Announcement.objects.filter(course_code=course)

        context = {
            'course':course,
            'announcements': announcements,
            }
        return render(request,"course.html",context)
    
    #except:
        return HttpResponse("<h1><center>Error</h1>")


def addAnnouncement(request, code):
    if request.method == 'POST':
            form = AnnouncementForm(request.POST)
            form.instance.course_code = Course.objects.get(code=code)
            if form.is_valid():
                form.save()
                return redirect('course-page', code=code)
                
    else:
        form = AnnouncementForm()
    return render(request, 'announcement.html', {'course': Course.objects.get(code=code), 'form': form})


def deleteAnnouncement(request, code, id):
        try:
            announcement = Announcement.objects.get(course_code=code, id=id)
            announcement.delete()
            messages.warning(request, 'Announcement deleted successfully.')
            return redirect('course-page', code=code)
        except:
            return redirect('course-page', code=code)


def editAnnouncement(request, code, id):
        announcement = Announcement.objects.get(course_code_id=code, id=id)
        form = AnnouncementForm(instance=announcement)
        context = {
            'announcement': announcement,
            'course': Course.objects.get(code=code),
            'form': form
        }
        return render(request, 'update-announcement.html', context)


def updateAnnouncement(request, code, id):
        try:
            announcement = Announcement.objects.get(course_code_id=code, id=id)
            form = AnnouncementForm(request.POST, instance=announcement)
            if form.is_valid():
                form.save()
                messages.info(request, 'Announcement updated successfully.')
                return redirect('course-page', code=code)
        except:
            return redirect('course-page', code=code)
