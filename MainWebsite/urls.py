from django.contrib import admin
from django.urls import path, include
from . import views


app_name = "MainWebsite"


urlpatterns = [

    # Home Page
    path('', views.home_page, name='home'),
    path('about-us/', views.about_us, name='about'),
    path('register/', views.register, name='register'),
    path('pick-plan/', views.pick_plan, name='pick-plan'),
    path('onboarding-free/', views.onboarding_free, name='onboarding-free'),

    path('welcome-video/', views.welcome_video, name='welcome-video'),

]