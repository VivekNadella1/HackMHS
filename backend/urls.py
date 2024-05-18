from django.contrib import admin
from django.urls import path, include
from backend import views

urlpatterns = [
  	path('signup/',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('college/', views.college, name='college'),
	path('college_tips',views.college_tips,name='college_tips'),
    path('logout/',views.LogoutPage,name='logout'),
	path('college_stats/',views.college_stats,name='college_stats'),
	path('extracurricular/',views.extracurricular_activities,name='extracurriculars'),
	path('awards/', views.awards, name='awards'),
	path('ap_courses/', views.ap_courses, name='ap_courses'),
	path('', views.XHomePage, name='homepage'),	
	]