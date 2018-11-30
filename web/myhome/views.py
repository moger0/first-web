from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from myadmin import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.urlresolvers import reverse
import json


# Create your views here.

def page_not_found(request):
    return render_to_response('404.html')

def index(request):
    # 查找所有顶级分类
    ob = models.Cates.objects.filter(pid=0)
    for i in ob: # {name:手机,sub:[子分类]}
        i.sub = models.Cates.objects.filter(pid=i.id)

    # [
    #     1.{name:手机,sub:[{name:魅蓝,subs:[goodslist],subs:[goodslist]}]}
    #     2.{
    #         name:只能设备,
    #         sub:[goodslist]
    #     }
    # ]
    # 循环: name 手机/智能设备
    #         sub name 魅蓝 魅族
    #                 subs 商品
    return render(request,'myhome/index.html',{'data':ob})

def goodslist(request):
    # 接收商品类别id
    cid = request.GET.get('id')
    ctype = models.Cates.objects.get(id=cid)
    # 获取所有的同类型
    types = models.Cates.objects.filter(pid=ctype.pid)
    data = ctype.goods_set.all().filter(gnum__gt=0)
    if request.GET.get('new') == 'status':
        data = ctype.goods_set.all().filter(gnum__gt=0).filter(status=0).order_by('-adddtime')
    elif request.GET.get('new') == 'price':
        data = ctype.goods_set.all().filter(gnum__gt=0).order_by('-price')

    return render(request,'myhome/list.html',{'data':data,'ctype':ctype,'types':types})

def goodsinfo(request):
    # 接收商品的id
    gid = request.GET.get('id')
    data = models.Goods.objects.get(id=gid)

    return render(request,'myhome/info.html',{'data':data})

def login(request):
    if request.method=='GET':
        return render(request,'myhome/login.html')
    elif request.method=='POST':
        # 接收用户信息
        userinfo = request.POST.dict()
        try:
            # 判断
            ob = models.Users.objects.get(phone=userinfo['phone'])
            # upass = check_password(userinfo['password'],ob.password)
            if ob and userinfo['password']==ob.password :
                request.session['vipuser']={'username':ob.username,'phone':ob.phone,'pic_url':ob.pic_url}
                # return render(request,'{myhome/index.html}')
                return HttpResponse('<script>alert("登陆成功");location.href="'+reverse('myhome_index')+'"</script>')
            else:
                return HttpResponse('<script>alert("用户名或密码错误");history.back(-1);</script>')
        except:
            return HttpResponse('<script>alert("用户名不存在");history.back(-1);</script>')
    

def loginout(request):
    del request.session['vipuser']
    return HttpResponse('<script>alert("退出成功");location.href="/"</script>')

def register(request):
    if request.method=="GET":
        return render(request,'myhome/register.html')
    elif request.method=="POST":
        # 接收用户数据
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        # 判断用户名是否可用
        if request.session['msgcode']['code']==data['code'] and request.session['msgcode']['phone']==data['phone']:
            # data['password']=make_password(data['password'],None,'pbkdf2_sha256')
            info={'username':'user'+data['phone'],'phone':data['phone'],'password':data['password'],'pic_url':'/static/pics/user.jpg'}
            ob = models.Users(**info)
            ob.save()

            # 返回 跳转到登录页面
            return HttpResponse('<script>alert("注册成功");location.href="'+reverse('myhome_login')+'"</script>')
        else:
            return HttpResponse('<script>alert("验证错误");location.href="'+reverse('myhome_register')+'"</script>')


def checkregister(request):
    # 获取提交的用户名
    p = request.GET.get('phone')
    # 根据用户查询数据
    ob = models.Users.objects.filter(phone=p)
    if ob:
        # 如果查询到数据用户名已经被注册
        return JsonResponse({"error":0,'msg':'用户名已被注册'})
    else:
        return JsonResponse({"error":1,'msg':'用户名可用'})

def goodscart(request):
    if request.session['vipuser']['phone']:
        # 查询数据库的数据
        userphone = request.session['vipuser']['phone']
        user = models.Users.objects.get(phone=userphone)
        print(user.id)
        goods = user.cart_set.all()

        # 去购物车库拿当前用户对应的商品
        # g = models.Cart.filter(uid=user.id)
        return render(request,'myhome/cart.html',{'data':goods})

def goodscartedit(request):
    # 接收数据 并修改 
    data = request.GET.dict()
    user = models.Users.objects.get(phone=request.session['vipuser']['phone'])
    good = models.Goods.objects.get(id=data['gid'])
    # 修改数据
    goods = models.Cart.objects.filter(uid=user).filter(gid=good)
    # 查询集更新数据时必须遍历更新
    pricesum = 0
    for i in goods:
        i.gnum = data['num']
        i.save()
        cid = i.id
        pricesum = float(i.gnum)*float(i.gid.price)

    return JsonResponse({'error':1,'pricesum':pricesum,'cid':cid})

# 删除购物车数据
def goodscartdel(request):
    try:
        # 接收id
        cid = request.GET.get('cid')
        # 删数据
        ob = models.Cart.objects.get(id=cid)
        ob.delete()
        return JsonResponse({'error':1})
    except:
        return JsonResponse({'error':0})

# 购物车
def goodscartadd(request):
    # 接收用户id 商品id
    data = request.GET.dict()
    user = models.Users.objects.get(phone=data['phone'])
    goods = models.Goods.objects.get(id=data['gid'])
    ob = models.Cart.objects.filter(uid=user).filter(gid=goods)
    # 判断有没有这个商品
    # print(ob.count()) # <query [{},{}]>
    # 查询集两大特性
    # (1)惰性执行：创建查询集不会访问数据库，直到调用数据时，才会访问数据库，调用数据的情况包括迭代、序列化、与if合用。
    # (2)缓存：使用同一个查询集，第一次使用时会发生数据库的查询，然后把结果缓存下来，再次使用这个查询集时会使用缓存的数据。
    # 对查询集进行切片后返回一个新的查询集，不会立即执行查询。
    # 如果获取一个对象，直接使用[0]，等同于[0:1].get()，但是如果没有数据，[0]引发IndexError异常
    try:
        if ob:
            for i in ob:
                i.gnum = i.gnum+int(data['num'])
            ob[0].save()
        else:
            car = models.Cart()
            car.uid = user
            car.gid = goods
            car.gnum = int(data['num'])
            car.save()
     # 添加一条数据 添加cart 并关联商品
    # c = models.Cart()
    # c.gnum = 10
    # c.uid =  models.Users.objects.get(id=1)
    # c.gid =  models.Goods.objects.get(id=3)
    # c.save()
   
   # 通过cart查用户
    # car = models.Cart.objects.get(id=9)
    # print(car.uid.username)
    # 通过用户查cart
    # user = models.Users.objects.get(id=1)
    # print(user.cart_set.all().values())
        return JsonResponse({'error':1})
    except:
        return JsonResponse({'error':0})


# 确认订单页
def goodsconfirm(request):
    # 获取用于提交的id
    res = request.GET.get('cid')
    clist = res.split(',')
    # 查询数据
    data = models.Cart.objects.filter(id__in=clist)
    # 查地址
    user = models.Users.objects.get(phone=request.session['vipuser']['phone'])
    # 当前用户有多少个地址
    address = models.Address.objects.filter(uid=user.id)
    # 蒋数据序列化 [{},{}]
    adds = list(address.values())
    # 循环每一条数据 通过县乡 找到对应的省和市
    for i in adds:
        xq = models.Citys.objects.get(id=i['zhen_id'])
        shi = models.Citys.objects.get(id=xq.upid)
        sheng = models.Citys.objects.get(id=shi.upid)
        i['shi'] = shi.name
        i['sheng'] = sheng.name
        i['zhen_id'] = xq.name
    print(adds)
    # 查询一级城市数据
    citys = models.Citys.objects.filter(level = 1)
    return render(request,'myhome/confirm.html',{'data':data,'citys':citys,'address':adds})

# 订单列表
def ordertolist(request):
    
    return render(request,'myhome/ordertolist.html')

# 删除订单数据
def orderodel(request):
    try:
        # 接收id
        cid = request.GET.get('cid')
        print(cid)
        # 删数据
        ob = models.Order.objects.filter(id=cid)
        print(ob)
        for i in ob:
            i.status = 4
            print(i.status)
            i.save()
        return JsonResponse({'error':1})
    except:
        return JsonResponse({'error':0})


# 获取地址
def goodscitys(request):
    # 获取用户提交的数据
    uid = request.GET.get('upid')
    # 查询数据
    data = models.Citys.objects.filter(upid=uid).values()
    # 返回数据
    return JsonResponse(list(data),safe=False)

def addressdel(request):
    # 接收id
    cid = request.GET.get('cid')
    # 删数据
    ob = models.Address.objects.get(id=cid)
    ob.delete()
    return JsonResponse({'error':1})

def addressedit(request):
    cid = request.GET.get('cid')
    ob = models.Address.objects.get(id=cid)
    return JsonResponse(ob,safe=False)

# 添加地址
def saveadd(request):
    # 获取用户数据
    data = request.GET.dict()
    try:
        # 存储数据
        ob = models.Address()
        ob.uid = models.Users.objects.get(phone=request.session['vipuser']['phone'])
        ob.name = data['name']
        ob.phone = data['phone']
        ob.zhen = models.Citys.objects.get(id=data['citys'])
        ob.info = data['info']
        ob.save()
        return JsonResponse({'error':1})
    except:
        return JsonResponse({'error':0})

# 生成订单
def orderconfirm(request):
    # 获取用户的数据
    orderdata = request.POST.dict()
    orderdata.pop('csrfmiddlewaretoken')
    # 获取用户对象
    orderdata['uid']=models.Users.objects.get(phone=request.session['vipuser']['phone'])
    # 地址
    address = models.Address.objects.get(id=orderdata['addrid'])
    xq = models.Citys.objects.get(id=address.zhen_id)
    shi = models.Citys.objects.get(id=xq.upid)
    sheng = models.Citys.objects.get(id=shi.upid)
    # print(xq.name,shi.name,sheng.name)
    orderdata['addr']=sheng.name+shi.name+xq.name+address.info

    # 总价格
    res = orderdata['cid'].split(',')
    # 查询数据
    goos = models.Cart.objects.filter(id__in=res)
    pricesume = 0
    for i in goos:
        pricesume += i.gnum*i.gid.price

    orderdata['price']=pricesume

    # 删除不需要的数据
    orderdata.pop('cid')
    orderdata.pop('addrid')
    print(orderdata,res)
    # 添加数据
    order = models.Order(**orderdata)
    order.save()

    # 添加订单详情 一个订单有多个商品 一个商品就是一个订单详情 
    for i in res:
        orderinfo = models.Orderinfo() 
        orderinfo.ordid = order
        goods = models.Cart.objects.get(id=i)
        orderinfo.gid = goods.gid.id
        orderinfo.title = goods.gid.title
        orderinfo.num = goods.gnum
        orderinfo.pic_url = goods.gid.pic_url
        orderinfo.save()

        # 删除购物车里的东西
        goods.delete()

    # return HttpResponse('支付页面')
    return HttpResponse('<script>alert("订单创建成功,确定返回主页");location.href="'+reverse('myhome_index')+'"</script>')


def information(request):
    if request.method == 'GET':
        phone = request.session['vipuser']['phone']
        user = models.Users.objects.get(phone=phone)
        return render(request,'myhome/information.html',{'ob':user})
    elif request.method == 'POST':
        phone = request.session['vipuser']['phone']
        user = models.Users.objects.get(phone=phone)
        data = request.POST.dict()
        myfiles = request.FILES.get("pic_url")
        # 'name': '', 'sex': '1', 'phone': '', 'email': '', 'age': ''}
        if data['username']:
            user.username = data['username']
        if data['phone']:
            user.phone = data['phone']
        if data['email']:
            user.email = data['email']
        if data['age']:
            user.age = data['age']
        if myfiles:
            if user.pic_url!="/static/pics/user.jpg":
                delpic(user.pic_url)
            user.pic_url = upload(myfiles)
        user.sex = data['sex']
        user.save()
        print(user.pic_url)
        return HttpResponse('<script>alert("修改成功");location.href="'+reverse('myhome_information')+'"</script>')


def upaddresslist(request):
    # 查地址
    user = models.Users.objects.get(phone=request.session['vipuser']['phone'])
    # 当前用户有多少个地址
    address = models.Address.objects.filter(uid=user.id)
    # 蒋数据序列化 [{},{}]
    adds = list(address.values())
    # 循环每一条数据 通过县乡 找到对应的省和市
    for i in adds:
        xq = models.Citys.objects.get(id=i['zhen_id'])
        shi = models.Citys.objects.get(id=xq.upid)
        sheng = models.Citys.objects.get(id=shi.upid)
        i['shi'] = shi.name
        i['sheng'] = sheng.name
        i['zhen_id'] = xq.name
    print(adds)
    # 查询一级城市数据
    citys = models.Citys.objects.filter(level = 1)
    return render(request,'myhome/address.html',{'citys':citys,'address':adds})


def upload(myfile):
    #执行图片的上传
    filename = str(time.time())+"."+myfile.name.split('.').pop()
    destination = open("./static/pics/"+filename,"wb+")
    for chunk in myfile.chunks():      # 分块写入文件  
        destination.write(chunk)  
    destination.close()
    # /static/picsn/图片
    return '/static/pics/'+filename

def delpic(pic_url):
    if pic_url!='/static/pics/user.jpg':
        os.remove(BASE_DIR+pic_url)
    return




# 短信
def sendmsg(request):
    #接口类型：互亿无线触发短信接口，支持发送验证码短信、订单通知短信等。
    #账户注册：请通过该地址开通账户http://user.ihuyi.com/register.html
    #注意事项：
    #（1）调试期间，请用默认的模板进行测试，默认模板详见接口文档；
    #（2）请使用 用户名 及 APIkey来调用接口，APIkey在会员中心可以获取；
    #（3）该代码仅供接入互亿无线短信接口参考使用，客户可根据实际需要自行编写；
      
    # import urllib2
    import urllib
    import urllib.request
    import json
    import random
    #用户名 查看用户名请登录用户中心->验证码、通知短信->帐户及签名设置->APIID
    account  = "C96067353" 
    #密码 查看密码请登录用户中心->验证码、通知短信->帐户及签名设置->APIKEY
    password = "a8de9ce07d9d5bcabe337b9c6880304b"
    mobile = request.GET.get('phone')
    # 随机验证码
    code = str(random.randint(10000,99999))
    # 把验证码存入session
    request.session['msgcode'] = {'code':code,'phone':mobile}
    text = "您的验证码是："+code+"。请不要把验证码泄露给其他人。"
    data = {'account': account, 'password' : password, 'content': text, 'mobile':mobile,'format':'json' }
    # req = urllib.request.urlopen(
    #     url= 'http://106.ihuyi.com/webservice/sms.php?method=Submit',
    #     data= urllib.parse.urlencode(data).encode('utf-8')
    # )
    # content =req.read()
    # res = json.loads(content.decode('utf-8'))
    # print(res)
    return HttpResponse(res)



    # 添加地址弹框
def myhomeaddress(request):
    cid = request.GET.get('cid')
    cob = models.Citys.objects.filter(upid=cid).values()
    return JsonResponse(list(cob),safe=False)

# 接收地址栏数据
def myhomeaddressadd(request):
    try:
        data = request.GET.dict()
        data['uid'] =  models.Users.objects.get(phone=request.session['vipuser']['phone'])
        data['city'] = models.Citys.objects.get(id=data['city'])
        ob = models.Address(**data)
        ob.save()
        area = upaddress(ob.city.id)
        area['id'] = str(ob.id)
        print(area)
        return JsonResponse({'error':1,'area':area})
    except:
        return JsonResponse({'error':0})

# 更改地址
def addressedit(request):
    if request.method == "GET":
        aid = request.GET.get('aid')
        aob = models.Address.objects.filter(id=aid).values()[0]
        ob = upaddress(str(aob['zhen_id']))
        aob.update(ob)
        return JsonResponse({'error':0,'aob':aob})
    elif request.method == 'POST':
        data = request.POST.dict()
        city = models.Citys.objects.get(id=data['quxian'])
        aob = models.Address.objects.get(id=data['aid'])
        aob.name = data['name']
        aob.phone = data['phone']
        aob.city = city
        aob.info = data['info']
        aob.save()
        return HttpResponse('<script>alert("修改成功");location.href="'+reverse('addresslist')+'"</script>')

# 更改默认地址
def myhomedefaultedit(request):
    try:
        aid = request.GET.get('aid')
        address = models.Address.objects.get(id=aid)
        user = address.uid
        ads = user.address_set.all()
        for i in ads:
            i.isselect = False
            i.save()
        address.isselect = True
        address.save()
        return JsonResponse({'error':0})
    except:
        return JsonResponse({'error':1})

# 地址管理
def addresslist(request):
    if request.method == 'GET':
        phone = request.session['vipuser']['phone']
        user = models.Users.objects.get(phone=phone)
        ob = list(user.address_set.all().values())
        for i in ob:
            data = upaddress(i['zhen_id'])
            i.update(data)
        address = models.Citys.objects.filter(upid=0)
        addresss = models.Citys.objects.filter(level=2)
        addresst = models.Citys.objects.filter(level=3)
        return render(request,'myhome/address1.html',{'ob':ob,'address':address,'addresss':addresss,'addresst':addresst})

# 地址删除
def myhomedeladdress(request):
    try:
        cid = request.GET.get('aid')
        ob = models.Address.objects.get(id=cid)
        ob.delete()
        return JsonResponse({'error':0})
    except:
        return JsonResponse({'error':1})

# 通过县区的id获取相应的市和省份和区县的名称
def upaddress(cid):
    data={}
    xq = models.Citys.objects.get(id=cid)
    shi = models.Citys.objects.get(id=xq.upid)
    sheng = models.Citys.objects.get(id=shi.upid)
    data['shi'] = shi.name
    data['sheng'] = sheng.name
    data['xq'] = xq.name
    data['shiid'] = shi.id
    data['shengid'] = sheng.id
    data['xqid'] = xq.id
    return data

# 订单管理
def myhomeordero(request):
    user = models.Users.objects.get(phone=request.session['vipuser']['phone'])
    order = user.order_set.all()
    order0 = order.all()
    order1 = order.filter(status=0)
    order2 = order.filter(status=1)
    order3 = order.filter(status=2)
    order4 = order.filter(status=3)
    order5 = order.filter(status=4)
    order6 = order.filter(status=5)

    # print(order0)
    # print(order1)
    # print(order2)
    # print(order3)
    # print(order4)
    return render(request,'myhome/ordero.html',{'order0':order0,'order1':order1,'order2':order2,'order3':order3,'order4':order4,'order5':order5,'order6':order6})