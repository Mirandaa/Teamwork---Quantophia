from django.urls import path

from . import views
from django.urls import include, path


urlpatterns = [
    path('', views.index, name='index'),
    path('banktest', views.runbanktest, name='banktest'),
    path('/getticker', views.buildAssetClass, name='buildAssetClass'),

]
