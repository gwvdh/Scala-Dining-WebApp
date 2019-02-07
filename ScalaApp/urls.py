"""ScalaApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from UserDetails import views as UDviews
from django.contrib.auth.views import LoginView
from CreditManagement import views as CMviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('logout/', UDviews.log_out, name='logout'),
    path('register/', UDviews.RegisterView.as_view(), name='register'),
    path('user/', include('UserDetails.urls_user')),
    path('association/<association_name>/', include('UserDetails.urls_association')),
    path('credit/', include('CreditManagement.urls')),
    path('site/', include('General.urls')),
    path('', include('Dining.urls')),
    path('test', CMviews.TransactionTestView.as_view()),
    path('test/<user>', CMviews.TransactionTestView.as_view()),
    # Quadrivium OpenID Connect
    path('oidc/', include('mozilla_django_oidc.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

