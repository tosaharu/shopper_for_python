"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

# JavaEEでいうサーブレット1行目、@WebServletの役割
urlpatterns = [
    # path('', views.index, name='index'),
    path('u_Login/', views.U_LoginView.as_view(), name='u_Login'),
    path('u_Logout/', views.U_LogoutView.as_view(), name='u_Logout'),

    path('u_Main/', views.U_MainView.as_view(), name='u_Main'),

    path('u_RegisterUser/', views.U_RegisterUserView.as_view(),
         name='u_RegisterUser'),

    path('u_Quit/', views.U_QuitView.as_view(), name='u_Quit'),

    path('u_RegisterProduct/', views.U_RegisterProductView.as_view(),
         name='u_RegisterProduct'),
    path('u_RegisterProduct/Ajax_RegisterStoreInfo/', views.Ajax_RegisterStoreInfo.as_view(),
         name='Ajax_RegisterStoreInfo'),

    path('u_StoreInfo/<int:id>', views.U_StoreInfoView.as_view(),
         name='u_StoreInfo'),

    path('u_ChangeInfo/', views.U_ChangeInfoView.as_view(), name='u_ChangeInfo'),
    path('u_ChangeInfo/Ajax_GetUserBirthday/',
         views.Ajax_GetUserBirthday.as_view(), name='Ajax_GetUserBirthday'),
    path('u_ChangeInfo/Ajax_ChangeUserInfo/',
         views.Ajax_ChangeUserInfo.as_view(), name='Ajax_ChangeUserInfo'),
    path('u_ChangeInfo/Ajax_ChangeUserPassword/',
         views.Ajax_ChangeUserPassword.as_view(), name='Ajax_ChangeUserPassword'),


    path('u_ResetPasswordAuth/', views.U_ResetPasswordAuthView.as_view(),
         name='u_ResetPasswordAuth'),
    path('u_ResetPasswordAuth/Ajax_CheckUserMailAndBirthday/',
         views.Ajax_CheckUserMailAndBirthday.as_view(), name='Ajax_CheckUserMailAndBirthday'),
    path('u_ResetPasswordAuth/Ajax_CheckOneTimePass/',
         views.Ajax_CheckOneTimePass.as_view(), name='Ajax_CheckOneTimePass'),

    path('u_ResetPassword/', views.U_ResetPasswordView.as_view(),
         name='u_ResetPassword'),

    path('u_SessionExpired/',
         views.U_SessionExpiredView.as_view(), name='u_SessionExpired'),

]
