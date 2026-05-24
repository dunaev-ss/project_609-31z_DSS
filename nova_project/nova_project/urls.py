from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from nova_project import views
from news import views as news

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', news.article_list, name='homepage'),
    path('accounts/', include('accounts.urls')),
    path('news/', include('news.urls')),
    path('f1/', include('f1_project.urls')),
    path('charts/', include('charts.urls')),
    path('about/', views.about, name='about'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
