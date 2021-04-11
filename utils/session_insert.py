

def insert_session(request,user_obj):
    # permission = models.Permission.objects.filter(role__userinfo=user_obj).distinct()
    # permission1 = user_obj.roles.first().permissions.distinct()
    permissions = user_obj.roles.values('permissions__url', 'permissions__title', 'permissions__is_menu').distinct()
    permission_list = list(user_obj.roles.values('permissions__url', 'permissions__title','permissions__menus__id', 'permissions__menus__title').distinct())
    # print(permission_list)

    #格式化写入的内容
    menu_dict = {}
    for perrmission_dict in permission_list:
        if perrmission_dict['permissions__menus__id']:
            if perrmission_dict['permissions__menus__id'] in menu_dict.keys():
                # print(dict[perrmission_dict['permissions__menus__id']]['children'],)
                menu_dict[perrmission_dict['permissions__menus__id']]['children'].append(
                    {'permissions__url': perrmission_dict.get('permissions__url'),
                     'permissions__title': perrmission_dict.get('permissions__title')}
                )
            else:
                menu_dict[perrmission_dict['permissions__menus__id']] = {
                    'permissions__menus__title': perrmission_dict['permissions__menus__title'],
                    'children': [{'permissions__url': perrmission_dict.get('permissions__url'),
                                  'permissions__title': perrmission_dict.get('permissions__title')}]
                }

    request.session['menu_dict'] = menu_dict

    # 写入当前权限
    request.session['permissions'] = list(permissions)

    print('当前用户id：', user_obj.id)


permission_list = [{
	'permissions__url': '/customers/',
	'permissions__title': '显示客户',
	'permissions__menus__id': 1,
	'permissions__menus__title': '客户管理'
}, {
	'permissions__url': '/my_customer/',
	'permissions__title': '查看我的客户',
	'permissions__menus__id': 1,
	'permissions__menus__title': '客户管理'
}, {
	'permissions__url': '/myconsult/',
	'permissions__title': '我的跟进记录',
	'permissions__menus__id': 2,
	'permissions__menus__title': '记录查询'
}, {
	'permissions__url': '/allconsult/',
	'permissions__title': '所有跟进记录',
	'permissions__menus__id': 2,
	'permissions__menus__title': '记录查询'
}, {
	'permissions__url': '/Enrollment/',
	'permissions__title': '报名记录',
	'permissions__menus__id': 2,
	'permissions__menus__title': '记录查询'
}, {
	'permissions__url': '/courseRecord/',
	'permissions__title': '课程记录',
	'permissions__menus__id': 2,
	'permissions__menus__title': '记录查询'
}, {
	'permissions__url': '/login/',
	'permissions__title': '登陆',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/register/',
	'permissions__title': '注册',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/starter/',
	'permissions__title': '主页',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/add_customer/',
	'permissions__title': '添加客户',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/edit_customer/(\\d+)/',
	'permissions__title': '编辑客户',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/get_valid_img/',
	'permissions__title': '图片验证码',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/search/',
	'permissions__title': '搜索',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/add_consult/',
	'permissions__title': '添加跟进记录',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/dit_consult/(\\d+)/',
	'permissions__title': '修改跟进记录',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/add_enrollment/',
	'permissions__title': '添加报名记录',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/edit_enrollment/(\\d+)/',
	'permissions__title': '编辑报名记录',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/add_courserecord/',
	'permissions__title': '添加课程记录',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/add_edit_courserecord/(\\d+)/',
	'permissions__title': '编辑课程记录',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/studyrecord/(\\d+)/',
	'permissions__title': '显示学习记录',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/showstudyrecord/',
	'permissions__title': '查看课程记录',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}]
"""
# 目标样式：{
    1 : {
        'permissions__menus__title': '客户管理',
        children:[
        {'permissions__url': '/customers/'},
	    {'permissions__title': '显示客户'},
    ]
  }

"""

menu_dict = {}
for perrmission_dict in permission_list:
    if perrmission_dict['permissions__menus__id']:
        if perrmission_dict['permissions__menus__id'] in menu_dict.keys():
            # print(dict[perrmission_dict['permissions__menus__id']]['children'],)
            menu_dict[perrmission_dict['permissions__menus__id']]['children'].append(
                {'permissions__url': perrmission_dict.get('permissions__url'),
                 'permissions__title': perrmission_dict.get('permissions__title')}
            )
        else:
            menu_dict[perrmission_dict['permissions__menus__id']] = {
                'permissions__menus__title': perrmission_dict['permissions__menus__title'],
                'children': [{'permissions__url': perrmission_dict.get('permissions__url'),
                              'permissions__title': perrmission_dict.get('permissions__title')}]
            }
# print(menu_dict)
"""
data = < QuerySet[{
	'permissions__url': '/customers/',
	'permissions__title': '显示客户',
	'permissions__menus__id': 1,
	'permissions__menus__title': '客户管理'
}, {
	'permissions__url': '/my_customer/',
	'permissions__title': '查看我的客户',
	'permissions__menus__id': 1,
	'permissions__menus__title': '客户管理'
}, {
	'permissions__url': '/myconsult/',
	'permissions__title': '我的跟进记录',
	'permissions__menus__id': 2,
	'permissions__menus__title': '记录查询'
}, {
	'permissions__url': '/allconsult/',
	'permissions__title': '所有跟进记录',
	'permissions__menus__id': 2,
	'permissions__menus__title': '记录查询'
}, {
	'permissions__url': '/Enrollment/',
	'permissions__title': '报名记录',
	'permissions__menus__id': 2,
	'permissions__menus__title': '记录查询'
}, {
	'permissions__url': '/courseRecord/',
	'permissions__title': '课程记录',
	'permissions__menus__id': 2,
	'permissions__menus__title': '记录查询'
}, {
	'permissions__url': '/login/',
	'permissions__title': '登陆',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/register/',
	'permissions__title': '注册',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/starter/',
	'permissions__title': '主页',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/add_customer/',
	'permissions__title': '添加客户',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/edit_customer/(\\d+)/',
	'permissions__title': '编辑客户',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/get_valid_img/',
	'permissions__title': '图片验证码',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/search/',
	'permissions__title': '搜索',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/add_consult/',
	'permissions__title': '添加跟进记录',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/dit_consult/(\\d+)/',
	'permissions__title': '修改跟进记录',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/add_enrollment/',
	'permissions__title': '添加报名记录',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/edit_enrollment/(\\d+)/',
	'permissions__title': '编辑报名记录',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/add_courserecord/',
	'permissions__title': '添加课程记录',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/add_edit_courserecord/(\\d+)/',
	'permissions__title': '编辑课程记录',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}, {
	'permissions__url': '/studyrecord/(\\d+)/',
	'permissions__title': '显示学习记录',
	'permissions__menus__id': 0,
	'permissions__menus__title': None
}] >
"""