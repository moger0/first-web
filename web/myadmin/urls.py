from django.conf.urls import url
from . views import viewsIndex,viewsUsers,viewsCates,viewsGoods

urlpatterns = [
    url(r'^$',viewsIndex.index,name="myadmin_index"),
    url(r'^user/add/$',viewsUsers.useradd,name="myadmin_user_add"),
    url(r'^user/userlist/$',viewsUsers.userlist,name="myadmin_user_list"),
     url(r'^user/del/([0-9]+)/$', viewsUsers.userdel,name="myadmin_user_del"),
    url(r'^user/edit/([0-9]+)/$', viewsUsers.useredit,name="myadmin_user_edit"),

    # 商品分类
    url(r'^cates/add/$',viewsCates.catesadd,name="myadmin_cates_add"),
    url(r'^cates/list/$',viewsCates.cateslist,name="myadmin_cates_list"),
    url(r'^cates/del/$',viewsCates.catesdel,name="myadmin_cates_del"),
    url(r'^cates/edit/$',viewsCates.catesedit,name="myadmin_cates_edit"),
    
]