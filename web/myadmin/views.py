from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from django.core.urlresolvers import reverse
import time,os
from . import models
from web.settings import BASE_DIR
from django.core.paginator import Paginator
from django.db.models import Q

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
    keywords = request.GET.get('keywords','')
    types = request.GET.get('types','')
    search={'keywords':keywords,'types':types}
    # 判断有没有条件查询
    if types:
        # 判断有没有搜索类型
        if types == 'all':
            # sql
            # select * from users where usernamelike %keywords% or email like %keywords%
            # models.Users.objects.filter(username__contains='123',email__contains='123')
            # data = models.Users.objects.filter(username__contains='123')
            # data.filter(email__contains='123')
            key={'男':'1','女':'0'}
            data = data.filter(Q(username__contains=keywords)|Q(phone__contains=keywords)|Q(email__contains=keywords)|Q(age__contains=keywords)|Q(sex__contains=key[keywords])|Q(status__contains=keywords))
            return fpage(request,data,search)
        elif types == 'sex':
            key={'男':'1','女':'0'}
            data = data.filter(sex__contains=key[keywords])
            return fpage(request,data,search)
        else:
            # data = models.Users.objects.filter(username__contains=keywords)
            t = {types+'__contains':keywords}
            data = data.filter(**t)
            return fpage(request,data,search)
    else:
        return fpage(request,data,search)

    


def fpage(request,data,search):
    # 数据分页
    # 实例化分页类 第一个参数所有的数据集合 每页要显示的条数
    p = Paginator(data,5)
    # 统计所有的数据
    # sum_data=p.count
    # 获取可以分多少页
    page_num = p.num_pages
    # 分页的范围 range(1,)
    pagenums = p.page_range

    # 接收页码
    pg = int(request.GET.get('p',1))
    # 判断当前页码不能小于1
    if pg<1:
        pg=1
    if pg>page_num:
        pg=page_num
    # 获取第几页的数据
    pagedata = p.page(pg)
    # 限制边界 如果当前页码小于或=3 只取前五条数据
    if pg <= 3:
        pag_list = pagenums[:5]
    elif pg+2 > page_num:
        pag_list = pagenums[-5:]
    else:
        pag_list = pagenums[pg-3:pg+2]
    print(pag_list)

    return render(request,'myadmin/user/userlist.html',{"info":pagedata,'pagenums':pag_list,'pg':pg,'search':search})


# 删除数据
def userdel(request,uid):
    ob=models.Users.objects.get(id=uid)
    pic_url=ob.pic_url
    delpic(pic_url)
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

def delpic(pic_url):
    if pic_url!='/static/pics/user.jpg':
        os.remove(BASE_DIR+pic_url)
    return
