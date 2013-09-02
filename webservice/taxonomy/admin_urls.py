from django.conf.urls import patterns

urlpatterns = patterns('',
   (r'^tree/$', 'taxonomy.admin_views.tree'),
)
