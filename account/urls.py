from django.urls import path
from .views import (home,AllUsersView,login,add_record,
                    add_student,description,
                  AllStudentsView,UpdateStudentsView,AllRecordView
                  )
from django.contrib.auth.views import LogoutView
urlpatterns = [
  path('dashboard/',home, name ='home'),
  path('site/descriptions/',description, name = 'desc'),
  path('users/',AllUsersView.as_view(), name = 'users'),
  path('',login, name = 'login'),
  path('logout/',LogoutView.as_view(template_name ='login.html'),name='logout'),
  path('add/record/',add_record, name = 'add_record'),
  path('add/student/',add_student, name = 'add_student'),
  path('all/records/',AllRecordView.as_view(),name = 'all_records'),
  path('all/students/',AllStudentsView.as_view(), name='allstudents'),
  path('update/<int:pk>/student/',UpdateStudentsView.as_view(), name = 'update_student')

]
