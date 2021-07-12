"""djangostagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from dsuser.views import RegisterView, LoginView, logout
from post.views import (TimeLine, PostWrite, PostDetail, PostUpdateView, delete)

urlpatterns = [
    path('post/',include('post.urls', namespace='post')),
    path('admin/', admin.site.urls),
    path('', TimeLine.as_view(), name='timeline/'),
    path('user/register/', RegisterView.as_view() ,name='user/register/'),
    path('user/login/', LoginView.as_view(), name='user/login/'),
    path('user/logout/', logout, name='user/logout/'),

    path('timeline/', TimeLine.as_view(), name='timeline/'),
    path('post/write/', PostWrite.as_view(), name='post/write/'),
    path('post/<int:pk>/', PostDetail.as_view()),
    # path('post/update/<int:pk>/', PostUpdate.as_view()),
    path('post/delete/<int:id>/', delete ),

]
