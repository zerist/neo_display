from django.urls import path
from . import views

app_name = 'display'
urlpatterns = [
    path('', views.index, name='index'),
    path('test', views.test, name='test'),
    path('search/<str:text>', views.search, name='search'),
    path('detail/<str:code>', views.detail, name='detail'),
    path('nearNode/<str:code>/<int:level>', views.nearNode, name='nearNode'),
    path('nearNodeByCategory/<str:category>', views.nearNodeByCategory, name='nearNodeByCategory'),
    path('svgMode/<str:code>', views.svgMode, name='svgMode'),
    path('nodeJSON/<str:name>', views.getNodeJSON, name='nodeJSON'),
    path('subNode/<str:name>', views.subNode, name='subNode')
]