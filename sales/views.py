import re
import random
import os

from sales import models
from django.core.exceptions import ValidationError
from django.shortcuts import (
    render, redirect, HttpResponse,
)
from django.http import JsonResponse
from django import forms
from CRM import settings
from django.forms import ModelForm
from django.forms.models import modelformset_factory
from PIL import Image
from django.urls import reverse
from django.views import View

from utils.hashlib_func import set_md5
from sales.page import MyPagenation


# Create your views here.
class registerForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        min_length=3,
        max_length=32,
        widget=forms.widgets.TextInput(attrs={'class': 'username', 'placeholder': '请输入用户名', 'autocomplete': 'off'}),
        error_messages={
            'required': '用户名不能为空',
            'min_length': '请输入长度3-32位',
            'max_length': '请输入长度3-32位',
        },
    )

    password = forms.CharField(
        label='密码',
        max_length=16,
        min_length=6,
        widget=forms.widgets.PasswordInput(
            attrs={'class': 'password', 'placeholder': "输入密码", 'oncontextmenu': "return false",
                   'onpaste': "return false"}),
        error_messages={
            'required': '密码不能为空',
            'min_length': '请输入长度6-16位',
            'max_length': '请输入长度6-16位',
        },
    )
    r_password = forms.CharField(
        label='确认密码',
        widget=forms.widgets.PasswordInput(
            attrs={'class': 'password', 'placeholder': "确认密码", 'oncontextmenu': "return false",
                   'onpaste': "return false"}),
        error_messages={
            'required': '密码不能为空',
        },
    )
    # 邮箱
    email = forms.EmailField(
        label='请输入邮箱',
        widget=forms.widgets.EmailInput(
            attrs={'class': 'email', 'placeholder': "输入邮箱地址", 'oncontextmenu': "return false",
                   'onpaste': "return false"}),
        error_messages={
            'required': '邮箱不能为空',
            'invalid': '邮箱格式错误',
        },
        # validators=[]
    )

    # 手机号格式校验函数
    def mobiel_validate(self):
        mobile_re = re.compile('^1[0-9]{10}$')
        if not mobile_re:
            raise ValidationError('手机号码格式错误')

    phone_number = forms.CharField(
        label='请输入号码',
        widget=forms.widgets.TextInput(
            attrs={'class': 'phone_number', 'placeholder': "输入手机号", 'oncontextmenu': "return false",
                   'onpaste': "return false"}),
        error_messages={
            'required': '手机号码不能为空',

        },
        validators=[mobiel_validate, ],
    )

    def clean(self):
        pwd = self.cleaned_data.get('password')
        r_pwd = self.cleaned_data.get('r_password')
        if pwd == r_pwd:
            return self.cleaned_data
        else:
            self.add_error('r_password', '两次密码不一致')
            # raise ValidationError('两次密码不一致')


def get_valid_img(request):
    # 生成一个随机的颜色数据
    def get_random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    from PIL import Image, ImageDraw, ImageFont

    # 生成图片对象，颜色标准，大小，颜色
    img_obj = Image.new('RGB', (200, 34), get_random_color())
    # 通过图片对象生成一个画笔对象
    darw_obj = ImageDraw.Draw(img_obj)
    # 设置生成验证码时的字体样式
    font_path = os.path.join(settings.BASE_DIR, 'statics/Notera-Personal-Use-Only/ZCOOL.ttf')
    print(font_path)
    # 创建字体对象,设置字体大小
    font_obj = ImageFont.truetype(font_path, 16)

    # 验证码字符串
    sum_str = ''

    for i in range(6):
        # 从0-9，a-z,A-Z生成一个随机字符
        a = random.choice([str(random.randint(0, 9)), chr(random.randint(97, 122)), chr(random.randint(65, 90))])
        sum_str += a
    print(sum_str)
    # 通过画笔对象添加文字：文字起始位置，文字内容，文字颜色，文字样式
    darw_obj.text((64, 10), sum_str, fill=get_random_color(), font=font_obj)

    # 开辟一块内存空间，将验证码对象保存到该空间中
    from io import BytesIO
    f = BytesIO()
    img_obj.save(f, 'png')
    data = f.getvalue()
    # 将验证码设置到session
    request.session['valid_str'] = sum_str
    return HttpResponse(data)

    # 添加燥线

    # 添加噪点


# 登陆
def login(request):
    response = {'user': None, 'err_msg': ''}
    # login_form =loginForm()
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 从前端页面获取验证码
        validcode = request.POST.get('validcode').upper()
        # 从session表中获取验证码
        r_validcode = request.session.get('valid_str').upper()
        print(username, password, validcode, r_validcode)
        if validcode == r_validcode:
            print('ok')
            # print(username,password)
            user_obj = models.UserInfo.objects.filter(username=username, password=set_md5(password)).first()

            # print(user_obj)
            if user_obj:
                response['user'] = username
                request.session['user_id'] = user_obj.id
                #写入用户权限session
                #TODO
                from utils.session_insert import insert_session
                insert_session(request,user_obj)

                # return HttpResponse('登陆成功')
            else:
                response['err_msg'] = '用户名或者密码错误'
            return JsonResponse(response)
        else:
            response['err_msg'] = '验证码错误'

        return JsonResponse(response)
    # username = request.POST.get('username')
    # password = request.POST.get('password')
    # validcode = request.POST.get('validcode').upper()
    # r_validcode = request.session.get('valid_str').upper()
    # print(validcode)
    # if validcode == r_validcode:
    #     print('ok')
    #     # print(username,password)
    #     user_obj = models.UserInfo.objects.filter(username=username, password=set_md5(password)).first()
    #     # print(user_obj)
    #     if user_obj:
    #         return redirect('customers')
    #         # return HttpResponse('登陆成功')
    #     else:
    #         # login_form = loginForm(request.POST)
    #         return render(request, 'login.html', {'error': '用户名或者密码错误'})


def home(request):
    if request.method == 'GET':
        return render(request, 'templates/saleshtml/home.html')


# 主页
def starter(request):
    print(request)
    if request.method == 'GET':
        return render(request, 'starter.html')


# 注册
def register(request):
    register_form = registerForm()
    if request.method == 'GET':
        return render(request, 'register.html', {'register_form': register_form})

    else:
        register_form = registerForm(request.POST)
        if register_form.is_valid():
            print(register_form.cleaned_data)
            register_form.cleaned_data.pop('r_password')
            # 对密码进行加密
            password = set_md5(register_form.cleaned_data.pop('password'))

            register_form.cleaned_data.update({'password': password})
            models.UserInfo.objects.create(
                **register_form.cleaned_data
            )
            return redirect('login')
        else:
            return render(request, 'register.html', {'register_form': register_form})


# def customers(request):
#     #获取当前登录用户的id
#     id = request.session.get('user_id')
#     current_obj = models.UserInfo.objects.filter(id=id)
#     #通过判断用户点击的页面链接来判断公户和私户
#     current_path = request.path
#     print(current_path,reverse('customers'))
#     if current_path == reverse('customers'):
#         print('走公户')
#         show_obj = models.Custumer.objects.filter(consultant__isnull=True)
#     else:
#         print('私户')
#         show_obj = models.Custumer.objects.filter(consultant=current_obj)
#
#     # print('session',id)
#     name = request.GET.get('name')
#     search_type = request.GET.get('search_type')
#     get_data = request.GET.copy()  # <QueryDict: {'search': ['name__contains'], 'name': ['三国']}>
#     print(request.GET,get_data,name,search_type)
#     # print(name,request.POST)
#     if name:
#         # 获取所有信息个数，得出总页数，a为需要展示的页面总数，b为最后一页信息个数
#
#         obj = show_obj.filter(**{search_type: name})  # obj = models.Custumer.objects.filter(**{search_type: name})
#
#     else:
#         obj = show_obj.all()
#     sum_obj = obj.count()
#     page_num = request.GET.get('page')
#     mypagenation = MyPagenation(sum_obj, page_num, settings.PER_PAGE_NUM, settings.PER_NUM_SHOW)
#     page_html = mypagenation.page_html(get_data)
#
#     customers_obj = obj.order_by('-qq')[
#                     (mypagenation.page_num - 1) * settings.PER_PAGE_NUM:mypagenation.page_num * settings.PER_PAGE_NUM]
#
#     return render(request, 'templates/saleshtml/customers.html',
#                   {'customers_obj': customers_obj, 'page_html': page_html})
#
class CustomerView(View):
    def get(self, request):
        # 获取当前登录用户的id
        id = request.session.get('user_id')
        current_obj = models.UserInfo.objects.filter(id=id)
        # 通过判断用户点击的页面链接来判断公户和私户
        current_path = request.path
        print(current_path, reverse('customers'))
        if current_path == reverse('customers'):
            print('走公户')
            TAG = '1'
            show_obj = models.Custumer.objects.filter(consultant__isnull=True)
        else:
            TAG = '2'
            print('私户')
            show_obj = models.Custumer.objects.filter(consultant=current_obj)
        print('用户为：', show_obj, models.Custumer.objects.filter(consultant_id=4))
        # print('session',id)
        name = request.GET.get('name')
        search_type = request.GET.get('search_type')
        # querydict为不可变数据类型，通过copy方式变成可变数据类型
        get_data = request.GET.copy()  # <QueryDict: {'search': ['name__contains'], 'name': ['三国']}>
        print(request.GET, get_data, name, search_type)
        # print(name,request.POST)
        if name:
            # 获取所有信息个数，得出总页数，a为需要展示的页面总数，b为最后一页信息个数
            obj = show_obj.filter(**{search_type: name})  # obj = models.Custumer.objects.filter(**{search_type: name})
        else:
            obj = show_obj.all()
        sum_obj = obj.count()
        page_num = request.GET.get('page')
        mypagenation = MyPagenation(sum_obj, page_num, settings.PER_PAGE_NUM, settings.PER_NUM_SHOW)
        page_html = mypagenation.page_html(get_data, request.path)
        # 当前页面数据，通过qq倒叙排序
        if obj:
            customers_obj = obj.order_by('-qq')[( mypagenation.page_num - 1) * settings.PER_PAGE_NUM:mypagenation.page_num * settings.PER_PAGE_NUM]
        else:customers_obj = None
        print('full_path:', request.get_full_path())
        return render(request, 'templates/saleshtml/customers.html',
                      {'customers_obj': customers_obj, 'page_html': page_html, 'TAG': TAG})

    def post(self, request):
        print(request.POST)
        action = request.POST.get('action')
        customers_id = request.POST.getlist('cids')
        if hasattr(self, action):
            # customers_obj = models.Custumer.objects.filter(id__in=customers_id)
            res = getattr(self, action)(request, customers_id)
            if res:
                return res
            return redirect(request.path)

    # 公户转私户
    def reverse_g2s(self, request, customers_id):
        customers_obj = models.Custumer.objects.filter(id__in=customers_id, consultant__isnull=True)
        if len(customers_obj) == len(customers_id):
            customers_obj.update(consultant_id=request.session.get('user_id'))
            return
        else:
            return HttpResponse('客户信息不可用，请确认！')

    # 私户转公户
    def reverse_s2g(self, request, customers_id):
        customers_obj = models.Custumer.objects.filter(id__in=customers_id)
        customers_obj.update(consultant=None)


class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Custumer
        fields = '__all__'
        widgets = {
            'birthday': forms.widgets.TextInput(attrs={'type': 'date'})
        }
        error_messages = (
            {
                'qq': {'required': '必填字段'},
                'course': {'required': '必填字段'},
            }
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            from multiselectfield.forms.fields import MultiSelectFormField
            if not isinstance(field, MultiSelectFormField):
                field.widget.attrs.update({"class": "form-control"})


# def add_customer(request):
#     customerform_obj = CustomerForm()
#     if request.method =='GET':
#         return render(request,'templates/saleshtml/add_customer.html',{'customerform_obj':customerform_obj})
#     else:
#         customerform_obj = CustomerForm(request.POST)
#         if customerform_obj.is_valid():
#             customerform_obj.save()
#             return redirect('customers')
#         else:
#             return render(request,'templates/saleshtml/add_customer.html',{'customerform_obj':customerform_obj})

# def edit_customer(request,cid):
#     """
#     编辑客户信息
#     :param request:
#     :param cid: 客户id
#     :return:
#     """
#     customer_obj = models.Custumer.objects.filter(id=cid).first()
#     if request.method =='GET':
#         customerform_obj = CustomerForm(instance=customer_obj)
#         return render(request,'templates/saleshtml/add_customer.html',{'customerform_obj':customerform_obj})
#     else:
#         customerform_obj = CustomerForm(request.POST,instance=customer_obj)
#         if customerform_obj.is_valid():
#             customerform_obj.save()
#             return redirect('customers')
#         else:
#             return render(request, 'templates/saleshtml/add_customer.html', {'customerform_obj': customerform_obj})


def add_edit_customer(request, cid=None):
    """
    编辑/添加客户
    :param self:
    :return:
    """
    print(request.POST)
    if cid:
        label = '编辑客户'
    else:
        label = '添加客户'
    customer_obj = models.Custumer.objects.filter(id=cid).first()
    if request.method == 'GET':
        customerform_obj = CustomerForm(instance=customer_obj)
        return render(request, 'templates/saleshtml/add_customer.html',
                      {'customerform_obj': customerform_obj, 'label': label})
    else:
        customerform_obj = CustomerForm(request.POST, instance=customer_obj)
        if customerform_obj.is_valid():
            customerform_obj.save()
            url = request.GET.get('next')
            print('url>>>>>', url, request.GET)
            # return redirect('customers')
            if url:
                return redirect(url)
            else:
                return redirect('customers')
        else:
            return render(request, 'templates/saleshtml/add_customer.html',
                          {'customerform_obj': customerform_obj, 'label': label})


def search(request):
    pass
    # name = request.GET.get('name')
    # search_type = request.GET.get('search')
    # get_data = request.GET.copy()   #<QueryDict: {'search': ['name__contains'], 'name': ['三国']}>
    # print(get_data)
    # # print(name,request.POST)
    # if name:
    #     # 获取所有信息个数，得出总页数，a为需要展示的页面总数，b为最后一页信息个数
    #     sum_obj = models.Custumer.objects.filter(**{search_type:name}).count()
    #     page_num = request.GET.get('page')
    #     mypagenation = MyPagenation(sum_obj, page_num, settings.PER_PAGE_NUM, settings.PER_NUM_SHOW)
    #     page_html = mypagenation.page_html(get_data)
    #
    #     customers_obj = models.Custumer.objects.filter(**{search_type:name}).order_by('-qq')[( mypagenation.page_num - 1) * settings.PER_PAGE_NUM:mypagenation.page_num * settings.PER_PAGE_NUM]
    #
    #     return render(request, 'templates/saleshtml/customers.html',
    #                   {'customers_obj': customers_obj, 'page_html': page_html})
    # else:return redirect('customers')


class ConsultRecordView(View):

    def get(self, request):

        # 查询所有跟进记录
        pk = request.GET.get('pk')
        print('pk>>>>>>>>>>>>>>>>>>>>>>>>', pk)
        if pk:
            try:
                pk = int(pk)
            except:
                pass
            TAG = '1'
            show_obj = models.ConsultRecord.objects.filter(delete_status=False, consultant=request.obj, customer_id=pk)
            print('xxx用户的跟进信息为：', show_obj, request.obj)
        else:
            if request.path == '/allconsult/':
                TAG = '1'
                show_obj = models.ConsultRecord.objects.filter(delete_status=False)
            # 查询某个销售的跟进记录
            else:
                # print(request.obj.pk,type(request.obj))
                TAG = '2'
                show_obj = models.ConsultRecord.objects.filter(delete_status=False, consultant=request.obj)
        print('跟进记录>>>>>', show_obj)
        # print('session',id)
        name = request.GET.get('name')
        search_type = request.GET.get('search_type')
        # querydict为不可变数据类型，通过copy方式变成可变数据类型
        get_data = request.GET.copy()  # <QueryDict: {'search': ['name__contains'], 'name': ['三国']}>
        print(request.GET, get_data, name, search_type)
        # print(name,request.POST)
        if name:
            # 获取所有信息个数，得出总页数，a为需要展示的页面总数，b为最后一页信息个数
            obj = show_obj.filter(**{search_type: name})  # obj = models.Custumer.objects.filter(**{search_type: name})
            # obj = show_obj.filter(qq__contains=name) --->obj = show_obj.filter(cunsultant__username__contains =name)
        else:
            obj = show_obj.all()
        sum_obj = obj.count()
        page_num = request.GET.get('page')
        mypagenation = MyPagenation(sum_obj, page_num, settings.PER_PAGE_NUM, settings.PER_NUM_SHOW)
        page_html = mypagenation.page_html(get_data, request.path)
        # 当前页面数据，通过qq倒叙排序
        print('最终obj', obj)
        if obj:
            consult_obj = obj[(mypagenation.page_num - 1) * settings.PER_PAGE_NUM:mypagenation.page_num * settings.PER_PAGE_NUM]
        else:consult_obj=None
        print('full_path:', request.get_full_path(), consult_obj)
        return render(request, 'templates/saleshtml/consultrecord.html',
                      {'consult_objs': consult_obj, 'page_html': page_html, 'TAG': TAG})

    def post(self, request):
        action = request.POST.get('action')
        cid_list = request.POST.getlist('cids')
        if hasattr(self, action):
            records = models.ConsultRecord.objects.filter(pk__in=cid_list)
            getattr(self, action)(records)
            return redirect(request.path)

            # 删除记录

    def deleteRecord(self, records):
        records.update(delete_status=True)


class ConsultRecordForm(forms.ModelForm):
    class Meta:
        model = models.ConsultRecord
        fields = '__all__'
        exclude = ('delete_status',)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field, content in self.fields.items():
            from multiselectfield.forms.fields import MultiSelectFormField
            if not isinstance(field, MultiSelectFormField):
                content.widget.attrs.update({"class": "form-control"})
            if field == 'customer':
                content.queryset = models.Custumer.objects.filter(consultant=request.obj)
            elif field == 'consultant':
                content.queryset = models.UserInfo.objects.filter(pk=request.obj.pk)


class AddEditConsultView(View):
    """
    跟进记录添加和编辑
    """

    # 添加纪录
    def get(self, request, cid=None):
        if cid:
            label = '编辑客户'
        else:
            label = '添加客户'
        consult_record_obj = models.ConsultRecord.objects.filter(pk=cid).first()
        if request.method == 'GET':
            # 编辑记录
            recordsForm = ConsultRecordForm(request, instance=consult_record_obj)
            return render(request, 'templates/saleshtml/add_edit_consultrecords.html',
                          {'recordsForm': recordsForm, 'label': label})

    # 编辑记录
    def post(self, request, cid=None):

        consult_record_obj = models.ConsultRecord.objects.filter(pk=cid).first()
        next_url = request.GET.get('next')
        recordsForm = ConsultRecordForm(request, request.POST, instance=consult_record_obj)
        if not next_url:
            return redirect('allconsult')
        if recordsForm.is_valid():
            recordsForm.save()
            return redirect(next_url)


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = models.Enrollment
        fields = '__all__'
        exclude = ('delete_status',)
        # error_messages = (
        #     {
        #         'customer': {'invalid': '此学生已经报名过了'},
        #     }
        # )

    def __init__(self, request, *args, **kwargs):

        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            from multiselectfield.forms.fields import MultiSelectFormField
            from django.forms import BooleanField
            if not isinstance(field, BooleanField):
                field.widget.attrs.update({"class": "form-control"})
            if key == 'customer':
                print(key, field, models.Enrollment.objects.filter(customer__consultant=request.obj))
                field.queryset = models.Custumer.objects.filter(consultant=request.obj)


def Enrollment(request):
    enrollment_obj = models.Enrollment.objects.filter(delete_status=False)
    if request.method == 'GET':
        # print('报名记录>>>>',enrollment)
        name = request.GET.get('name')
        search_type = request.GET.get('search_type')
        # querydict为不可变数据类型，通过copy方式变成可变数据类型
        get_data = request.GET.copy()  # <QueryDict: {'search': ['name__contains'], 'name': ['三国']}>
        print(request.GET, get_data, name, search_type)
        # print(name,request.POST)
        if name:
            # 判断此时状态，如果name不为空则是搜索
            obj = enrollment_obj.filter(
                **{search_type: name})  # obj = models.Custumer.objects.filter(**{search_type: name})
        else:
            obj = enrollment_obj.all()
        sum_obj = obj.count()
        page_num = request.GET.get('page')
        mypagenation = MyPagenation(sum_obj, page_num, settings.PER_PAGE_NUM, settings.PER_NUM_SHOW)
        page_html = mypagenation.page_html(get_data, request.path)
        # 当前页面数据，通过qq倒叙排序
        if obj:
            final_obj = obj[(mypagenation.page_num - 1) * settings.PER_PAGE_NUM:mypagenation.page_num * settings.PER_PAGE_NUM]
        else:final_obj = None
        print('full_path:', request.get_full_path())
        # return render(request, 'templates/saleshtml/customers.html',
        #               {'customers_obj': customers_obj, 'page_html': page_html, 'TAG': TAG})
        return render(request, 'templates/saleshtml/EnrollmentForm.html',
                      {'enrollments': final_obj, 'page_html': page_html})
    else:
        # enrollmentform = EnrollmentForm(instance=enrollment_obj)
        action = request.POST.get('action')
        enrollmentform_pk_list = request.POST.getlist('cids')
        print(enrollmentform_pk_list, action)
        del_obj = models.Enrollment.objects.filter(id__in=enrollmentform_pk_list)
        del_obj.update(delete_status=True)
        return redirect('Enrollment')


def add_edit_enrollment(request, cid=None):
    enrollment_obj = models.Enrollment.objects.filter(pk=cid).first()
    enrollmentform = EnrollmentForm(request, instance=enrollment_obj)

    if cid:
        label = '添加记录'
    else:
        label = '编辑记录'
    if request.method == 'GET':

        return render(request, 'templates/saleshtml/add_edit_enrollment.html',
                      {'enrollmentform': enrollmentform, 'label': label})

    else:
        enrollmentform = EnrollmentForm(request, request.POST, instance=enrollment_obj)
        if enrollmentform.is_valid():
            enrollmentform.save()
            next_url = request.GET.get('next')
            print('next_url>>>>>>>>>>>>', next_url)
            if next_url:
                return redirect(next_url)
            else:
                return redirect('Enrollment')
        else:
            print(enrollmentform.errors)
            Validationerror = '该学生已经报名!!!'
            return render(request, 'templates/saleshtml/add_edit_enrollment.html',
                          {'enrollmentform': enrollmentform, 'label': label, 'Validationerror': Validationerror})


class CourseRecord(forms.ModelForm):
    class Meta:
        model = models.CourseRecord
        fields = '__all__'

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('self.fields>>>>>>>>>>>>', self.fields)
        from django.forms import BooleanField

        for key, field in self.fields.items():
            if not isinstance(field, BooleanField):
                field.widget.attrs.update({'class': 'form-control'})


class courseRecord(View):

    def get(self, request):
        # courseRecord =  models.CourseRecord.objects.all()
        # print('courseRecord>>>>>>>',courseRecord)
        search_type = request.GET.get('search_type')
        name = request.GET.get('name')
        get_data = request.GET.copy()
        print('get_data:', get_data, 'search_type', search_type, 'name:', name)
        if name:
            courseRecord = models.CourseRecord.objects.filter(**{search_type: name})
        else:
            courseRecord = models.CourseRecord.objects.all()
        sum_obj = courseRecord.count()
        page_num = request.GET.get('page')
        # 得到页面对象
        page_obj = MyPagenation(sum_obj, page_num, settings.PER_PAGE_NUM, settings.PER_NUM_SHOW)
        # 生成页脚数据
        page_html = page_obj.page_html(get_data, request.path)
        # 往页面上渲染数据
        courseRecord = courseRecord.order_by('-date')[
                       (page_obj.page_num - 1) * settings.PER_PAGE_NUM:page_obj.page_num * settings.PER_PAGE_NUM]

        return render(request, 'templates/saleshtml/courserecord.html',
                      {'page_html': page_html, 'courseRecords': courseRecord})

    # def post(self,request):
    #     cid_list = request.POST.getlist('cids')
    #     del_obj = models.CourseRecord.objects.filter(id__in=cid_list)
    #     del_obj.delete()
    #     return redirect('courseRecord')

    # 查看学习记录
    def post(self, request):
        cid_list = request.POST.getlist('cids')
        action = request.POST.get('action')
        if hasattr(self, action):
            res = getattr(self, action)(request, cid_list)
            return res

    # 批量生成学习记录
    def bulk_create_record(self, request, cid_list):
        for cid in cid_list:
            courserecord_obj = models.CourseRecord.objects.filter(pk=cid).first()
            student_obj = courserecord_obj.re_class.custumer_set.filter(status='studying')
            print('student_obj>>>', len(student_obj))
            obj_list = []
            for student in student_obj:
                # models.StudyRecord.objects.create(
                #
                #     course_record_id = cid,
                #     student = student_obj,
                # )
                obj = models.StudyRecord(
                    course_record_id=cid,
                    student=student,
                )
                obj_list.append(obj)
            models.StudyRecord.objects.bulk_create(obj_list)
        return redirect(request.path)

def add_edit_courserecord(request, cid=None):
    page_obj = models.CourseRecord.objects.filter(pk=cid).first()
    CourseRecordForm = CourseRecord(request, instance=page_obj)
    if cid:
        label = '编辑记录'
    else:
        label = '添加纪录'
    if request.method == 'GET':
        return render(request, 'templates/saleshtml/add_edit_courserecord.html',
                      {'CourseRecordForm': CourseRecordForm, 'label': label})
    else:
        CourseRecordForm = CourseRecord(request, request.POST, instance=page_obj)
        if CourseRecordForm.is_valid():
            CourseRecordForm.save()
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect('courseRecord')
        else:
            Validationerror = '该课程已经存在!!!'
            return render(request, 'templates/saleshtml/add_edit_courserecord.html',
                          {'CourseRecordForm': CourseRecordForm, 'label': label, 'Validationerror': Validationerror})


class StudyRecordForm(forms.ModelForm):
    class Meta:
        model = models.StudyRecord
        fields ='__all__'


class StudyRecord(View):


    def get(self,request,course_record_id):
        formset = modelformset_factory(model=models.StudyRecord, form=StudyRecordForm)
        study_records = models.StudyRecord.objects.filter(course_record_id=course_record_id)
        formset = formset(queryset=study_records)
        print(course_record_id)
        return render(request,'templates/saleshtml/studyrecord.html',{'formsets':formset})
    def post(self, request,course_record_id):
        formset = modelformset_factory(model=models.StudyRecord, form=StudyRecordForm,extra=0)
        # print('*args',*args)
        form_cls = formset(request.POST)
        if form_cls.is_valid():
            form_cls.save()
            print('------------提交数据成功----------')
            return redirect(request.path)
        else:
            print('------------提交数据失败----------',formset.errors)
            return render(request, 'templates/saleshtml/studyrecord.html', {'formsets': form_cls})
