"""LNContract URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from django.urls import include, path

from contracts import views 

urlpatterns = [
    path('', views.index),
    path('connect/<int:pk>', views.connect),
    path('connect_cp/<int:pk>',views.connect_cp),
    path('contracts/', views.contracts),
    path('contract/<int:pk>', views.contract),
    path('open_channel/<int:pk>', views.open_channel)
    
]
 