import re
import random
import os

from sales import models
from django.core.exceptions import ValidationError
from django.shortcuts import (
render,redirect,HttpResponse,
)
from django.http import JsonResponse
from django import forms
from CRM import settings
from django.forms import ModelForm
from PIL import Image


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
        widget=forms.widgets.PasswordInput(attrs={'class': 'password', 'placeholder': "输入密码", 'oncontextmenu': "return false", 'onpaste': "return false"}),
        error_messages={
            'required':'密码不能为空',
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
    #邮箱
    email = forms.EmailField(
        label='请输入邮箱',
        widget=forms.widgets.EmailInput(attrs={'class': 'email', 'placeholder': "输入邮箱地址", 'oncontextmenu': "return false", 'onpaste': "return false"}),
        error_messages={
            'required':'邮箱不能为空',
            'invalid':'邮箱格式错误',
                       },
        # validators=[]
    )


    #手机号格式校验函数
    def mobiel_validate(self):
        mobile_re = re.compile('^1[0-9]{10}$')
        if not mobile_re:
            raise ValidationError('手机号码格式错误')

    phone_number =forms.CharField(
        label='请输入号码',
        widget=forms.widgets.TextInput(attrs={'class':'phone_number', 'placeholder': "输入手机号", 'oncontextmenu': "return false", 'onpaste': "return false"}),
        error_messages={
            'required':'手机号码不能为空',

        },
        validators=[mobiel_validate,],
    )


    def clean(self):
        pwd = self.cleaned_data.get('password')
        r_pwd = self.cleaned_data.get('r_password')
        if pwd == r_pwd:
            return self.cleaned_data
        else:
            self.add_error('r_password','两次密码不一致')
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

    #开辟一块内存空间，将验证码对象保存到该空间中
    from io import BytesIO
    f = BytesIO()
    img_obj.save(f, 'png')
    data = f.getvalue()
    #将验证码设置到session
    request.session['valid_str'] = sum_str
    return HttpResponse(data)

    # 添加燥线

    # 添加噪点


#登陆
def login(request):
    response = {'user':None,'err_msg':''}
    # login_form =loginForm()
    if request.method=='GET':
        return render(request,'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        #从前端页面获取验证码
        validcode = request.POST.get('validcode').upper()
        #从session表中获取验证码
        r_validcode = request.session.get('valid_str').upper()
        print(username,password,validcode,r_validcode)
        if validcode ==r_validcode:
            print('ok')
            # print(username,password)
            user_obj = models.UserInfo.objects.filter(username=username,password=set_md5(password)).first()
            # print(user_obj)
            if user_obj:
                response['user'] = username
                request.session['user_id'] = user_obj.id
                print('当前用户id：',user_obj.id)
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
    if request.method =='GET':
        return render(request, 'templates/saleshtml/home.html')

#主页
def starter(request):
    print(request)
    if request.method == 'GET':
        return render(request,'starter.html')


#注册
def register(request):
    register_form = registerForm()
    if request.method == 'GET':
        return render(request, 'register.html', {'register_form': register_form})

    else:
        register_form = registerForm(request.POST)
        if register_form.is_valid():
            print(register_form.cleaned_data)
            register_form.cleaned_data.pop('r_password')
            #对密码进行加密
            password = set_md5(register_form.cleaned_data.pop('password'))

            register_form.cleaned_data.update({'password':password})
            models.UserInfo.objects.create(
                **register_form.cleaned_data
            )
            return redirect('login')
        else:return render(request, 'register.html', {'register_form': register_form})

def customers(request):
    #获取当前登录用户的id
    id = request.session.get('user_id')
    #通过判断用户点击的页面链接来判断公户和私户
    path = request.path
    print(path)

    # print('session',id)
    name = request.GET.get('name')
    search_type = request.GET.get('search_type')
    get_data = request.GET.copy()  # <QueryDict: {'search': ['name__contains'], 'name': ['三国']}>
    print(request.GET,get_data,name,search_type)
    # print(name,request.POST)
    if name:
        # 获取所有信息个数，得出总页数，a为需要展示的页面总数，b为最后一页信息个数
        obj = models.Custumer.objects.filter(**{search_type: name})

    else:
        obj = models.Custumer.objects.all()
    sum_obj = obj.count()
    page_num = request.GET.get('page')
    mypagenation = MyPagenation(sum_obj, page_num, settings.PER_PAGE_NUM, settings.PER_NUM_SHOW)
    page_html = mypagenation.page_html(get_data)

    customers_obj = obj.order_by('-qq')[
                    (mypagenation.page_num - 1) * settings.PER_PAGE_NUM:mypagenation.page_num * settings.PER_PAGE_NUM]

    return render(request, 'templates/saleshtml/customers.html',
                  {'customers_obj': customers_obj, 'page_html': page_html})
    # # 获取所有信息个数，得出总页数，a为需要展示的页面总数，b为最后一页信息个数
    # sum_obj = models.Custumer.objects.all().count()
    # page_num = request.GET.get('page')
    # mypagenation = MyPagenation(sum_obj,page_num,settings.PER_PAGE_NUM,settings.PER_NUM_SHOW)
    # page_html = mypagenation.page_html()
    # # a, b = divmod(sum_obj, per_page_num)
    # # # 首先获取page的值
    # # try:
    # #     page_num = int(request.GET.get('page'))
    # # except:
    # #     page_num = 1
    # # if per_page_num:
    # #     a += 1
    # # print(a, b)
    # # # 判断输入是否合法
    # # if page_num <= 0:
    # #     page_num = 1
    # # elif page_num > a:
    # #     page_num = a
    # # # 设置显示页数
    # # first_page = page_num - page_num_show // 2
    # # last_page = page_num + page_num_show // 2
    # # print(first_page, last_page)
    # # if first_page <= 0:
    # #     first_page = 1
    # #     last_page = page_num_show
    # # elif last_page >= a:
    # #     last_page = a
    # #     first_page = a - page_num_show+1
    # # page_html = ''
    # # #向上翻页
    # # if page_num <=1:
    # #     pre_page = f'<li class="disabled"><a href="#" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'
    # # else:
    # #     pre_page = f'<li><a href="/customers/?page={page_num-1}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'
    # # page_html += pre_page
    # # #循环生成页面
    # # for i in range(first_page,last_page+1):
    # #     if i == page_num:
    # #         page_html += f'<li class="active"><a href="/customers/?page={i}">{i}</a></li>'
    # #     else:page_html += f'<li><a href="/customers/?page={i}">{i}</a></li>'
    # #
    # # #向下翻页
    # # if page_num>=a:
    # #     next_page = '<li class="disabled"><a href="#" aria-label="Next"><span aria-hidden="true" >&raquo;</span></a></li>'
    # # else:
    # #     next_page = f'<li><a href="/customers/?page={page_num+1}" aria-label="Next"><span aria-hidden="true" >&raquo;</span></a></li>'
    # # page_html+=next_page
    #
    # customers_obj = models.Custumer.objects.all().order_by('-qq')[(mypagenation.page_num - 1) * settings.PER_PAGE_NUM:mypagenation.page_num * settings.PER_PAGE_NUM]
    # # return render(request, 'templates/saleshtml/customers.html',
    # #               {'customers_obj': customers_obj, 'customers_count': range(first_page, last_page + 1)})
    # return render(request,'templates/saleshtml/customers.html',{'customers_obj': customers_obj,'page_html':page_html})

class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Custumer
        fields ='__all__'
        widgets = {
            'birthday':forms.widgets.TextInput(attrs={'type':'date'})
        }
        error_messages=(
            {
                'qq':{'required':'必填字段'},
                'course':{'required':'必填字段'},
            }
        )
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            from multiselectfield.forms.fields import MultiSelectFormField
            if not isinstance(field,MultiSelectFormField):
                field.widget.attrs.update({"class":"form-control"})

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


def add_edit_customer(request,cid=None):
    """
    编辑/添加客户
    :param self:
    :return:
    """
    print(request.POST)
    if cid :label='编辑客户'
    else:label='添加客户'
    customer_obj = models.Custumer.objects.filter(id=cid).first()
    if request.method=='GET':
        customerform_obj = CustomerForm(instance=customer_obj)
        return render(request, 'templates/saleshtml/add_customer.html', {'customerform_obj': customerform_obj,'label':label})
    else:
        customerform_obj = CustomerForm(request.POST, instance=customer_obj)
        if customerform_obj.is_valid():
            customerform_obj.save()
            return redirect('customers')
        else:
            return render(request, 'templates/saleshtml/add_customer.html', {'customerform_obj': customerform_obj,'label':label})

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