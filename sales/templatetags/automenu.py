from django import template
register = template.Library()



@register.inclusion_tag('automenu.html')
def menulist(request):
    # for now_path in request.session.get('permissions'):
    #     print(now_path,now_path['permissions__url'],request.path)
    #     if request.path ==now_path['permissions__url']:
    #         now_path['class'] ='active'
    #         print('当前用户权限信息',now_path)
    #         return {'menu_dict': request.session.get('menu_dict')}
    print('sssion>>>>>>>>>:',request.session.get('menu_dict'))
    return {'menu_dict': request.session.get('menu_dict')}