from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('members/', views.members_index, name='members_index'),
    path('members/<int:member_id>/', views.member_detail, name='member_detail'),
    path('members/create/', views.MemberCreate.as_view(), name='member_create'),
    path('members/<int:pk>/update/', views.MemberUpdate.as_view(), name='member_update'),
    path('members/<int:pk>/delete/', views.MemberDelete.as_view(), name='member_delete'),
    path(
        'members/<int:member_id>/add_comment/', 
        views.add_comment, 
        name='add_comment'
    ),
    path('accounts/signup/', views.signup, name='signup'),
    path('recruitment/', views.recruitment, name='recruitment'),
    path('historical/', views.historical, name='historical'),
    path('graduation/', views.graduation, name='graduation'),
    path('attrition/', views.attrition, name='attrition'),
    path('analytics/', views.analytics, name='analytics'),
]