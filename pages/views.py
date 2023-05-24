import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import utils.code
from account.models import Employee

# Create your views here.
from pages.models import Tool


@login_required(login_url='login/')
def index(req):
    data = {
        'isLogin': True,
        'username': req.user.username,
        'isAdmin': False
    }
    user = User.objects.filter(username=req.user.username)
    if user:
        user = user.first()
        employee = Employee.objects.get(username_id=user.id)
        if employee:
            if employee.em_classes == 2:
                data.update({'isAdmin': True})
            data.update({'em': utils.code.process(employee)})
    return render(req, 'index.html', data)


@login_required(login_url='login/')
def manage(req):
    res = {"code": 0, "msg": "", "count": 0, "data": []}
    req_username = req.user.username
    id = User.objects.get(username=req_username).id
    em_classes = Employee.objects.get(username_id=id)
    if em_classes.em_classes == 2:
        users = User.objects.all()
        res.update({'count': len(users), 'data': list(users.values())})
        return JsonResponse(res, safe=False)
    else:
        return JsonResponse(res, safe=False)


def mine(req):
    data = {
        'isLogin': True,
        'username': req.user.username,
        'isAdmin': False
    }
    user = User.objects.filter(username=req.user.username)
    if user:
        user = user.first()
        employee = Employee.objects.get(username_id=user.id)
        if employee:
            if employee.em_classes == 2:
                data.update({'isAdmin': True})
            data.update({'em': utils.code.process(employee)})
    return render(req, 'mine.html', data)


@login_required(login_url='login/')
def base_info(req):
    res = {"code": 0, "msg": "", "count": 0, "data": []}
    if isAdmin(req):
        tools = Tool.objects.all()
        res.update({'count': len(tools), 'data': list(tools.values())})
        return JsonResponse(res, safe=False)
    else:
        user_id = User.objects.get(username=req.user.username)
        part_id = Employee.objects.get(username_id=user_id).em_belong
        tools = Tool.objects.filter(tool_part=part_id)
        res.update({'count': len(tools), 'data': list(tools.values())})
        return JsonResponse(res, safe=False)


def base_page(req):
    return render(req, 'repo.html')


def isAdmin(req):
    user = User.objects.filter(username=req.user.username)
    if user:
        user = user.first()
        employee = Employee.objects.get(username_id=user.id)
        if employee:
            if employee.em_classes == 2:
                return True
            else:
                return False
    else:
        return False


@login_required(login_url='login/')
@require_POST
@csrf_exempt
def addTool(req):
    try:
        tool_class = int(req.POST.get('tools-class'))
        tool_price = float(req.POST.get('tool-price'))
        tool_part = int(req.POST.get('tools-part'))
        tool_area = int(req.POST.get('tools-area'))
        tool_borrowed = req.POST.get('tool-borrowed')
        tool_damaged = req.POST.get('tool-damaged')
        tool_name = req.POST.get('tool-name')
        Tool.objects.create(tool_class=tool_class, tool_name=tool_name, tool_area=tool_area, tool_part=tool_part,
                            tool_price=tool_price, tool_damaged=tool_damaged, tool_borrowed=tool_borrowed)
        return JsonResponse("{'msg':'success'}", safe=False)
    except Exception as e:
        print(req.POST)
        return JsonResponse("{'msg':'" + e.__str__() + "'}", safe=False)


@login_required(login_url='login/')
@require_POST
@csrf_exempt
def delTool(req):
    try:
        tool_id = int(req.POST.get('id'))
        tool = Tool.objects.get(id=tool_id)
        tool.delete()
        return JsonResponse("{'msg':'success'}", safe=False)
    except Exception as e:
        return JsonResponse("{'msg':'" + e.__str__() + "'}", safe=False)


@login_required(login_url='login/')
@require_POST
@csrf_exempt
def editTool(req):
    id = int(req.POST.get('id'))
    tool = Tool.objects.get(id=id)
    tool.tool_name = req.POST.get('tool_name')
    tool.save()
    return JsonResponse("{'msg':'success'}", safe=False)


@login_required(login_url='login/')
def borrow_page(req):
    return render(req, 'borrowd.html')


@login_required(login_url='login/')
@require_POST
@csrf_exempt
def borrow(req):
    try:
        print(req.POST)
        id = int(req.POST.get('id'))
        borrowed = int(req.POST.get('borrowed'))
        if isAdmin(req):
            tool = Tool.objects.get(id = id)
            if tool.tool_borrowed == borrowed:
                tool.tool_borrowed = tool.tool_borrowed ^ 1
                tool.save()
                return JsonResponse("{'msg':'success'}", safe=False)
            else:
                return JsonResponse("{'msg':'无法租借或归还'}", safe=False)
        else:
            tool = Tool.objects.get(id=id)
            user = User.objects.get(username=req.user.username)
            emp = Employee.objects.get(username_id=user.id)
            if (tool.tool_part == emp.id and emp.em_classes == 0) or emp.em_classes == 1:
                if tool.tool_borrowed == borrowed:
                    tool.tool_borrowed = tool.tool_borrowed ^ borrowed
                    tool.save()
                    return JsonResponse("{'msg':'success'}", safe=False)
                else:
                    return JsonResponse("{'msg':'无法租借或归还'}", safe=False)
            else:
                return JsonResponse("{'msg':'权限不足'}", safe=False)
    except Exception as e:
        return JsonResponse("{'msg':'" + e.__str__() + "'}", safe=False)