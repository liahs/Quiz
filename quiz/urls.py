"""quiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from play import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='home'),
    path('login/',views.log_in,name='log_in'),
    path('logout/',views.log_out,name='log_out'),
    path('qlist/',views.qlist,name='qlist'),
    path('progress/',views.progress,name='progress'),
    path('check/',views.check,name='check'),
    path('signup/',views.sign_up,name='sign_up'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('add_qans/',views.add_qans,name='add_qans'),
    path('pas_fail/',views.pass_fail,name='pass_fail'),
    path('check_user/',views.check_user,name='check_user'),
    path('forget_pass/',views.forget_pass,name="forget_pass"),
    path('resetpass/',views.resetpass,name='resetpass')
]
