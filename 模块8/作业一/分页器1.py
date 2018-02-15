class PageX:
    '''
    需要传入 数据列表，每页显示条数，
    '''

    def __init__(self,data,perpage,page,pageamount=3):
        self.data = data
        self.pageamount = pageamount
        self.perpage = perpage
        if len(data)%perpage:
            self.max_page_number = len(data)//perpage+1
        else:
            self.max_page_number = len(data)//perpage
        try:
            self.page = int(page)
        except Exception:
            self.page = 1

        if self.page not in range(1,self.max_page_number+1):
            self.page = 1
        self.previous_page_number = self.page-1
        self.next_page_number = self.page+1


    def has_previous(self):
        if self.previous_page_number:
            return True
        else:return False

    def has_next(self):
        if self.next_page_number <self.max_page_number:
            return True
        else:return False

    def object_list(self):
        start = self.previous_page_number*self.perpage
        end = self.page*self.perpage
        return self.data[start:end]


    def page_list(self):
        paginator=[]
        page_bgein= self.page-self.pageamount
        page_end = self.page+self.pageamount
        if page_bgein < 1:
            page_bgein = 1
            page_end = 2 * self.pageamount + 1
        if page_end >= self.max_page_number:
            page_end = self.max_page_number
            page_bgein = self.max_page_number - 2 * self.pageamount - 1
        for i in range(page_bgein,page_end+1):
            if i == self.max_page_number:
                continue
            p = '<a style="display:inline-block;width:20px;heigth:20px;padding:5px" href="/index/?page='+str(i)+'">'+str(i)+'</a>'
            paginator.append(p)
        return paginator



