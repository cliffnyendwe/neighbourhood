
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^member/(?P<user_username>\w+)/$', views.profile, name='userprofile'),
    url(r'^(\w+)/edit$', views.editprofile, name='editprofile') ,
    url (r'^hood/updates/post/$' ,views.post_update , name='updates' ) ,
    url(r'^search/hood/$', views.search, name='search'),
    url (r'^hood/(?P<hood_name>\w+)/$' , views.hood_details , name = 'hood_details' ) ,
    url(r'^hood/$' , views.create_hood , name='new_hood'),
    url(r'^comment/(?P<update_id>\d+)', views.comment, name='comment'),
    url(r'^business/' , views.business , name='business' ) , 
    url(r'^new/business/' , views.newbusiness , name='newbusiness' ) , 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
