from django.urls import path

from . import views


urlpatterns = [
    # Login
    path('', views.index, name='index'),
    # Registration
    path('registration/role/', views.registration_role, name='registration_role'),
    path('registration/student/', views.registration_student, name='registration_student'),
    path('registration/faculty/', views.registration_faculty, name='registration_faculty'),
    path('registration/toolkeeper/', views.registration_toolkeeper, name='registration_toolkeeper'),
    # Home Page
    path('home/', views.home_sf, name='home_sf'),
    path('toolkeeper/home/', views.home_tk, name='home_tk'),
]