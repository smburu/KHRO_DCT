"""
KHRO Data Capture URL Configurations, This Django Tool is developed by Dr. Stephen Mburu,PhD
Health Infomatics specialist, University of Nairobi  - Kenya: smburu@uonmbiac.ke\
"""
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url,include
from django.conf import settings #to facilitate viewing on browser in-built pdf
from django.conf.urls.static import static #facilitate display of resources
from home import views

"""
KHRO Data Capture URL Configurations, This Django Tool is developed by Dr. Stephen Mburu,PhD
Health Infomatics specialist, University of Nairobi  - Kenya: smburu@uonmbiac.ke\
"""
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url,include
from django.conf import settings #to facilitate viewing on browser in-built pdf
from django.conf.urls.static import static #facilitate display of resources
from home import views
from rest_framework.documentation import (
    include_docs_urls, get_schemajs_view)

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='KHRO API Endpoints')

# Register URL patterns for hitting KHRO endpoints for the registered models
api_patterns = [
    url(r'^', include(
        ('regions.urls', 'rg'), namespace='rg')),
    url(r'^', include(
        ('indicators.urls', 'indicators'), namespace='indicators')),
    url(r'^', include(
        ('research.urls', 'research'), namespace='research')),
    url(r'^', include(
        ('elements.urls', 'elements'), namespace='elements')),
    url(r'^', include(
        ('settings.urls', 'settings'), namespace='settings')),
    url(r'^', include(
        ('home.urls', 'home'), namespace='home')),
    url(r'^', include(
        ('commodities.urls', 'Commodities'), namespace='commodities')),
]

urlpatterns = [
    # Site-based URL patterns for hitting KHRO web portal login and dashboard
    path('', views.index, name='index'), # for hitting at the custom login index page
    path('admin/', admin.site.urls),

    path('accounts/login/', views.login_view, name='login'), # URL for Login call to custom view
    path('datawizard/', include('data_wizard.urls')), # Call to smart data import wizard
	# Reset password urls
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Change password urls
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # API-based URL patterns for hitting KHRO endpoints for consuming data in JSON
    url(r'^api/', include((api_patterns, 'api'), namespace='api')),
    path('docs/', include_docs_urls(title='KHRO', public=False)),
    path('schema/', get_schemajs_view(title='KHRO', public=False)),
    path(r'swagger-docs/', schema_view),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #configured to access root media
