from django.shortcuts import render,HttpResponse,redirect
from django.conf.urls import url
from report_system import models
from report_system.formsclass import Register,Login
from static.plugins.piccode import piccode
from io import BytesIO
import time
def index(request):
    '''
    主页函数
    :param request:
    :return:
    '''
    blockname = models.WebBlock.objects.all()
    data = models.User.objects.filter(name='rooter').first()


    return render(request, 'report_system/index.html',{'blockname':blockname,"data":data})


def register(request):
    '''
    注册函数，通过form组件验证和生成html，iframe伪造ajax上传图片，随机验证码，完成注册页面业务

    :param request:
    :return:
    '''
    if request.method == 'GET':
        form = Register(request)
        return render(request, 'report_system/register.html', {'form':form, })
    else:
        form = Register(request,request.POST,request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            data = models.User.objects.filter(name=name)
            if not data :

                form.cleaned_data.pop('pwd2')
                form.cleaned_data.pop('piccode')
                rg_time = time.time()
                form.cleaned_data['rg_time']=rg_time
                import os
                img = request.FILES.get('avatar')
                file_path = os.path.join('static/images/avatar', str(time.time())+img.name)
                with open(file_path, 'wb') as f:
                    for chun in img.chunks():
                        f.write(chun)
                form.cleaned_data['avatar'] = file_path
                models.User.objects.create(**form.cleaned_data)
                return redirect('/success/')
            else:
                msg='账号已存在'
                return render(request, 'report_system/register.html', {'form':form, 'msg':msg})
        return render(request, 'report_system/register.html', {'form':form})


def login(request):
    '''
    登录函数
    :param request:
    :return:
    '''
    if request.method=='GET':
        uid = request.session.get('uid')
        if uid:
            return redirect('/home?uid=%s'%uid)
        form = Login(request)
        return render(request,'report_system/login.html',{'form':form})
    else:
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        data = models.User.objects.filter(name=name,pwd=pwd).first()
        if data:
            request.session['uid'] = data.uid
            return redirect('/home?uid=%s'%data.uid)
        else:
            form=Login(request,request.POST)
            msg = '用户名或密码错误'
            return render(request, 'report_system/login.html', {'form': form,'msg':msg})


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

def avatarsave(request):
    '''
    浏览器不支持头像本地预览时，将头像图片存到服务器，临时保存
    :param request:
    :return:
    '''
    img = request.FILES.get('avatar')
    import os
    file_path = os.path.join('static/images/avatemp',img.name,str(time.time()))
    with open(file_path,'wb') as f:
        for chun in img.chunks():
            f.write(chun)
    return HttpResponse(file_path)

def home(request):
    uid = request.GET.get('uid')
    data = models.User.objects.filter(uid=uid).first()
    print(data)


    return render(request,'report_system/home.html',{"data":data})

def blogregister(request):
    return render(request,'report_system/blogregister.html')

def blog (request):
    return render(request,'report_system/blog.html')


def blogwirte (request):
    return render(request,'report_system/blogwirte.html')


def admin (request):


    return render(request,'report_system/admin.html')


def admin_login(request):
    return render(request,'report_system/admin_login.html')









urlpatterns = [
    url(r'^register$',register),
    url(r'^register/avatar$',avatarsave),
    url(r'^check_code/',check_code),
    url(r'^login$',login),
    url(r'^home',home),
    url(r'^admin$',admin),
    url(r'^admin_login$',admin_login),
    url(r'^blog/\d+$',blog),
    url(r'^blogregister$',blogregister),
    url(r'^blogwrite$',blogwirte),
    url(r'',index),

]
