
from django.urls import path, include
from blog import views
app_name = 'blog'

urlpatterns = [
    path('about/post<int:post_id>/', views.about, name='about'),
    path('delete/post=<int:post_id>/', views.delete, name='delete'),
    path('add/', views.add, name='add'),
    path('update/post=<int:post_id>/', views.update_blog, name='update'),
    path('comment/at/post=<int:post_id>/', views.add_comment, name='add_comment'),
    path('reply/at/comment=<int:comment_id>/', views.add_reply, name='add_reply'),
    path('delete/comment=<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('delete/reply=<int:reply_id>/', views.delete_reply, name='delete_reply'),
    path('edit/comment=<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('edit/reply=<int:reply_id>/', views.edit_reply, name='edit_reply'),

]
