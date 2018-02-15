from django.shortcuts import render,HttpResponse,redirect
from django.conf.urls import url
from user import models
from user.forms_class import Register,Login
from static.plugins.piccode import piccode
from io import BytesIO
import time

def logconfirm(wrapper):
    '''
    登录状态装饰器
    :param wrapper:
    :return:
    '''
    def fun(request,param,*args,**kwargs):
        print(param)
        if param == str(request.session.get('uid')):
            res = wrapper(request,param,*args,**kwargs)
            return res
        else:
            return HttpResponse('没有权限偷窥别人隐私！')
    return fun


def register(request):
    '''
        注册函数，通过form组件验证和生成html，iframe伪造ajax上传图片，随机验证码，完成注册页面业务

        :param request:
        :return:
        '''
    if request.method == 'GET':
        form = Register(request)
        return render(request, 'user/register.html', {'form': form, })
    else:
        form = Register(request, request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            data = models.User.objects.filter(name=name)
            if not data:
                form.cleaned_data.pop('pwd2')
                form.cleaned_data.pop('piccode')
                rg_time = time.time()
                form.cleaned_data['rg_time'] = rg_time
                import os
                img = request.FILES.get('avatar')
                file_path = os.path.join('static/images/avatar', str(time.time()) + img.name)
                with open(file_path, 'wb') as f:
                    for chun in img.chunks():
                        f.write(chun)
                form.cleaned_data['avatar'] = file_path
                models.User.objects.create(**form.cleaned_data)
                return redirect('/login.html')
            else:
                msg = '账号已存在'
                return render(request, 'user/register.html', {'form': form, 'msg': msg})
        return render(request, 'user/register.html', {'form': form})


def check_code(request):
    '''
    返回验证图片
    :param request:
    :return:
    '''
    img, code = piccode(120, 30)
    stream = BytesIO()
    img.save(stream, 'png')
    codedata = stream.getvalue()
    request.session['piccode'] =code
    return HttpResponse(codedata)


def login(request):
    '''
        登录函数
        :param request:
        :return:
        '''
    if request.method == 'GET':
        uid = request.session.get('uid')
        if uid:
            return redirect('/home/%s.html' % uid)
        form = Login(request)
        return render(request, 'user/login.html', {'form': form})
    else:
        form = Login(request, request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            pwd = form.cleaned_data.get('pwd')
            session = request.POST.get('logrecord')
            data = models.User.objects.filter(name=name, pwd=pwd).first()
            if data:
                request.session['uid'] = data.uid
                if session:
                    request.session.set_expiry(259200)
                return redirect('/home/%s.html' % data.uid)
        form = Login(request, request.POST)
        msg = '用户名或密码错误'
        return render(request, 'user/login.html', {'form': form, 'msg': msg})


@logconfirm
def home(request,param):
    '''
    个人主页,展示个人详细信息
    :param request:
    :return:
    '''
    id = param
    data = models.User.objects.filter(uid=id).first()
    return render(request,'user/home.html',{'data':data})


def logout(request):
    '''
    退出登录状态
    :param request:
    :return:
    '''
    del request.session['uid']
    return redirect('/login')







urlpatterns=[
    url(r'^register.html$',register),
    url(r'^check_code/',check_code),
    url(r'^login.html$',login),
    url(r'^home/(\d+).html$',home),
    url(r'^logout/$',logout),

]
