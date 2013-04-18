from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', redirect_to, {'url': '/polls/'}),
    (r'^polls/', include('questions.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^static_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
)
