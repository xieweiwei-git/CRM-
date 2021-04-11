from django.utils.safestring import mark_safe


class MyPagenation(object):
    """
    sum_obj:所有要展示的对象个数
    page_num:当前页
    PER_PAGE_NUM：每页展示信息条数
    PER_NUM_SHOW：需要展示的页脚数
    """

    def __init__(self,sum_obj,page_num,PER_PAGE_NUM,PER_NUM_SHOW):
        print('sum_obj'+f':{sum_obj}')

        self.a, self.b = divmod(sum_obj, PER_PAGE_NUM)
        # 首先获取page的值
        try:
            self.page_num = int(page_num)
        except:
            self.page_num = 1
        # if PER_PAGE_NUM:
        #     print('PER_PAGE_NUM:',PER_PAGE_NUM)
        #     self.a += 1
        if self.b:
            print('PER_PAGE_NUM:',PER_PAGE_NUM)
            self.a += 1
        print(self.a, self.b)
        # 判断输入是否合法
        if self.page_num <= 0:
            self.page_num = 1
        elif self.page_num > self.a:
            self.page_num = self.a
        # 设置显示页数
        first_page = self.page_num - PER_NUM_SHOW // 2
        last_page = self.page_num + PER_NUM_SHOW // 2
        if self.a<5:
            first_page =  1
            last_page = self.a
        elif first_page <= 0:

            first_page = 1
            last_page = PER_NUM_SHOW

        elif last_page >= self.a:
            last_page = self.a
            first_page = self.a - PER_NUM_SHOW + 1

        self.first_page = first_page
        self.last_page = last_page
        print(self.first_page,self.last_page)

    def page_html(self,get_data,path):
        page_html = '<nav aria-label="Page navigation"><ul class="pagination">'
        get_data['page'] = 1
        print('last_page', get_data.urlencode())
        first_page = f'<li><a href="{path}?{get_data.urlencode()}" aria-label="Previous"><span aria-hidden="true">首页</span></a></li>'
        # first_page = f'<li><a href="/customers/?page=1" aria-label="Previous"><span aria-hidden="true">首页</span></a></li>'
        page_html +=first_page
        # 向上翻页
        if self.page_num <= 1:
            pre_page = f'<li class="disabled"><a href="#" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'
        else:
            get_data['page'] = self.page_num - 1
            print('last_page',get_data, get_data.urlencode())
            pre_page = f'<li><a href="{path}?{get_data.urlencode()}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'
        page_html += pre_page
        # 循环生成页面
        for i in range(self.first_page, self.last_page + 1):
            get_data['page'] = i  # {‘name’:xxx,'search_type':'qq','page':xx}
            print('xunhuan', get_data.urlencode())
            if i == self.page_num:
                page_html += f'<li class="active"><a href="{path}?{get_data.urlencode()}">{i}</a></li>'
            else:

                page_html += f'<li><a href="{path}?{get_data.urlencode()}">{i}</a></li>'
                # page_html += f'<li><a href="/customers/?page={i}">{i}</a></li>'
        # 向下翻页
        if self.page_num >= self.a:
            next_page = '<li class="disabled"><a href="#" aria-label="Next"><span aria-hidden="true" >&raquo;</span></a></li>'
        else:

            get_data['page'] = self.page_num+1
            print('next_page', get_data.urlencode())
            next_page = f'<li><a href="{path}?{get_data.urlencode()}" aria-label="Next"><span aria-hidden="true" >&raquo;</span></a></li>'
            # next_page = f'<li><a href="/customers/?page={self.page_num + 1}" aria-label="Next"><span aria-hidden="true" >&raquo;</span></a></li>'
        page_html += next_page

        get_data['page'] = self.a
        print('last_page', get_data.urlencode())
        last_page = f'<li><a href="{path}?{get_data.urlencode()}" aria-label="Next"><span aria-hidden="true" >尾页</span></a></li></ul></nav>'
        # last_page = f'<li><a href="/customers/?page={self.a + 1}" aria-label="Next"><span aria-hidden="true" >尾页</span></a></li></ul></nav>'
        page_html+=last_page
        return mark_safe(page_html)

