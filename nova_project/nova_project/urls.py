from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from nova_project import views
from articles import views as article_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', article_views.article_list, name='homepage'),
    path('about/', views.about, name='about'),
    path('articles/', include('articles.urls')),
    path('accounts/', include('accounts.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)