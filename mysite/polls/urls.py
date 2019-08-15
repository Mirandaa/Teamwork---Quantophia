from polls.view import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('getSecurity', views.buildAssetClass, name='buildAssetClass'),
    path('getResult', views.getResult, name='index'),

]



