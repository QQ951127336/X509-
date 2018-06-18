"""ManagerProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from CertificateWeb import views as webViews
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',webViews.home),
    url(r'^userPage/',webViews.userPage),
    url(r'^loginBehavior/',webViews.loginBehavior),
    url(r'^registerBehavior/',webViews.registerBehavior),
    url(r'^applyCerBehavior/',webViews.applyCerBehavior),
    url(r'^showApplyCerList/',webViews.showApplyCerList),
    url(r'^getCertificate/',webViews.getCertificate),
    url(r'^showCertificate/',webViews.showCertificate),
    url(r'^applyForRevoke/',webViews.applyForRevoke),
    url(r'^showApplyForRevokeList/',webViews.showApplyForRevokeList),
    url(r'^doRevoke/',webViews.doRevoke),
    url(r'^checkRevoke/',webViews.checkRevoke),
]
