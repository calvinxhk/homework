from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class TestLogMiddleware(MiddlewareMixin):

    def process_request(self,request):
        valid = ['/index','/register','/login','/check_code/']
        if request.path not in valid :
            if not request.session.get('uid') :
               return redirect('/login')



    def process_response(self,request,response):
        return response