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
    
    # Student/Faculty
    path('home/', views.home_sf, name='home_sf'),
    path('reservation/', views.reservation, name='reservation'),
    path('profile/', views.profile_sf, name='profile_sf'),
    path('transactions/', views.transactions_sf, name='transactions_sf'),
    path('transactions/view/', views.view_transactions, name='view_transactions'),

    # Tool Keeper
    path('toolkeeper/home/', views.home_tk, name='home_tk'),
    path('toolkeeper/transactions/', views.transactions_tk, name='transactions_tk'),

]