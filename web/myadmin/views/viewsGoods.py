from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
from .. import models
from django.core.urlresolvers import reverse
import time,os
from . viewsIndex import upload,limit
from web.settings import BASE_DIR
from django.core.paginator import Paginator
from django.db.models import Q

def goodsadd(request):
    # 查询商品类别
    cates = models.Cates.objects.extra(select = {'paths':'concat(path,id)'}).order_by('paths')
    return render(request,'myadmin/goods/add.html',{'info':cates})

def goodsinsert(request):
    # 获取用户数据
    data = request.POST.dict()
    # { 'gnum':'111','title':'111','price':'111','fname':'4','info':'' }
    data.pop('csrfmiddlewaretoken')
    print(data)
    # 添加数据
    ob=models.Goods()
    ob.title=data['title']
    ob.gnum=int(data['gnum'])
    ob.price=float(data['price'])
    ob.info=data['info']

    ob.cateid = models.Cates.objects.get(id=data['fname'])
    myfile = request.FILES.get('pic_url')
    if myfile:
        ob.pic_url = upload(myfile)
        ob.save()
        return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_goods_list')+'"</script>')
    else:
        return HttpResponse('<script>alert("必须选择商品图片");history.back(-1)</script>')


def goodslist(request):
    # 查询商品
    ob = models.Goods.objects.all()
    # 查询
    types = request.GET.get('types')
    keywords = request.GET.get('keywords')
    # 判断有没有搜索
    if types and keywords:
        if types == 'title':
            ob = ob.filter(title__contains=keywords)
    if types == 'price':
            ob = ob.filter(price_gte=int(keywords))
    # 调用 分页
    return limit(request,ob,1,'myadmin/goods/goodslist.html')
    # return render(request,'myadmin/goods.goodslist.html'{'info':ob})

def goodsdel(request):   
# 获取要删除的分类的id    
    cid = request.GET.get('id')    
    # 根据id去查询子分类    
    ob = models.Goods.objects.filter(id = cid)
    for i in ob:
        print(i.status)
    if i.status == 0:
        i = models.Goods.objects.get(id = cid)
        i.status = 1   
        i.save()   
        return JsonResponse({'error': 1, 'msg': '删除成功'})
    else:        
        return JsonResponse({'error': 0, 'msg': '该商品已被删除'})



def goodsedit(request):
    # 接收id
    gid = request.GET.get('id')
    # 查询
    ob = models.Goods.objects.get(id = gid)
    if request.method=='GET':
        cates = models.Cates.objects.extra(select = {'paths':'concat(path,id)'}).order_by('paths')
        return render(request,'myadmin/goods/edit.html',{'info':ob,'cates':cates})
    elif request.method=='POST':
        # 接收用户数据
        data = request.POST.dict()
        # 更新数据
        ob.title = data['title']
        ob.gnum = data['gnum']
        ob.status = data['status']
        ob.info = data['info']
        ob.price = data['price']
        ob.cateid = models.Cates.objects.get(id=data['fname'])
        # 判断有没有上传图片
        myfile = request.FILES.get('pic_url')
        if myfile:
            # 删除
            os.remove(BASE_DIR+ob.pic_url)
            ob.pic_url = upload(myfile)
        ob.save()
        return HttpResponse('<script>alert("修改成功");location.href="'+reverse('myadmin_goods_list')+'"</script>')




def upload(myfile):
    #执行图片的上传
    filename = str(time.time())+"."+myfile.name.split('.').pop()
    destination = open("./static/pics/"+filename,"wb+")
    for chunk in myfile.chunks():      # 分块写入文件  
        destination.write(chunk)  
    destination.close()
    # /static/picsn/图片
    return '/static/pics/'+filename