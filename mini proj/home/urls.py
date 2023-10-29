from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from home.views import delete_user


urlpatterns = [
    path('', views.index,name="index"),
    path('about/', views.about,name="about"),
    path('services/', views.services,name="services"),
    path('login/', views.login_view, name='login'),
    path('register/', views.register,name="register"),
    path('registration_success/', views.registration_success, name='registration_success'),
    path('userpage/', views.userpage,name="userpage"),
    path('worker_list/', views.worker_list,name="worker_list"),
    path('agentpage/', views.agentpage,name="agentpage"),
    path('addworker/', views.addworker,name="addworker"),
    path('viewworker/', views.viewworker,name="viewworker"),
    path('update_worker/<int:worker_id>/', views.update_worker, name='update_worker'),
    path('delete_worker/<int:worker_id>/', views.delete_worker, name='delete_worker'),
    path('policepage/', views.policepage,name="policepage"),
    path('adminpanel/', views.adminpanel,name="adminpanel"),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('logout/', views.logout_view, name='logout'),
    path('all-police/', views.PoliceOfficerViewSet.as_view()),
    path('accounts/profile/', views.userpage,name="userpage"),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]