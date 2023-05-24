"""体系结构项目 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import account.views
import pages.views

urlpatterns = [
    path('admin/', admin.site.urls, name='account'),
    path('', pages.views.index, name='index'),
    path('login/', account.views.account_login, name='login'),
    path('reg/', account.views.account_reg, name='reg'),
    path('logout/', account.views.account_logout, name='logout'),
    path('manage/', pages.views.manage),
    path('mine/', pages.views.mine),
    path('base/', pages.views.base_info),
    path('base_page/', pages.views.base_page),
    path('addTool/',pages.views.addTool,name='addTool'),
    path('delTool/',pages.views.delTool,name='delTool'),
    path('editTool/',pages.views.editTool,name='editTool'),
    path('borrow_page/',pages.views.borrow_page),
    path('borrowTool/',pages.views.borrow),
]
