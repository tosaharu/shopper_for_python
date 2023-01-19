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
    path('', views.IndexView.as_view(), name='index'),

    path('u_Login/', views.U_LoginView.as_view(), name='u_Login'),
    path('u_Logout/', views.U_LogoutView.as_view(), name='u_Logout'),

    path('u_Main/', views.U_MainView.as_view(), name='u_Main'),
    path('u_Main/Ajax_GetMultiSelectArea/',
         views.Ajax_GetMultiSelectArea.as_view(), name='Ajax_GetMultiSelectArea'),
    path('u_Main/Ajax_GetAreaProduct/',
         views.Ajax_GetAreaProduct.as_view(), name='Ajax_GetAreaProduct'),
    path('u_Main/Ajax_GetSortedProduct/',
         views.Ajax_GetSortedProduct.as_view(), name='Ajax_GetSortedProduct'),

    path('u_RegisterUser/', views.U_RegisterUserView.as_view(),
         name='u_RegisterUser'),
    path('u_RegisterUser/Ajax_GetArea/', views.Ajax_GetArea.as_view(),
         name='u_RegisterUser/Ajax_GetArea'),  # 同じajaxは他でも使用する
    path('u_RegisterUser/Ajax_CheckUserMail/', views.Ajax_CheckUserMail.as_view(),
         name='u_Register/User_Ajax_CheckUserMail'),

    path('u_Quit/', views.U_QuitView.as_view(), name='u_Quit'),

    path('u_RegisterProduct/', views.U_RegisterProductView.as_view(),
         name='u_RegisterProduct'),
    path('u_RegisterProduct/Ajax_GetArea/', views.Ajax_GetArea.as_view(),
         name='u_RegisterProduct/Ajax_GetArea'),  # 同じajaxは他でも使用する
    path('u_RegisterProduct/Ajax_GetStore/', views.Ajax_GetStore.as_view(),
         name='Ajax_GetStore'),

    path('u_RegisterProduct/Ajax_SearchStoreName/', views.Ajax_SearchStoreName.as_view(),
         name='Ajax_SearchStoreName'),
    path('u_RegisterProduct/Ajax_SearchStoreAddress/', views.Ajax_SearchStoreAddress.as_view(),
         name='Ajax_SearchStoreAddress'),


    path('u_RegisterProduct/Ajax_CheckStore/', views.Ajax_CheckStore.as_view(),
         name='Ajax_CheckStore'),
    path('u_RegisterProduct/Ajax_CheckSimilarStoreInfo/', views.Ajax_CheckSimilarStoreInfo.as_view(),
         name='Ajax_CheckSimilarStoreInfo'),
    path('u_RegisterProduct/Ajax_RegisterStoreInfo/', views.Ajax_RegisterStoreInfo.as_view(),
         name='Ajax_RegisterStoreInfo'),

    path('u_RegisterProduct/Ajax_CheckItem/', views.Ajax_CheckItem.as_view(),
         name='Ajax_CheckItem'),
    path('u_RegisterProduct/Ajax_CheckSimilarItemInfo/', views.Ajax_CheckSimilarItemInfo.as_view(),
         name='Ajax_CheckSimilarItemInfo'),
    path('u_RegisterProduct/Ajax_RegisterItemInfo/', views.Ajax_RegisterItemInfo.as_view(),
         name='Ajax_RegisterItemInfo'),

    path('u_StoreInfo/<int:store_id>', views.U_StoreInfoView.as_view(),
         name='u_StoreInfo'),
    path('u_StoreInfo/Ajax_GetArea/', views.Ajax_GetArea.as_view(),
         name='u_StoreInfo/Ajax_GetArea'),
    path('u_StoreInfo/Ajax_CheckStore/', views.Ajax_CheckStore.as_view(),
         name='u_StoreInfo/Ajax_CheckStore'),
    path('u_StoreInfo/Ajax_CheckSimilarStoreInfo/', views.Ajax_CheckSimilarStoreInfo.as_view(),
         name='u_StoreInfo/Ajax_CheckSimilarStoreInfo'),

    path('u_ChangeInfo/', views.U_ChangeInfoView.as_view(), name='u_ChangeInfo'),
    path('u_ChangeInfo/Ajax_GetUserBirthday/',
         views.Ajax_GetUserBirthday.as_view(), name='Ajax_GetUserBirthday'),
    path('u_ChangeInfo/Ajax_CheckUserMail/', views.Ajax_CheckUserMail.as_view(),
         name='u_ChangeInfo_Ajax_CheckUserMail'),
    path('u_ChangeInfo/Ajax_GetArea/', views.Ajax_GetArea.as_view(),
         name='u_ChangeInfo/Ajax_GetArea'),  # 同じajaxは他でも使用する
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

    path('u_Inquiry/', views.U_InquiryView.as_view(),
         name='u_Inquiry'),

]
