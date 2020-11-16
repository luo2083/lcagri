from django.urls import path
from . import views
urlpatterns = [
    path('test', views.test_session),
    path('test2', views.test_session2),
    path('user', views.UserView.as_view()),
    path('authorize', views.authorize, name='authorize'),
    path('status', views.get_staus, name='status'),
    path('logout', views.logout, name='logout')
]