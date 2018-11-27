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

def orderlist(request):
   # 查询商品
    ob = models.Order.objects.all()
    # 查询
    types = request.GET.get('types')
    keywords = request.GET.get('keywords')
    # 判断有没有搜索
    if types and keywords:
        if types == 'addr':
            ob = ob.filter(addr__contains=keywords)
    if types == 'price':
            ob = ob.filter(price_gte=int(keywords))
    # 调用 分页
    return limit(request,ob,5,'myadmin/order/orderlist.html')


def orderdel(request):   
# 获取要删除的分类的id    
    cid = request.GET.get('id')    
    # 根据id去查询子分类    
    ob = models.Order.objects.filter(id = cid)
    for i in ob:
        print(i.status)
    if i.status == 0:
        i = models.Order.objects.get(id = cid)
        i.status = 1   
        i.save()   
        return JsonResponse({'error': 1, 'msg': '删除成功'})
    else:        
        return JsonResponse({'error': 0, 'msg': '该商品已被删除'})

def orderedit(request):
    oid = request.GET.get('id')
    ob = models.Order.objects.get(id=oid)
    # 判断请求方式 GET通过链接访问都是get方式   a标签 url路由地址栏
    if request.method=='GET':
        # 查询数据
        return render(request,'myadmin/order/edit.html',{'info':ob})
    elif request.method=='POST':
        ob.addr=request.POST.get('addr')
        ob.wl=request.POST.get('wl')
        ob.paytype=request.POST.get('paytype')
        ob.price=request.POST.get('price')
        ob.status=request.POST.get('status')
        ob.save()

        return HttpResponse('<script>alert("修改成功");location.href="'+reverse('myadmin_orderlist')+'"</script> ')