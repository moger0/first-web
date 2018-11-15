from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index,name="myadmin_index"),
    url(r'^user/add/$',views.useradd,name="myadmin_user_add"),
    url(r'^user/userlist$',views.userlist,name="myadmin_user_list"),
     url(r'^user/del/([0-9]+)/$', views.userdel,name="myadmin_user_del"),
    url(r'^user/edit/([0-9]+)/$', views.useredit,name="myadmin_user_edit"),
]