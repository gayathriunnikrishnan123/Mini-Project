from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.index,name="index"),
    path('about/', views.about,name="about"),
    path('login/', views.login_view, name='login'),
    path('register/', views.register,name="register"),
    path('userpage/', views.userpage,name="userpage"),
     path('agentpage/', views.agentpage,name="agentpage"),
      path('policepage/', views.policepage,name="policepage"),
    path('userpage/logout', views.userLogout,name="logout"),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

]