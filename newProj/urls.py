"""
URL configuration for newProj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Homepage
    path('', views.homepage, name='homepage'),

    # Open Day booking
    path('openday/', views.openday, name='openday'),
    path('payment/', views.payment, name='payment'),
    path('booking_success/<int:booking_id>/', views.booking_success, name='booking_success'),

    #Courses
    path('all_courses', views.all_courses, name='all_courses'),

    # College links
    path('college_links/', views.college_Links, name='college_Links'),

    # Student application
    path('applytocourse/', views.ApplyToCourse, name='ApplyToCourse'),
    path('GuardianSection/', views.GuardianSection, name='GuardianSection'),
    path('applicationsuccess/<int:application_id>/', views.ApplicationSuccess, name='ApplicationSuccess'),

    # Student account & login
    path('viewcourse/<int:course_id>/', views.view_course, name='view_course'),
    path('studentaccount/<int:student_id>/', views.StudentAccount, name='StudentAccount'),
    path('login/', views.student_login, name='student_login'),
    path('logout/', views.student_logout, name='student_logout'),
    path('view_account/', views.view_account, name= 'view_account'),
    

    #Admin Account & login
    path('Admin_login/', views.Admin_login, name='Admin_login'),

    #navbar information 
    path('contact', views.contact, name='contact'),
    path('campus', views.campus, name='campus'),
    path('about', views.about, name='about')
]
