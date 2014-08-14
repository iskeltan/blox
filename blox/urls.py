import os
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

here = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)


urlpatterns = patterns('',
    url(r'^$', 'post.views.home', name='home'),
    url(r'^post/(?P<post_id>[0-9]+)/$','post.views.detail', name='detail'),
    url(r'^add_comment/(?P<post_id>[0-9]+)/(?P<obj_name>.*)/(?P<obj_id>[0-9]+)/$','post.views.add_comment', name='add_comment'),

    url(r'^account/login/$', 'account.views.login_view', name='login'),
    url(r'^account/register/$','account.views.register_view', name='register'),
    url(r'^account/logout/$', 'account.views.logout_view', name='logout'),
    url(r'^account/activate/(?P<activation_code>.*)/', 'account.views.activate_user', name='activate_user'),

    url(r'^comment/activate/(?P<activation_code>.*)/$','post.views.activate_comment', name='activate_comment'),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.views.static',
   (r'^static/(?P<path>.*)$',
       'serve', {
        #static directory root
        'document_root': here('../static'),
        #directory listing
        'show_indexes': True }),)

