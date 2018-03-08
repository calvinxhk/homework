from django.shortcuts import render,redirect,HttpResponse
from django.conf.urls import url
from user.forms_class import Login
from backstage import models
from user import models as userinfo
from static.plugins.分页器 import PageX
from user.forms_class import Register
from django.db.models import Q,Count
from backstage.group_form import GroupADD,GUserADD

def login(request):
    '''
    登录页面
    :param request:
    :return:
    '''
    if request.method == 'GET':
        form = Login(request)
        return render(request, 'backstage/login.html', {'form': form})
    else:
        form = Login(request, request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            pwd = form.cleaned_data.get('pwd')
            data = models.Admin.objects.filter(name=name, pwd=pwd).first()
            if data:
                request.session['rid'] = data.rid
                return redirect('/admin/backstage.html')
        form = Login(request, request.POST)
        msg = '用户名或密码错误'
        return render(request, 'backstage/login.html', {'form': form, 'msg': msg})


def logconfirm(wrapper):
    '''
    登录状态确认装饰器
    :param wrapper: 除登录外的view视图函数
    :return:
    '''
    def inner(request,*args,**kwargs):
        if request.session.get('rid'):
            res = wrapper(request,*args,**kwargs)
            return res
        else:
            return redirect('/admin/login.html')
    return inner


@logconfirm
def backstage(request):
    '''
    用户管理界面
    :param request:
    :return:
    '''
    if request.method=='GET':
        data = userinfo.User.objects.all()
        url = request.path
        page = request.GET.get('page')
        Page = PageX(data,url,30,page)
        return render(request, 'backstage/backstage.html',{'page':Page})


@logconfirm
def detail(request,param):
    '''
    用户详细信息页面
    :param request:
    :param param: 用户uid
    :return:
    '''
    data = userinfo.User.objects.filter(uid=param).first()
    group = userinfo.GroupUser.objects.filter(uid=param)
    return render(request,'backstage/detail.html',{'data':data,"group":group})


@logconfirm
def useradd(request):
    '''
    增加用户页面
    :param request:
    :return:
    '''
    if request.method == 'GET':
        form = Register(request)
        return render(request, 'backstage/adduser.html', {'form': form, })
    else:
        form = Register(request, request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            data = userinfo.User.objects.filter(name=name)
            if not data:
                import os,time
                form.cleaned_data.pop('pwd2')
                form.cleaned_data.pop('piccode')
                rg_time = time.time()
                form.cleaned_data['rg_time'] = rg_time
                img = request.FILES.get('avatar')
                file_path = os.path.join('static/images/avatar', str(time.time()) + img.name)
                with open(file_path, 'wb') as f:
                    for chun in img.chunks():
                        f.write(chun)
                form.cleaned_data['avatar'] = file_path
                userinfo.User.objects.create(**form.cleaned_data)
                return redirect('/admin/backstage.html')
            else:
                msg = '账号已存在'
                return render(request, 'backstage/adduser.html', {'form': form, 'msg': msg})
        return render(request, 'backstage/adduser.html', {'form': form})


@logconfirm
def userdel(request):
    '''
    删除用户页面
    :param request:
    :return:
    '''
    if request.method =='POST':
        ids = request.POST.get("id").split(',')
        for id in ids[:-1]:
            userinfo.User.objects.filter(uid=id).delete()
        return HttpResponse('ok')

@logconfirm
def userupdate(request):
    '''
    更新用户信息
    :param request:
    :return:
    '''
    if request.method == "POST":
        for m in request.POST:
            if m =='csrfmiddlewaretoken':
                continue
            res = request.POST.getlist(m)
            uid = res[0]
            phone = res[1]
            userinfo.User.objects.filter(uid=uid).update(phone=phone)
    return HttpResponse('ok')

@logconfirm
def search(request):
    '''
    组合条件搜索用户信息
    :param request:
    :return:
    '''
    if request.method == 'POST':
        condition = request.POST.getlist('condition')
        value = request.POST.getlist('value')
        ckind = set(condition)
        conn = Q()
        for item in ckind:
            q = Q()
            q.connector='OR'
            n=0
            for data in condition:
                if data == item:
                    q.children.append((data,value[n]))
                n += 1
            conn.add(q,"AND")
        data=userinfo.User.objects.filter(conn)
        url = request.path
        page = request.GET.get('page')
        Page = PageX(data, url, 30, page)
        return render(request, 'backstage/backstage.html', {'page': Page})


@logconfirm
def backgroup(request):
    '''
    用户组管理界面
    :param request:
    :return:
    '''
    group = userinfo.Group.objects.all()
    data = userinfo.GroupUser.objects.all().values('gid').annotate(count = Count('gid'))
    return render(request,'backstage/backgroup.html',{'data':data,'group':group})


@logconfirm
def groupsearch(request):
    '''
    用户组条件搜索
    :param request:
    :return:
    '''
    if request.method == 'POST':
        condition = request.POST.getlist('condition')
        value = request.POST.getlist('value')
        ckind = set(condition)
        conn = Q()
        for item in ckind:
            q = Q()
            q.connector='OR'
            n=0
            for data in condition:
                if data == item:
                    q.children.append((data,value[n]))
                n += 1
            conn.add(q,"AND")
        group=userinfo.Group.objects.filter(conn)
        data = userinfo.GroupUser.objects.all().values('gid').annotate(count=Count('gid'))
        return render(request, 'backstage/backgroup.html',{'data':data,'group':group})
    else:
        return redirect('/admin/backstage.html')


@logconfirm
def groupadd(request):
    '''
    用户组增加
    :param request:
    :return:
    '''
    if request.method == 'GET':
        form = GroupADD()
        return render(request, 'backstage/addgroup.html', {'form': form, })
    else:
        form = GroupADD( request.POST)
        if form.is_valid():
            gname = form.cleaned_data.get('gname')
            data = userinfo.Group.objects.filter(gname=gname)
            if not data:
                userinfo.Group.objects.create(**form.cleaned_data)
                return redirect('/admin/backgroup.html')
            else:
                msg = '分组已存在'
                return render(request, 'backstage/addgroup.html', {'form': form, 'msg': msg})
        return render(request, 'backstage/addgroup.html', {'form': form})


@logconfirm
def groupdel(request):
    '''
    用户组删除
    :param request:
    :return:
    '''
    if request.method == "POST":
        res = request.POST.get('gid').split(',')
        for gid in res[:-1]:
            userinfo.GroupUser.objects.filter(gid=gid).delete()
            userinfo.Group.objects.filter(gid=gid).delete()
        return HttpResponse('TURE')
    else:
        return redirect('/admin/backgroup.html')


@logconfirm
def groupupdate(request):
    '''
    用户组更新名字
    :param request:
    :return:
    '''
    if request.method == "POST":
        for m in request.POST:
            if m =='csrfmiddlewaretoken':
                continue
            res = request.POST.getlist(m)
            gid = res[0]
            gname = res[1]
            userinfo.Group.objects.filter(gid=gid).update(gname=gname)
    return HttpResponse('ok')


@logconfirm
def gdetail(request,gid):
    '''
    跳转用户组所有成员页面
    :param request:
    :param gid:
    :return:
    '''
    group = userinfo.Group.objects.filter(gid=gid)
    data = userinfo.Group.objects.filter(gid=gid).first().groupuser_set.all().values(
        'uid__uid','uid__name','uid__phone',)
    return render(request,'backstage/gdetail.html',{'group':group,'data':data})


@logconfirm
def gdeluser(request):
    '''
    删除用户组中成员
    :param request:
    :return:
    '''
    if request.method == "POST":
        res = request.POST.get('gid').split(',')
        gid = res[0]
        for uid in res[1:-1]:
            userinfo.GroupUser.objects.filter(uid=uid,gid=gid).delete()
        return HttpResponse('TURE')
    else:
        return redirect('/admin/backgroup.html')


@logconfirm
def gadduser(request,gid):
    '''
    增加用户组中成员
    :param request:
    :return:
    '''
    if request.method == 'GET':
        form = GUserADD()
        group = userinfo.Group.objects.filter(gid=gid).first()
        return render(request, 'backstage/gadduer.html', {'form': form,'group':group})
    else:
        form = GUserADD( request.POST)
        group = userinfo.Group.objects.filter(gid=gid).first()
        if form.is_valid():
            uid = form.cleaned_data.get('uid')
            user = userinfo.User.objects.filter(uid=uid)
            if user:
                data = userinfo.GroupUser.objects.filter(uid=uid,gid=gid)
                if not data:
                    userinfo.GroupUser.objects.create(uid_id=uid,gid_id=gid)
                    return redirect('/admin/backgroup.html')
                else:
                    msg = '用户已存在'
                    return render(request, 'backstage/gadduer.html', {'form': form,'group':group, 'msg': msg})
        msg = '用户不存在'
        return render(request, 'backstage/gadduer.html', {'form': form,'group':group, 'msg': msg})

urlpatterns = [
    url(r'^login.html$',login),
    url(r'^backstage.html$',backstage),
    url(r'^detail/(\d+).html',detail),
    url(r'^backstage/add.html$',useradd),
    url(r'^del.html$',userdel),
    url(r'^update.html$',userupdate),
    url(r'^search.html$',search),
    url(r'^backgroup.html$',backgroup),
    url(r'^groupdel.html$',groupdel),
    url(r'^groupupdate.html$',groupupdate),
    url(r'^backstage/groupadd.html$',groupadd),
    url(r'^groupsearch.html$',groupsearch),
    url(r'^groupdetail/(\d+).html$',gdetail),
    url(r'^gdeluser.html$',gdeluser),
    url(r'^gadduser/(\d+).html',gadduser),




]
