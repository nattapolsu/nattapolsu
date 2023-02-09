from django.urls import path
from onsite import views
#onsite

urlpatterns = [
    path('traininng',views.TrainingPage,name='training-page'),
    path('form',views.FormPage,name='form-page'),
    path('edit/<course_id>',views.EditForm),
    path('delete/<course_id>',views.DeleteForm),
    path('addcourse',views.AddCourse,name='addcourse'),
    path('courseRegistration',views.courseRegistration,name='courseRegistration'),
    path('contactEdit/<contact_id>',views.contactEdit,name="contactEdit"),
    path('contactDelete/<contact_id>',views.contactDelete),
]