from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
from .. import models
from django.core.urlresolvers import reverse
import time,os
from web.settings import BASE_DIR
from django.core.paginator import Paginator
from django.db.models import Q



def catesadd(request):
    if request.method=='GET':
        # cates = models.Cates.objects.all()
        cates = models.Cates.objects.extra(select = {'paths':'concat(path,id)'}).order_by('paths')
        # 查询所有分类 分配数据
        return render(request,'myadmin/cates/add.html',{'info':cates})
    elif request.method=='POST':
        data = request.POST.dict()  # fname=0 name=手机
        # 添加
        ob = models.Cates()
        ob.name = data['name']
        ob .pid = int(data['fname'])
        # 判断是否是顶级分类
        if ob.pid != 0:
            f = models.Cates.objects.get(id=data['fname']) # id=0 [{object:object}] <query:[{},{}]>
            ob.path = f.path+str(ob.pid)+','
        else:
            ob.path=data['fname']+','
            # ob.path='0,'
        ob.save()
        return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_cates_list')+'"</script>')



def cateslist(request):
    # cates = models.Cates.objects.all()
    # 模型提供 extra
    ob = models.Cates.objects.extra(select = {'paths':'concat(path,id)'}).order_by('paths')
    for x in ob:
        print(x.path.count(',')-1)
    # 顶级分类
        # 服装
            # 男装
                # 西装
            # 女装
        # 数码
            # 手机
    # return render(request,'myadmin/cates/userlist.html',{'info':ob})
    keywords = request.GET.get('keywords','')
    types = request.GET.get('types','')
    search = {'keywords':keywords,'types':types}
    # 判断有没有条件查询
    if types:
        # 判断有没有搜索类型
        if types == 'all':
            ob = ob.filter(Q(name__contains=keywords)|Q(pid__contains=keywords))
            return fpage(request,ob,search)
        else:
            t = {types+'__contains':keywords}
            ob = ob.filter(**t)
            return fpage(request,ob,search)
    else:
        return fpage(request,ob,search)



def catesdel(request):    
# 获取要删除的分类的id    
    cid = request.GET.get('id')    
    # 根据id去查询子分类    
    ob = models.Cates.objects.filter(pid = cid)    
    a = 0    
    for i in ob:        
        print(i.isDelete)        
        if i.isDelete == 1:            
            a += 1    
    if a == 0:        
        z = models.Cates.objects.get(id=cid)        
        z.isDelete=0        
        z.save()        
        return JsonResponse({'error': 1, 'msg': '删除成功'})    
    else:        
        return JsonResponse({'error': 0, 'msg': '有子分类不能删除'})




# 修改
def catesedit(request):
    # 接收数据
    data = request.GET.dict()
    print(data)
    try:
        # 更新数据
        ob = models.Cates.objects.get(id=int(data['id']))
        ob.name=data['name']
        
    except:

        return JsonResponse({'error':0,'msg':'修改失败'})
    else:
        ob.save()
        return JsonResponse({'error':1,'msg':'修改成功'})

def fpage(request,ob,search):
    # 数据分页
    # 实例化分页类 第一个参数所有的数据集合 每页要显示的条数
    p = Paginator(ob,5)
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


    return render(request,'myadmin/cates/userlist.html',{"info":pagedata,'pagenums':pag_list,'pg':pg,'search':search})