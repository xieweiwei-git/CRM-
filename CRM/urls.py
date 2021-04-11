"""CRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from sales import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    #获取图片验证码
    url(r'^get_valid_img/', views.get_valid_img, name='get_valid_img'),

    url(r'^starter/', views.starter, name='starter'),
    url(r'^home/', views.home, name='home'),
    # 显示客户
    url(r'^customers/', views.CustomerView.as_view(), name='customers'),
    # url(r'^customers/',views.customers,name='customers'),
    # 查看我的客户
    url(r'my_customer/', views.CustomerView.as_view(), name='my_customer'),
    # 添加客户
    url(r'^add_customer/', views.add_edit_customer, name='add_customer'),
    url(r'^edit_customer/(\d+)/', views.add_edit_customer, name='edit_customer'),

    # url(r'^edit_customer/(\d+)/',views.edit_customer,name='edit_customer'),
    url(r'^search/', views.search, name='search'),

    # 跟进记录
    url(r'^myconsult/', views.ConsultRecordView.as_view(), name='myconsult'),
    url(r'^allconsult/', views.ConsultRecordView.as_view(), name='allconsult'),

    # 添加/编辑跟进记录
    url(r'^add_consult/', views.AddEditConsultView.as_view(), name='add_consult'),
    url(r'^edit_consult/(\d+)/', views.AddEditConsultView.as_view(), name='edit_consult'),

    # 报名记录
    url(r'^Enrollment/', views.Enrollment, name='Enrollment'),
    # 添加/修改报名记录
    url(r'^add_enrollment/', views.add_edit_enrollment, name='add_enrollment'),
    url(r'^edit_enrollment/(\d+)/', views.add_edit_enrollment, name='edit_enrollment'),

    # 课程记录
    url(r'^courseRecord/', views.courseRecord.as_view(), name='courseRecord'),
    # 添加/编辑课程记录页面
    url(r'^add_courserecord/', views.add_edit_courserecord, name='add_courserecord'),
    url(r'^add_edit_courserecord/(\d+)/', views.add_edit_courserecord, name='add_edit_courserecord'),

    #显示学习记录
    url(r'^studyrecord/(\d+)/',views.StudyRecord.as_view(),name='studyrecord'),
    #查看课程学习记录
    url(r'^showstudyrecord/',views.StudyRecord.as_view(),name='showstudyrecord')
]
