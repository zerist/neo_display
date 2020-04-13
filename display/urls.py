from django.urls import path
from . import views

app_name = 'display'
urlpatterns = [
    path('', views.index, name='index'),
    path('test', views.test, name='test'),
    path('search/<str:text>', views.search, name='search'),
    path('detail/<str:code>', views.detail, name='detail'),
    path('nearNode/<str:code>/<int:level>', views.nearNode, name='nearNode')
]