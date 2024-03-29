from django.urls import path
from django.contrib.auth import views as auth_views
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
    path('transactions/<str:transaction_id>/', views.transaction_details_sf, name='transaction_details_sf'),
    path('change_password/', views.change_password_sf, name='change_password_sf'),
   
    # Tool Keeper
    # transactions tool keeper
    path('tk/transactions/', views.transactions_tk, name='transactions_tk'),
    path('tk/transactions/csv/', views.transaction_csv, name='transaction_csv'),

    # scan code toolkeeper
    path('tk/scanqr/', views.scanqr_tk, name='scanqr_tk'),

    # profile toolkeeper
    path('tk/profile/', views.profile_tk, name='profile_tk'),
    path('tk/change_password/', views.change_password_tk, name='change_password_tk'),

    # view transaction details toolkeeper
    path('tk/transactions/<str:transaction_id>/', views.transaction_details_tk, name='transaction_details_tk'),
    path('tk/transactions/<str:transaction_id>/borrow/', views.borrow_tools_tk, name='borrow_tools_tk'),
    path('tk/transactions/<str:transaction_id>/return/', views.return_tools_tk, name='return_tools_tk'),
    path('tk/transactions/<str:transaction_id>/void/', views.void_tools_tk, name='void_tools_tk'),
    path('scan_tools/', views.scan_tools, name='scan_tools'),

    # storages toolkeeper
    path('tk/manage_tools/storages/', views.storages_tk, name='storages_tk'),
    path('tk/manage_tools/storage/<int:storage>', views.storage_tk, name='storage_tk'),

    # add tool toolkeeper
    path('tk/manage_tools/add/', views.add_tools_tk, name='add_tools_tk'),

    # edit tools toolkeeper
    path('tk/manage_tools/tools/$', views.tools_tk, name='tools_tk'),

    path('openStorage/', views.openStorage, name='openStorage'),

    # Reset Password urls
    path("password_reset/", views.reset_password, name="reset_password"),
    path("password_reset/sent/",
            auth_views.PasswordResetDoneView.as_view(template_name='password_reset/reset_password_sent.html'),
            name="reset_password_sent"),
    path("password_reset/<uidb64>/<token>/",
            auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/reset_password_confirm.html'),
            name="reset_password_confirm"),
    path("password_reset_complete/",
            auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/reset_password_complete.html'),
            name="password_reset_complete"),
]