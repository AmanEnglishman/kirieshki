from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='list'),
    path('posts/<int:pk>/', views.post_detail, name='detail'),
    path('posts/<int:pk>/comments/', views.add_comment, name='add_comment'),
    path('posts/<int:pk>/like/', views.toggle_like, name='toggle_like'),
]
