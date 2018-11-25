from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from myadmin import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.urlresolvers import reverse

# Create your views here.

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
    # 接收id
    cid = request.GET.get('cid')
    # 删数据
    ob = models.Cart.objects.get(id=cid)
    ob.delete()
    return JsonResponse({'error':1})

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