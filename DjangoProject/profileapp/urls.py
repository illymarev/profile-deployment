from django.urls import path, include
from django.views.i18n import JavaScriptCatalog
from . import views

app_name = 'profile'

urlpatterns = [
    path('<int:pk>/profile/', views.ShowProfile.as_view(), name='showprofile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('<int:pk>/update/', views.UpdateProfile.as_view(), name='updateprofile'),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('', views.main_page_redirect, name='redirect-page')
]
