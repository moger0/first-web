from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$',views.index,name="myhome_index"),

    url(r'^goods/list/$',views.goodslist,name="myhome_list"),
    url(r'^goods/info/$',views.goodsinfo,name="myhome_info"),
    url(r'^login/$',views.login,name="myhome_login"),
    url(r'^loginout/$',views.loginout,name="myhome_loginout"),
    url(r'^register/$',views.register,name="myhome_register"),
    url(r'^checkregister/$',views.checkregister,name="myhome_checkregister"),
    # 短信验证
    url(r'^sendmsg/$',views.sendmsg,name="sendmsg"),

    url(r'^cart/$',views.goodscart,name="myhome_cart"),
    url(r'^cartadd/$',views.goodscartadd,name="myhome_cartadd"),
    url(r'^cartedit/$',views.goodscartedit,name="myhome_cartedit"),
    url(r'^cartdel$',views.goodscartdel,name="myhome_cartdel"),
]