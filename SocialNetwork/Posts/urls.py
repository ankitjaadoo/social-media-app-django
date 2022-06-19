from django.urls import path
from . import views
 
urlpatterns = [
    path('create', views.CreatePost),
    path('<str:username>/', views.Timeline), 
    path('<int:post_id>/delete', views.DeletePost),
    path('<int:post_id>', views.ShowPost), 
    path('<int:post_id>/like', views.Like),
    path('<int:post_id>/comment', views.Comment),
    path('search', views.Search),
]