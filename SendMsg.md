更新:
    在python3中导入urllib模板,并使用urllib.request时可能会产生一个bug
    AttributeError: module 'urllib' has no attribute 'request'
    
    解决方案,重新导入urllib.request
    import urllib
    import urllib.request
    import json
    import random


手机短信验证码
    互亿无线
    1,注册,登录
        http://www.ihuyi.com

        文档地址
        http://www.ihuyi.com/api/sms.html


    2,定义url路由和视图函数
        注意,把代码中的 APIID,APIKEY

    url(r'^sendmsg/$',  views.sendmsg,name="sendmsg"),

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
        account  = "C04988412" 
        #密码 查看密码请登录用户中心->验证码、通知短信->帐户及签名设置->APIKEY
        password = "ca70bbd0206045c57873b014d5e9891f"
        mobile = request.GET.get('phone')
        # 随机验证码
        code = str(random.randint(10000,99999))
        # 把验证码存入session
        request.session['msgcode'] = code
        text = "您的验证码是："+code+"。请不要把验证码泄露给其他人。"
        data = {'account': account, 'password' : password, 'content': text, 'mobile':mobile,'format':'json' }
        req = urllib.request.urlopen(
            url= 'http://106.ihuyi.com/webservice/sms.php?method=Submit',
            data= urllib.parse.urlencode(data).encode('utf-8')
        )
        content =req.read()
        res = json.loads(content.decode('utf-8'))
        print(res)
        return HttpResponse(res)


    3,修改注册的页面,加短信发送功能