from django.urls import path
from iso import views #ดึงฟังก์ชันจาก views มา
#iso

urlpatterns = [
    path('',views.HomePage,name='home-page'),
    path('news',views.NewsBlog,name='news-page'),
    path('register/',views.Register,name='register-page'),
]