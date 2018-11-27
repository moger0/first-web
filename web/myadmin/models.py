from django.db import models

# Create your models here.
class Users(models.Model):
    # 会员 姓名 密码 手机号 邮箱 性别 年龄 状态 path 注册时间
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=30)
    phone=models.CharField(max_length=11)
    email=models.CharField(max_length=30,null=True)
    age=models.IntegerField()
    sex=models.CharField(max_length=1,choices=(('1','男'),('0','女')))
    pic_url=models.CharField(max_length=255)
    status=models.IntegerField(default=0)
    addtime=models.DateTimeField(auto_now_add=True)


# 商品分类
class Cates(models.Model):
    # id    name    pid     path
    # 1     服装      0       0,
    # 2     家电      0       0,
    # 3     男装      1       0,1,
    # 4     正装      3       0,1,3,
    # 5     女装      1       0,1,
    # 6     热裤      5       0,1,5,
    # 7     电视      2       0,2,
    # 8     西裤      4       0,1,3,4
    name = models.CharField(max_length=30)
    pid = models.IntegerField()
    path = models.CharField(max_length=30)
    isDelete = models.BooleanField(default=True)

    def __str__(self):
        return self.path


# 商品管理
class Goods(models.Model):
    # id 标题 外键 图片 数量 价格 状态 简介 销售量 点击量 添加时间
    title = models.CharField(max_length=70)
    cateid = models.ForeignKey(to='Cates')

    pic_url = models.CharField(max_length=200)
    gnum = models.IntegerField()
    price = models.FloatField()
    status = models.IntegerField(default=0)
    info = models.TextField(max_length=255)

    ordernum = models.IntegerField(default=0)
    clicknum = models.IntegerField(default=0)

    adddtime = models.DateTimeField(auto_now_add=True)

class Cart(models.Model):
    # id uid gid gnum
    uid = models.ForeignKey(to='Users')
    gid = models.ForeignKey(to='Goods')
    gnum = models.IntegerField()

class Address(models.Model):
    # uid 省 市 县/区 收货人 联系方式 详细地址
    uid = models.ForeignKey(to="Users")
    name = models.CharField(max_length=10)
    phone = models.CharField(max_length=11)

    # sheng = models.ForeignKey(to='Citys')
    # shi = models.ForeignKey(to='Citys')
    zhen =  models.ForeignKey(to="Citys")

    info = models.CharField(max_length=255)

    isselect = models.BooleanField(default=0)


class Citys(models.Model):
    name = models.CharField(max_length=30)
    level = models.IntegerField()
    upid = models.IntegerField()


# 订单
  #id uid  地址   物流信息 支付信息 状态
  # 1  1   地址 
class Order(models.Model):
    uid = models.ForeignKey(to="Users")
    addr = models.CharField(max_length=255)
    wl = models.CharField(max_length=50)
    paytype = models.CharField(max_length=30)
    price = models.IntegerField(default=0)
    # 0 未付款 1已付款 2未发货 3已发货 
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)

# 订单详情
  # orderid gid   商品标题 购买数量 
class Orderinfo(models.Model):
    ordid = models.ForeignKey(to="Order")
    gid = models.IntegerField()
    title = models.CharField(max_length=100)
    num = models.IntegerField()
    pic_url = models.CharField(max_length=100)