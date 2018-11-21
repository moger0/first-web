from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from myadmin import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
    return render(request,'myhome/index.html')

def goodslist(request):
    pass
    return render(request,'myhome/login.html')

def goodsinfo(request):
    pass
    return render(request,'myhome/login.html')

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
                return render(request,'myhome/index.html')
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