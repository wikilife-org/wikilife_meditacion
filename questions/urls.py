from django.conf.urls.defaults import *

urlpatterns = patterns('questions.views',
    (r'^$', 'index'),
    (r'^(?P<person_id>\d+)/(?P<seq>\d+)/$', 'detail'),
    (r'^result/(?P<response_id>\d+)/$', 'result'),
    (r'^vote/', 'vote'),
    (r'^start/', 'start'),
    (r'^thanks/(?P<person_id>\d+)/$', 'thanks'),
    (r'^charts/', 'charts'),
    (r'^chart/(?P<chart_id>\d+)/$', 'chart'),
)
