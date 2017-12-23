from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from post import views
from django.views.generic import RedirectView

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^post/', include('post.urls')),
    url(r'^resume/$', TemplateView.as_view(template_name='resume/index.html'),name='resume_cv'),
]

urlpatterns += [
    url(r'^$', RedirectView.as_view(url="/post/list", permanent=True)),
]

urlpatterns +=[
    url(r'^accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)