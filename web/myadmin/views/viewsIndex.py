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

