from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:mgr.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^index/$','index.views.index', name='index'),
                       url(r'^servers/$','servers.views.servers', name='servers'),
                       url(r'^users/$','users.views.users', name='users'),
                       url(r'^projects/$','projects.views.projects', name='projects')
    # Examples:
    # url(r'^$', 'virt_mgr.views.home', name='home'),
    # url(r'^virt_mgr/', include('virt_admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
