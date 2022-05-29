from django.urls import path
from . import views

urlpatterns = [
    path('',views.getRoutes),
    path('posts',views.getPosts),
    path('posts/create',views.createPost),
    # path('posts/update/<str:pk>',views.updatePost),
    # path('posts/delete/<str:pk>',views.deletePost),
    # path('posts/<str:pk>',views.getPost),
    path('register',views.registerUser),
    path('login',views.loginUser),
    path('createAddiction',views.createAddiction),
    path('info',views.getInfo),
    path('explore',views.explore),
    path('explore/<str:pk>',views.getInfoExplore),
    path('explore/<str:pk>/posts',views.getPostExplore),
    path('search/<str:pk>',views.search),
	path('imgupload',views.ImgCloudinaryUpload)
]