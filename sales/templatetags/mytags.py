from django import template
from django.urls import reverse


register = template.Library()


@register.simple_tag
def resole_url(request,url,pk):
    """

    :param request: request参数
    :param url: 编辑页面的别名
    :param pk: 需要编辑的参数的主键
    :return:
    """
    #原本编辑界面路径：/edit_customer/238/    ----->/customers/?page=4
    #希望get得到的路径：/customers/?search_type=qq__contains&name=12&page=2
    #将样式修改成，后台通过get方法获取next中的参数/edit_customer/238/?next=/customers/?search_type=qq__contains&name=12&page=2
    #实际上，后台get方法返回值为：/customers/?search_type=qq__contains 无法获取到&之后的内容
    next_url = request.get_full_path()  #redirect需要通过next参数得到的路径

    #解码后的编辑路径 /edit_customer/
    rev_url = reverse(url,args=(pk,))

    from django.http import QueryDict
    Q = QueryDict(mutable=True)  #将q定义成querydict对象
    Q['next'] = next_url #将next_url 赋值给 Q['next']属性
    next_url = Q.urlencode()  #将编码后的之再次复制给next_url

    res_url = rev_url+'?'+next_url
    print('res_url>>>>>>>>>>>',res_url)
    return res_url