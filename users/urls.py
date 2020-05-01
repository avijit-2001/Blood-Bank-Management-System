from django.urls import path
from . import views
app_name = 'users'

urlpatterns = [

    path('', views.home, name='home'),
    path('old/', views.old_home, name="old_post"),
    path('signup/donor/', views.sig_don, name='sig_don'),
    path('create/donor/', views.crp_don, name='crp_don'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('update/profile/', views.update, name='update'),
    path('signup/hospital/', views.sig_hos, name='sig_hos'),
    path('create/hospital/', views.crp_hos, name='crp_hos'),
    path('hospital/search/donor/', views.search_donor, name='search_donor'),
    path('request/donor<int:donor_id>/bg<str:blood_group>/city<str:city>/', views.make_request, name='make_request'),
    # blood_group, city, request_id
    path('undo/req/bg<str:blood_group>/city<str:city>/id=<int:request_id>/', views.undo_request, name='undo_request'),
    path('donor/new/request/view/', views.request_view_donor, name='request_view_donor'),
    path('donor/accept/request/request_id=<int:request_id>/', views.accept_request, name='accept_request'),
    path('donor/reject/request/request_id=<int:request_id>/', views.reject_request, name='reject_request'),
    path('hospital/view/repo/', views.view_repo, name='view_repo'),
    path('hospital/add/blood/repo', views.add_blood, name='add_blood'),
    path('hospital/remove/blood/repo', views.remove_blood, name='remove_blood'),
    path('hospital/active/request/', views.active_reqs, name='active_reqs'),
    path('hospital/approve/req=<int:request_id>/', views.approve, name='approve'),
    path('hospital/history/', views.view_history, name='view_history'),
    path('tongle', views.change, name='tongle'),
]