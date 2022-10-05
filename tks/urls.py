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

    # Tool Keeper
    path('toolkeeper/home/', views.home_tk, name='home_tk'),
    path('toolkeeper/transactions/', views.transactions_tk, name='transactions_tk'),
    
    # note: must include the transaction id of the borrower!!
    path('toolkeeper/transactions/tid', views.borrower_transaction, name='borrower_transaction'),

    # add tool toolkeeper
    path('toolkeeper/managetools/add', views.add_tools_tk, name='add_tools_tk'),
]