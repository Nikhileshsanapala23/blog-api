from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create-post/', views.create_post, name='create_post'),
    path('posts/', views.list_posts, name='list_posts'),
    path('post/<int:id>/', views.post_detail, name='post_detail'),
    path('post/<int:id>/comment/', views.create_comment, name='create_comment'),
]