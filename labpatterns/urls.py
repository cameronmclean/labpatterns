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
    url(r'^newsolutionale/$', 'patterns.views.add_new_solution', name='new_solution'),
    url(r'^related/$', 'patterns.views.see_related_terms', name='see_related'),
    url(r'^match/$', 'patterns.views.ontology_lookup', name='match'),
    url(r'^supporting/$', 'patterns.views.add_supporting', name='supporting'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
)
