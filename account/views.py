from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import *

from account.models import Employee


# Create your views here.
def account_login(req):
    data = {
        "isLogin": False
    }
    if req.method == 'GET':
        return render(req, 'account_login.html')
    else:
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(req, user=user)
            data.update({"isLogin": True, 'code': 200})
            return HttpResponseRedirect('/')
        else:
            data.update({"isLogin": False, 'code': 400})
            return render(req, 'account_login.html', data)


def account_reg(req):
    data = {
        "isLogin": False
    }
    if req.method == 'GET':
        return render(req, 'account_reg.html', data)
    else:
        username = req.POST.get('username')
        password = req.POST.get('password')
        email = req.POST.get('email')
        user = User.objects.filter(username=username)
        if not user:
            User.objects.create_user(username=username, password=password, email=email)
            user = User.objects.get(username=username)
            Employee.objects.create(username_id=user.id, em_belong=-1, em_classes=-1)
            login(req, user=user)
            return HttpResponseRedirect('/')
        else:
            data.update({"isLogin": False, 'code': 400})
            return render(req, 'account_login.html', data)


@login_required(login_url='login')
def account_logout(req):
    logout(req)
    return HttpResponseRedirect('/')
