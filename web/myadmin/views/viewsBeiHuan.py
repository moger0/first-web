from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from django.core.urlresolvers import reverse
import time,os
from .. import models
from web.settings import BASE_DIR
from django.core.paginator import Paginator
from django.db.models import Q
import pymysql

# Create your views here.
def sqlbeifen(request):
    # db = pymysql.connect("localhost","root","123456","web")
    # db.close()
    try:
        dumpcmd = "mysqldump -uroot -p123456 web > ../../db_web.sql"
        print(dumpcmd)
        os.system(dumpcmd)
        # return HttpResponse('ok')
        return HttpResponse('<script>alert("备份成功");history.back(-1);</script>')
    except:
        return HttpResponse('<script>alert("备份失败");history.back(-1);</script>')

def sqlhuanyuan(request):
    try:
        dumpcmd = "mysql -uroot -p123456 web < ../../db_web.sql"
        print(dumpcmd)
        os.system(dumpcmd)
        # return HttpResponse('ok')
        return HttpResponse('<script>alert("还原成功");history.back(-1);</script>')
    except:
        return HttpResponse('<script>alert("还原失败");history.back(-1);</script>')
