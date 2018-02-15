from django.shortcuts import render,redirect,HttpResponse
from django.conf.urls import url
from user.forms_class import Login
from backstage import models
from user import models as userinfo
from static.plugins.分页器 import PageX
from user.forms_class import Register

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
        if request.session['rid']:
            data = userinfo.User.objects.all()
            url = request.path
            page = request.GET.get('page')
            Page = PageX(data,url,30,page)
            return render(request, 'backstage/backstage.html',{'page':Page})
        else:
            redirect('/admin/login.html')

@logconfirm
def backgroup(request):
    '''
    用户组管理界面
    :param request:
    :return:
    '''


    return render(request,'backstage/backgroup.html')

@logconfirm
def detail(request,param):
    data = userinfo.User.objects.filter(uid=param).first()
    return render(request,'backstage/detail.html',{'data':data})


@logconfirm
def useradd(request):
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
                return redirect('backstage.html')
            else:
                msg = '账号已存在'
                return render(request, 'backstage/adduser.html', {'form': form, 'msg': msg})
        return render(request, 'backstage/adduser.html', {'form': form})

@logconfirm
def userdel(request):
    if request.method =='POST':
        ids = request.POST.get("id").split(',')
        for id in ids[:-1]:
            userinfo.User.objects.filter(uid=id).delete()
        return HttpResponse('ok')

@logconfirm
def userupdate(request):
    if request.method=="POST":
        print(request.POST)
    return HttpResponse('ok')


urlpatterns = [
    url(r'login.html$',login),
    url(r'backstage.html$',backstage),
    url(r'backgroup.html$',backgroup),
    url(r'detail/(\d+).html',detail),
    url(r'backstage/add.html$',useradd),
    url(r'del.html$',userdel),
    url(r'update.html$',userupdate)



]
