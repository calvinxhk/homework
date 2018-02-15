from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse

class test(MiddlewareMixin):
    def process_request(self,requset):
        print('执行 process_request')
        return HttpResponse('stop')

    def process_response(self,request,response):
        print('执行process_response')
        return response
