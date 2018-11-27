from django.conf.urls import url
from . views import viewsIndex,viewsUsers,viewsCates,viewsGoods,viewsBeiHuan,viewsOrder

urlpatterns = [
    # 首页
    url(r'^$',viewsIndex.index,name="myadmin_index"),

    # 登录
    url(r'^login/$',viewsIndex.login,name="myadmin_login"),
    url(r'^loginout/$',viewsIndex.loginout,name="myadmin_loginout"),
    url(r'^verifycode/$',viewsIndex.verifycode,name="myadmin_code"),

    # 用户管理
    url(r'^user/add/$',viewsUsers.useradd,name="myadmin_user_add"),
    url(r'^user/userlist/$',viewsUsers.userlist,name="myadmin_user_list"),
     url(r'^user/del/([0-9]+)/$', viewsUsers.userdel,name="myadmin_user_del"),
    url(r'^user/edit/([0-9]+)/$', viewsUsers.useredit,name="myadmin_user_edit"),

    # 商品分类
    url(r'^cates/add/$',viewsCates.catesadd,name="myadmin_cates_add"),
    url(r'^cates/list/$',viewsCates.cateslist,name="myadmin_cates_list"),
    url(r'^cates/del/$',viewsCates.catesdel,name="myadmin_cates_del"),
    url(r'^cates/edit/$',viewsCates.catesedit,name="myadmin_cates_edit"),
    
    # 商品管理
    url(r'^goods/add/$',viewsGoods.goodsadd,name="myadmin_goods_add"),
    url(r'^goods/insert/$',viewsGoods.goodsinsert,name="myadmin_goods_insert"),
    url(r'^goods/list/$',viewsGoods.goodslist,name="myadmin_goods_list"),
    url(r'^goods/del/$',viewsGoods.goodsdel,name="myadmin_goods_del"),
    url(r'^goods/edit/$',viewsGoods.goodsedit,name="myadmin_goods_edit"),

    # 数据备份与还原
    url(r'^mysqlbeifen/$',viewsBeiHuan.sqlbeifen,name="sqlbeifen"),
    url(r'^mysqlhuanyuan/$',viewsBeiHuan.sqlhuanyuan,name="sqlhuanyuan"),

    # 订单管理
    url(r'^order/list/$',viewsOrder.orderlist,name="myadmin_orderlist"),
    url(r'^order/del/$',viewsOrder.orderdel,name="myadmin_orderdel"),
    url(r'^order/edit/$',viewsOrder.orderedit,name="myadmin_orderedit"),

    # 404
    url(r'^404/$',viewsIndex.index404,name="myadmin_index404"),

]