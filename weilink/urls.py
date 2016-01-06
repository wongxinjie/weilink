from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'weilink.views.home', name='home'),
    # url(r'^weilink/', include('weilink.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', 'weilink.views.index', name='index'),
    url(r'^login/$', 'weilink.views.people_login', name='login'),
    url(r'^signup/$', 'weilink.views.signup', name='signup'),
    url(r'^create_verifycode', 'weilink.views.create_verifycode', name='create_verifycode'),
    url(r'^match_email/$', 'weilink.views.match_email', name='match_email'),
    url(r'^authemail', 'weilink.views.auth_email', name='auth_email'),
    url(r'^search', 'weilink.views.search', name='search'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^people/', include('people.urls')),
    url(r'^message/', include('message.urls')),
    url(r'^letter/', include('letter.urls')),
    url(r'^manager/', include('manager.urls')),
    url(r'^reminder/', include('reminder.urls')),
    url(r'^photo/', include('photoes.urls')),
)
