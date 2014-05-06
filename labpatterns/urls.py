from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'labpatterns.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'patterns.views.home', name='home'),
    url(r'^new/$', 'patterns.views.add_new_pattern_name', name='new_name'),
)
