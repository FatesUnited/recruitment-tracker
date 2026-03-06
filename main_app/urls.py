from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('members/', views.members_index, name='members_index'),
    path('members/<int:member_id>/', views.member_detail, name='member_detail'),
    path('historical/', views.historical, name='historical'),
    path('graduation/', views.graduation, name='graduation'),
    path('attrition/', views.attrition, name='attrition'),
    path('analytics/', views.analytics, name='analytics'),
]