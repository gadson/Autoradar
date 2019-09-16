#from rest_framework.routers import DefaultRouter
from .views import *
from django.conf.urls.static import static


#router = DefaultRouter()
#router.register(r'articles', ArticleViewSet)




#urlpatterns = router.urls

from django.conf.urls import url
#from . import views


urlpatterns = [
    #url(r'^$', index, name='index'),
    url(r'^view/$', view, name='view'),
    url(r'^edit/$', edit, name='edit'),
    url(r'^edit_mobile/$', edit_mobile, name='edit_mobile'),
    url(r'^object/$', object, name='object'),
    url(r'^password/$', password, name='password'),
    url(r'^backup/$', backup, name='backup'),
    url(r'^object_mobile/$', object_mobile, name='object_mobile'),
    url(r'^add/$', add, name='add'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^mov/$', main, name='main'),
    url(r'^ev/$', event, name='event'),
    url(r'^policy/$', policy, name='policy'),
    url(r'^login_mobile/$', login_mobile, name='login_mobile'),
    url(r'^mon/$', monitor, name='monitor'),
    url(r'^register_mobile/$', register_mobile, name='register_mobile'),
    url(r'^mobile/$', mobile, name='mobile'),
    url(r'^$', index, name='index'),
]