"""tabeasy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include, path
from ajax_select import urls as ajax_select_urls

from tourney import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('accounts/', include('accounts.urls')),
    path('', include('tourney.urls')),
    path('submission/', include('submission.urls', namespace='submission')),
    path('load_teams', views.load_teams, name='load_teams'),
    path('load_judges', views.load_judges, name='load_judges'),
    path('load_sections', views.load_sections),
    path('load_amta_witnesses', views.load_amta_witnesses),
    path('load_paradigms', views.load_paradigms),
    path('donate', views.donate, name='donate'),
    url(r'^ajax_select/', include(ajax_select_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
