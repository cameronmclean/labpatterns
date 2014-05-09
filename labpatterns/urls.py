from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'labpatterns.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'patterns.views.home', name='home'),
    url(r'^new/$', 'patterns.views.add_new_pattern_name', name='new_name'),
    url(r'^newprobtext/$', 'patterns.views.add_new_prob_and_context', name='new_probtext'),
    url(r'^newforce/$', 'patterns.views.add_new_force', name="new_force"),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
)
