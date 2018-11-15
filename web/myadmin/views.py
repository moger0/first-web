from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from django.core.urlresolvers import reverse
import time,os
from . import models
from web.settings import BASE_DIR

# Create your views here.
def index(request):
    return render(request,'myadmin/index.html')

# 添加数据
def useradd(request):
    if request.method=='GET':
        # 返回页面
        return render(request,'myadmin/user/add.html')
    elif request.method=='POST':
        try:
            data = request.POST.dict()
            data.pop('csrfmiddlewaretoken')
            # data['password']=make_password(data['pssword'],None,'pbkdf2_sha256')
            myfile = request.FILES.get("pic_url",None)
            # 判断图片有没有提交
            if myfile:
                pic=upload(myfile)
                data['pic_url']=pic
            else:
                data['pic_url']='/static/pics/user.jpg'
            # 存数据
            ob = models.Users(**data)
            ob.save()
            return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_user_list')+'"</script>')
        except:
            return HttpResponse('<script>alert("添加失败");location.href=""</script>')



# 查询所有用户
def userlist(request):
    data = models.Users.objects.all().exclude(status=3)
    return render(request,'myadmin/user/userlist.html',{"info":data})

# 删除数据
def userdel(request,uid):
    ob=models.Users.objects.get(id=uid)
    ob.status=3
    ob.save()
    return HttpResponse('<script>alert("删除成功");location.href="'+reverse('myadmin_user_list')+'"</script>')

# 修改数据
def useredit(request,uid):
    ob = models.Users.objects.get(id=uid)
    # 判断请求方式 GET通过链接访问都是get方式   a标签 url路由地址栏
    if request.method=='GET':
        # 查询数据
        return render(request,'myadmin/user/edit.html',{'info':ob})
    elif request.method=='POST':
        ob.username=request.POST.get('username')
        # 判断有没有提交密码 如果提交了就更新
        if request.POST.get('password'):
            ob.password=request.POST.get('password')
        ob.phone=request.POST.get('phone')
        ob.sex=request.POST.get('sex')
        ob.age=request.POST.get('age')
        ob.email=request.POST.get('email')
        # 判断有没有提交图像 如果提交了就吧原来的文件删除
        if request.FILES.get('pic_url'):
            # 删除原来的图片 /home/first-web//static/pics/图片
            # 判断是否用的是默认头像 如是不做删除
            if ob.pic_url!='/static/pics/user.jpg':
                os.remove(BASE_DIR+ob.pic_url)
            # 将提交上来的新图片写入到本地 并将地址入库 
            myfile = request.FILES.get('pic_url')
            ob.pic_url=upload(myfile)
        ob.save()

        return HttpResponse('<script>alert("修改成功");location.href="'+reverse('myadmin_user_list')+'"</script> ')


def upload(myfile):
    #执行图片的上传
    filename = str(time.time())+"."+myfile.name.split('.').pop()
    destination = open("./static/pics/"+filename,"wb+")
    for chunk in myfile.chunks():      # 分块写入文件  
        destination.write(chunk)  
    destination.close()
    # /static/picsn/图片
    return '/static/pics/'+filename