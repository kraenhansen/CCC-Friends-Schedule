from django.conf.urls import patterns, include, url
from .admin import admin_site

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ccc_friend_schedule.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^schedule\.xml$',
    	'ccc_friend_schedule.views.schedule', name='schedule'),
    url(r'^attend/(?P<user_token>[^/]*)/(?P<event_id>\d*)/$',
    	'ccc_friend_schedule.views.attend', name='attend'),
    
    url(r'^admin/', include(admin_site.urls)),
)
