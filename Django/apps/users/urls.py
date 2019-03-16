from django.urls import path, re_path

from . import views

# 正在部署的应用的名称
app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    re_path(r'^userinfo/(?P<pk>\d+)/$', views.userinfo, name='userinfo'),
    re_path(r'^user/(?P<pk>\d+)/pwdchange/$', views.pwd_change, name='pwd_change'),
    path('logout/', views.logout, name='logout'),
    path('upload/', views.upload, name='upload'),
    path('editUserInfo/', views.edit_userinfo, name='edit_userinfo'),
    path('addUser/', views.adduser, name='adduser'),
    path('updateUser/', views.updateuser, name='updateuser')
]
