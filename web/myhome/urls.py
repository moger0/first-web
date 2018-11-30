from django.conf.urls import url
from . import views
import myhome
urlpatterns = [
    # 首页
    url(r'^$',views.index,name="myhome_index"),

    url(r'^goods/list/$',views.goodslist,name="myhome_list"),
    url(r'^goods/info/$',views.goodsinfo,name="myhome_info"),
    url(r'^login/$',views.login,name="myhome_login"),
    url(r'^loginout/$',views.loginout,name="myhome_loginout"),
    url(r'^register/$',views.register,name="myhome_register"),
    url(r'^checkregister/$',views.checkregister,name="myhome_checkregister"),
    # 短信验证
    url(r'^sendmsg/$',views.sendmsg,name="sendmsg"),

    # 购物车
    url(r'^cart/$',views.goodscart,name="myhome_cart"),
    url(r'^cartadd/$',views.goodscartadd,name="myhome_cartadd"),
    url(r'^cartedit/$',views.goodscartedit,name="myhome_cartedit"),
    url(r'^cartdel$',views.goodscartdel,name="myhome_cartdel"),

    # 订单
    url(r'^order/$',views.goodsconfirm,name="myhome_order"),
    url(r'^ordertolist/$',views.ordertolist,name="myhome_ordertolist"),

    # 获取地址
    url(r'^address/$',views.goodscitys,name="myhome_citys"),
    url(r'^addressdel/$',views.addressdel,name="myhome_adddel"),
    url(r'^addressedit/$',views.addressedit,name="myhome_addedit"),
    # 存地址
    url(r'^saveadd/$',views.saveadd,name="myhome_saveadd"),

    # 提交订单生成订单
    url(r'^orderconfirm/$',views.orderconfirm,name="myhome_ordconfirm"),

    # 个人中心
    url(r'^information/$',views.information,name="myhome_information"),
    url(r'^upaddresslist/$',views.upaddresslist,name="myhome_upaddresslist"),

     # 地址管理
    url(r'^addresslist/$',views.addresslist,name="addresslist"),
    # 地址添加
    url(r'^address/$',views.myhomeaddress,name="myhome_addresss"),
    # 修改地址
    url(r'^addressedit/$',views.addressedit,name="addressedit"),
    # 删除地址
    url(r'^deladdress/$',views.myhomedeladdress,name="myhome_deladdress"),
    # 修改默认地址
    url(r'^defaultedit/$',views.myhomedefaultedit,name="myhome_defaultedit"),
    # 接收地址栏数据
    url(r'^addressadd/$',views.myhomeaddressadd,name="myhome_addresssadd"),

     # 订单管理
    url(r'^ordero/$',views.myhomeordero,name="myhome_ordero"),
    url(r'^orderdel/$',views.orderodel,name="myhome_orderdel"),

]

handler404 = myhome.views.page_not_found #改动2