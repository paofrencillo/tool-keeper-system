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
    path('transactions/view/', views.view_transactions, name='view_transactions'),

    # Tool Keeper
    # transactions tool keeper
    path('toolkeeper/transactions/', views.transactions_tk, name='transactions_tk'),
    
    # scan code toolkeeper
    path('toolkeeper/scanqr/', views.scanqr_tk, name='scanqr_tk'),

    # note: must include the transaction id of the borrower!!
    path('toolkeeper/transactions/tid', views.borrower_transaction, name='borrower_transaction'),

    # storages tool keeper
    path('toolkeeper/tools/storages', views.storages_tk, name='storages_tk'),

    # add tool toolkeeper
    path('toolkeeper/tools/add', views.add_tools_tk, name='add_tools_tk'),

    # edit tools toolkeeper
    path('toolkeeper/tools/edit', views.edit_tools_tk, name='edit_tools_tk'),
]