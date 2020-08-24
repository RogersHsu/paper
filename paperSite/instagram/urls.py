"""paperSite URL Configuration

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
from django.contrib import admin
from django.urls import path
from . import views
# from views import index

urlpatterns = [

    path('', views.index, name='instagram'),
    path('search', views.search),
    path('getData/<str:newType>/<int:postNum>', views.getData, name='getData'),
    path('recommend', views.recommend, name='recommend'),
    # path('recommendNew/<str:recommend>', views.recommendNew),
    path('getSysets/<str:input>', views.getSysets, name='getSysets'),
    path('recommendNewUser', views.recommendNewUser, name='recommendNewUser'),
    path('recommendNewType', views.recommendNewType, name='recommendNewType'),
    path('currentTypes', views.currentTypes, name='currentTypes'),
    path('currentUsers', views.currentUsers, name='currentUsers'),
    path('getUsers/<int:postNum>', views.getUsers, name='getUsers'),
    path('questionnaire_animal', views.questionnaire_animal, name='questionnaire_animal'),
    path('questionnaire_vehicle', views.questionnaire_vehicle, name='questionnaire_vehicle'),
    path('getUserUrls/<str:userName>', views.getUserUrls, name='getUserUrls'),
    path('submitScore/<str:userName>/<int:value1>/<int:value2>/<str:qType>', views.submitScore, name='submitScore'),

    # 以下內容不在論文中，多做的尚未完成，就沒有在操作手冊說明
    path('currentTypes_admin', views.currentTypes_admin, name='currentTypes_admin'),
    path('getAdminData/<str:model>/<str:newType>/<int:postNum>', views.getAdminData, name='getData'),
    path('ex_results_animal', views.ex_results_animal, name='ex_results_animal'),
    path('ex_results_vehicle', views.ex_results_vehicle, name='ex_results_vehicle'),
    path('getUserEx/<str:userName>', views.getUserEx, name='getUserEx')

]
