from django.urls import path

from . import views


urlpatterns = [
    # Login
    path('', views.index, name='index'),
    # Logout
    path('logout/', views.userlogout, name='logout'),

    # Registration
    path('registration/role/', views.registration_role, name='registration_role'),
    path('registration/student/', views.registration_student, name='registration_student'),
    path('registration/faculty/', views.registration_faculty, name='registration_faculty'),
    path('registration/toolkeeper/', views.registration_toolkeeper, name='registration_toolkeeper'),
    
    # Student/Faculty
    path('home/', views.home_sf, name='home_sf'),
    path('reservation/', views.reservation_sf, name='reservation_sf'),
    path('profile/', views.profile_sf, name='profile_sf'),
    path('transactions/', views.transactions_sf, name='transactions_sf'),
    path('transactions/<int:transaction_id>/', views.transaction_details_sf, name='transaction_details_sf'),

    # Tool Keeper
    # transactions tool keeper
    path('tk/transactions/', views.transactions_tk, name='transactions_tk'),
    
    # scan code toolkeeper
    path('tk/scanqr/', views.scanqr_tk, name='scanqr_tk'),

    # view transactions toolkeeper
    path('tk/transactions/', views.borrower_transaction, name='borrower_transaction'),

    # view transaction details toolkeeper
    path('tk/transactions/<int:transaction_id>', views.view_transaction_details_tk, name='view_transaction_details_tk'),
    path('tk/transactions/checkDateTime/<int:transaction_id>', views.check_datetime_tk, name='check_datetime_tk'),
    
    # storages toolkeeper
    path('tk/tools/storages', views.storages_tk, name='storages_tk'),

    # add tool toolkeeper
    path('tk/tools/add', views.add_tools_tk, name='add_tools_tk'),

    # edit tools toolkeeper
    path('tk/tools/edit', views.edit_tools_tk, name='edit_tools_tk'),
]