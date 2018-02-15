from django.shortcuts import render,HttpResponse,redirect
from django.conf.urls import url
from django.forms import Form,fields,widgets
from 作业一 import models

def logtest(wrapper):
    def func(request,*args,**kwargs):
        user = request.session.get("user")
        if  user:
            result = wrapper(request,*args,**kwargs)
            return result
        else:
            return redirect('/login/')
    return func


@ logtest
def index(request):
    user = request.session.get("user")
    gender = request.session.get('gender')
    if gender == 'boy':
        data = models.UserGirl.objects.all()
        record = models.UserBoy.objects.filter(name='xhk').first().record.all()
        print(record)



    else:
        data = models.UserBoy.objects.all()
        record = models.UserGirl.objects.filter(name='')

    return render(request, 'index.html',{'user':user,'gender':gender,'data':data,"record":record})


def login(request):
    if request.method =='GET':
        user = request.session.get("user")
        if user:
            return redirect('/index/')
        return render(request,'login.html')
    else:
        user = request.POST.get('user')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        logsession =request.POST.get('logsession')
        print(logsession)
        if gender =='boy':
            data = models.UserBoy.objects.filter(name=user,password=password)
        else:
            data = models.UserGirl.objects.filter(name=user,password=password)
        if data:
            request.session['user'] = user
            request.session['gender'] = gender
            if logsession:
                request.session.set_expiry(1800)

            return redirect('/index/')
        else:
            return render(request,'login.html',{'msg':'登录失败！'})


# def test(requset):
#     if requset.method == 'GET':
#         result = Test()
#         return render(requset,'test.html',{'result':result})
#     else:
#         result = Test(requset.POST)
#         if result.is_valid():
#             return HttpResponse("正确")
#         else:
#             return render(requset,'test.html',{'result':result})

# class Test(Form):
#
#     user = fields.CharField(required=True,min_length=6,max_length=16,error_messages={
#         'required':'你他妈倒是写啊','max_length':'你闲着没事干打这么多字啊','min_length':'你太短了！'
#     },label='用户名')
#
#     password = fields.CharField(required=True,min_length=6,max_length=16)
#     def __init__(self,*args,**kwargs):
#         super(Test,self).__init__(*args,**kwargs)

def test(requset):
    if requset.method == 'GET':
        return render(requset,'test.html')
    else:
        status = True
        user = requset.POST.get('user')
        password = requset.POST.get('password')
        if user =='xhk' and password =='123456':
            msg ={'status':status,'answer':'ok'}
        else:
            msg={'answer':'fuckyou'}
        import json
        msg = json.dumps(msg)
        print(type(msg))
        return HttpResponse(msg)

def test1(requset):
    msg= requset.POST

    return HttpResponse(msg)

def test3(request):
    print(request.POST,request.FILES)
    files = request.FILES.get('文件')
    import os
    files_path = os.path.join('static',files.name)
    with open(files_path,'wb') as f:
        for chun in files.chunks():
            f.write(chun)
    print(files_path)
    return HttpResponse(files_path)


def jsonp(request):
    return render(request,'jsonp.html')


urlpatterns=[
    url(r'^test/',test),
    url(r'^login/',login),
    url(r'^index/',index),
    url(r'^test1/',test1),
    url(r'^test3/',test3),
    url(r'^jsonp',jsonp),


]