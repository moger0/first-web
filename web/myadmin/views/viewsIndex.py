from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from django.core.urlresolvers import reverse
import time,os
from .. import models
from web.settings import BASE_DIR
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request,'myadmin/index.html')

def index404(request):
    return render(request,'404.html')

def login(request):
    if request.method=="GET":
        # 返回登录页面
        return render(request,'myadmin/login.html')
    if request.method=="POST":
        # 获取用户提交的数据
        data = request.POST.dict()
        # 判断验证码
        if data['code'] != request.session['verifycode']:
            return HttpResponse('<script>alert("验证码有误");loaction.href="'+reverse('myadmin_login')+'"</script>')
        try:
            # 判断用户和密码
            if data['username'] == "admin" and data['password'] == "123456":
                request.session['admin']={'username':'admin'}
            # 跳转到首页
            return HttpResponse('<script>alert("登陆成功");location.href="'+reverse('myadmin_index')+'"</script>')
        except:
             return HttpResponse('<script>alert("登陆失败");location.href="'+reverse('myadmin_login')+'"</script>')



def loginout(request):
    request.session['admin']=''
    return HttpResponse('<script>alert("退出成功");location.href="'+reverse('myadmin_login')+'"</script>')


# 验证码
def verifycode(request):
    #引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    # str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    str1 = '123456789'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象
    font = ImageFont.truetype('FreeMono.ttf', 23)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    #内存文件操作
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


def upload(myfile):
    #执行图片的上传
    filename = str(time.time())+"."+myfile.name.split('.').pop()
    destination = open("./static/pics/"+filename,"wb+")
    for chunk in myfile.chunks():      # 分块写入文件  
        destination.write(chunk)  
    destination.close()
    # /static/picsn/图片
    return '/static/pics/'+filename

def limit(request,data,datanum,path):
     # 数据分页
    # 实例化分页类 第一个参数所有的数据集合 每页要显示的条数
    p = Paginator(data,datanum)
    # 统计所有的数据
    # sum_data=p.count
    # 获取可以分多少页 
    page_num=p.num_pages
    # 分页的范围 range(1,)
    pagenums = p.page_range
    
    # 接受页码
    pg = int(request.GET.get('p',1))
    # 判断当前页码不能小于1
    if pg<1:
        pg=1
    if pg>page_num:
        pg=page_num
    # 获取第几页的数据
    pagedata = p.page(pg)
    # 限制边界 如果当前页码小于或=3 只区前五条数据
    # 
    if pg <= 3:
        pag_list=pagenums[:5]
    elif pg+2> page_num:
         pag_list=pagenums[-5:]
    else:
        pag_list=pagenums[pg-3:pg+2]
    print(pag_list)

    return render(request,path,{"info":pagedata,'pagenums':pag_list,'pg':pg})