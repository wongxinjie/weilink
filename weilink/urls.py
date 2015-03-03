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
    url(r'^login/$', 'weilink.views.login', name='login'),
    url(r'^signup/$', 'weilink.views.signup', name='signup'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^people/', include(people.urls)),
    url(r'^message/', include(message.urls)),
    url(r'^letter/', include(letter.urls)),
    url(r'^manager/', include(manager.urls)),
)
