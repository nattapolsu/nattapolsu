from django.urls import path
from online import views #ดึงฟังก์ชันจาก views มา
#iso

urlpatterns = [
    path('elerning',views.ElerningPage,name='elerning-page'),
    path('course/<int:code>',views.course_page,name='course-page'),
    path('addAnnouncement/<int:code>/',views.addAnnouncement, name='addAnnouncement'),
    path('announecement/<int:code>/<int:id>/',views.deleteAnnouncement, name='deleteAnnouncement'),
    path('edit/<int:code>/<int:id>/',views.editAnnouncement, name='editAnnouncement'),
    path('update/<int:code>/<int:id>/',views.updateAnnouncement, name='updateAnnouncement'),
]