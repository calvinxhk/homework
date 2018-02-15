
from django.conf.urls import url,include


urlpatterns = [
    url(r'^admin/',include('backstage.views')),
    url(r'',include('user.views')),
]
