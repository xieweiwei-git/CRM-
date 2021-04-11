from django.db import models
from multiselectfield import MultiSelectField
from django.utils.safestring import mark_safe

# Create your models here.


course_choices = (('LinuxL', 'Linux中高级'),
                  ('PythonFullStack', 'Python全栈开发'),)

class_type_choices = (('fulltime', '脱产班'),
                      ('online', '网络班'),
                      ('weekend', '周末班'),)

source_type = (('qq', 'qq群'),
               ('referral', '内部转介绍'),
               ('website', '官方网站'),
               ('baidu_ads', '百度推广'),
               ('office_direct', '直接上门'),
               ('WoM', '口碑'),
               ('public_class', '公开课'),
               ('website_luffy', '路飞官网'),
               ('others', '其他'),)

enroll_status_choices = (('signed', '已报名'),
                         ('unregistered', '未报名'),
                         ('studying', '学习中'),
                         ('paid_in_full', '学费已经交齐'),)


seek_status_choices = (('A', '近期无报名计划'), ('B', '一个月内报名'), ('C', '2周内报名'), ('D', '1周内报名'),
                       ('E', '订金'), ('F', '到班'), ('G', '全款'), ('H', '无效'))

pay_type_choices = (('deposit', '订金/报名费'),
                    ('tuition', '学费'),
                    ('transfer', '转班'),
                    ('dropout', '退学'),
                    ('refund', '退款'),)

addtendance_choices = (
    ('checked', '已签到'),
    ('vacate', '请假'),
    ('late', '迟到'),
    ('absence', '缺勤'),
    ('leave_early', '早退'),
)

score_choices = (
    (100, 'A+'),
    (90, 'A'),
    (85, 'B+'),
    (80, 'B'),
    (70, 'B-'),
    (60, 'C+'),
    (50, 'C'),
    (40, 'C-'),
    (0, 'D'),
    (-1, 'N/A'),
    (-100, 'COPY'),
    (-1000, 'FAIL')
)


class UserInfo(models.Model):
    """
    用户表：销售/讲师/班主任
    """

    username = models.CharField(max_length=16)
    password = models.CharField(max_length=32)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    roles = models.ManyToManyField(to='Role')

    def __str__(self):
        return self.username


class Custumer(models.Model):
    """
    客户表
    """
    # help_text参数基本上都是供 admin里面的应用设置的
    qq = models.CharField(verbose_name='QQ', max_length=64, unique=True, help_text='QQ号必须唯一')

    # blank=True控制的是required：False，null控制的是数据库字段允许为空
    qq_name = models.CharField('QQ昵称', max_length=64, blank=True, null=True)
    # 允许空，因为有的人不愿意给真是姓名
    # null
    # 是针对数据库而言，如果
    # null = True, 表示数据库的该字段可以为空，即在Null字段显示为YES
    #
    # blank
    # 是针对表单的，如果
    # blank = True，表示你的表单填写该字段的时候可以不填，但是对数据库来说，没有任何影响
    name = models.CharField('姓名', max_length=32, help_text='学员报名后可改为真实姓名')
    sex_type = (('male', '男'), ('female', '女'))  # 保存的是male和female
    sex = models.CharField('性别', choices=sex_type, max_length=16, default='male', blank=True, null=True)
    birthday = models.DateField('出生日期', default=None, help_text='格式：yyyy-mm-dd', blank=True, null=True)
    # phone = models.BigIntegerField('手机号码',blank=True,null=True)
    phone = models.CharField('手机号码', blank=True, null=True, max_length=13)  # 改成字符串方便搜索
    source = models.CharField('客户来源', max_length=64, choices=source_type, default='qq')

    introduce_from = models.ForeignKey('self', verbose_name='转介绍自学员', blank=True, null=True, on_delete=models.CASCADE)
    # self指的是自己这个表,自己是自己表的子关联字段
    # '''
    # id name introduce_from
    # 1   dz     None
    # 2   xf      1
    # 3   sd      1
    # '''
    course = MultiSelectField('资讯课程',
                              choices=course_choices)  # 多选，会存成一个列表的形式，通过modelform调用的时候，会成为一个多选框,如果不想用多选可以用charfield

    class_type = models.CharField('班级类型', max_length=64, choices=class_type_choices, default='fulltime')
    customer_note = models.TextField('客户备注', blank=True, null=True)
    status = models.CharField('状态', choices=enroll_status_choices, max_length=64, default='unregistered',
                              help_text='客户此时的注册状态')
    date = models.DateTimeField('咨询日期', auto_now_add=True)  # 没啥屌用的字段，销售说记录客户注册时的时间，周年时发song祝福
    last_consult_date = models.DateField('最后跟进时间', auto_now_add=True)
    # 考核销售的绩效，记录最后跟进时间，如果时间长未跟进影响绩效
    next_date = models.DateField('预计再次跟进时间', blank=True, null=True)
    # 销售预计下次跟进的时间，也没啥吊用

    # 用户表中存放的是自己公司的所有员工
    consultant = models.ForeignKey('UserInfo', verbose_name='销售', related_name='customers', blank=True, null=True,
                                   on_delete=models.CASCADE)

    class_list = models.ManyToManyField(to='Classlist', verbose_name='已报班级',blank=True, null=True )

    def __str__(self):
        return self.name + ':' + self.qq
    def records(self):
        return

    def status_show(self):
        status_color = {
            'signed': 'yellow',
            'unregistered': 'red',
            'studying': 'green',
            'paid_in_full': 'lightblue',
        }
        return mark_safe(f'<span style="background-color:{status_color[self.status]}">{self.get_status_display()}</span>')

class Classlist(models.Model):
    """
    班级表
    """
    course = models.CharField('课程名称', max_length=64, choices=course_choices)
    semester = models.IntegerField('学期')
    campuses = models.ForeignKey(to='Campuses', verbose_name='校区', on_delete=models.CASCADE)
    price = models.IntegerField('学费', default=10000)
    memo = models.CharField('说明', blank=True, null=True, max_length=100)
    start_date = models.DateField('开班日期')
    graduate_date = models.DateField('结业日期', blank=True, null=True)

    teachers = models.ManyToManyField(to='UserInfo', verbose_name='老师')

    class_type = models.CharField(choices=class_type_choices, max_length=64, verbose_name='班额及类型', blank=True,
                                  null=True)

    class Meta:
        unique_together = ('course', 'semester', 'campuses')  # 联合唯一

    def __str__(self):
        return f'python{self.semester}期：' + self.course


class Campuses(models.Model):
    """
    校区表
    """
    name = models.CharField(verbose_name='校区', max_length=64)
    address = models.CharField(verbose_name='详细地址', max_length=512, blank=True, null=True)

    def __str__(self):
        return self.name

#部门表
class Department(models.Model):
    """
    部门表
    """
    name = models.CharField(max_length=32,verbose_name='部门名称')
    count = models.IntegerField(verbose_name='部门人数')


#跟进记录

class ConsultRecord(models.Model):
    customer = models.ForeignKey(to='Custumer',verbose_name='咨询的客户')
    note = models.TextField(verbose_name='跟进详情')
    status = models.CharField('跟进状态',choices=seek_status_choices,max_length=8,help_text='客户此时的状态')

    consultant = models.ForeignKey('UserInfo',verbose_name='跟进人',related_name='records')
    #related_name:自定义外键属性
    #查询方式如：查询某条跟进记录的跟进人 ,正向查询:models.ConsultRecord.objects.get(xxx).customer.name
    #models.ConsultRecord.objects.get(xxx).records.name
    date = models.DateTimeField('跟进日期',auto_now_add=True)

    delete_status = models.BooleanField(verbose_name='删除状态',default=False)
    #销售删除表只是将这个字段设置为false，实际上还是存在

    def __str__(self):
        return str(self.customer) + str(self.consultant)

#报名表
class Enrollment(models.Model):
    """
    报名表
    """
    why_us = models.TextField('为什么报名',max_length=1024,default=None,blank=True, null=True)
    your_expectation =models.TextField('学完想达到的具体期望',max_length=1024,blank=True, null=True)
    encroll_date = models.DateTimeField('报名日期',auto_now_add=True)
    contract_approved = models.BooleanField('审批通过',help_text='在审阅完学员的资料无误后，勾选此项，合同即生效',default=False)
    memo = models.TextField('备注',blank=True, null=True)
    delete_status = models.BooleanField('删除状态',default=False)
    customer = models.ForeignKey(to='Custumer',verbose_name='客户名称')
    school = models.ForeignKey('Campuses',verbose_name='校区')
    enrolment_class = models.ForeignKey(to='Classlist',verbose_name='所报班级')

    def __str__(self):
        return str(self.customer) +':'+str(self.memo)
    class Meta:
        unique_together = ('enrolment_class','customer')

#课程记录表
class CourseRecord(models.Model):
    day_num = models.IntegerField('节次',help_text='填写几节课，或者是几天的课程')
    date = models.DateTimeField(auto_now_add=True,verbose_name='上课时间')
    course_title = models.CharField('课程标题',max_length=64,null=True,blank=True)
    course_memo = models.TextField('课程内容',max_length=300,null=True,blank=True)
    has_homework = models.BooleanField('本节课有作业',default=True)
    homework_title = models.CharField('作业标题',max_length=64,blank=True,null=True)
    homework_memo = models.TextField('作业描述',max_length=500,blank=True,null=True)
    scoring_point = models.TextField('得分点',max_length=300,blank=True,null=True)
    re_class = models.ForeignKey(to='Classlist',verbose_name='班级')
    teacher = models.ForeignKey('UserInfo',verbose_name='讲师')

    class Meta:
        unique_together = ('re_class','day_num')
    def __str__(self):
        return str(self.course_title)+ ':' +str(self.day_num)

#学习记录表
class StudyRecord(models.Model):

    class Meta:
        unique_together = ('course_record','student')

    attendance = models.CharField('考勤',choices=addtendance_choices,default='checked',max_length=64)
    score = models.IntegerField('课程成绩',choices=score_choices,default=-1)
    homework_note = models.CharField(max_length=300,verbose_name='作业批语',blank=True,null=True)
    date = models.DateField(auto_now_add=True)
    note = models.CharField('备注',max_length=300,blank=True,null=True)
    homework = models.FileField(verbose_name='作业文件',blank=True,null=True,default=None)
    course_record = models.ForeignKey('CourseRecord',verbose_name='某个课程')
    student = models.ForeignKey('Custumer',verbose_name='学员')

    def __str__(self):
        return self.course_record.course_title +':'+self.student.name
#身份信息表
class Role(models.Model):
    name = models.CharField(max_length=12)
    permissions = models.ManyToManyField(to='Permission')
    def __str__(self):
        return self.name


#一级菜单
class Menu(models.Model):
    title = models.CharField(max_length=16)

    def __str__(self):
        return self.title

#权限表
class Permission(models.Model):
    url = models.CharField(max_length=32)
    title = models.CharField(max_length=32)
    is_menu = models.BooleanField(default=False)
    menus = models.ForeignKey('Menu',default=None)
    def __str__(self):
        return self.title




