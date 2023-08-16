from django.urls import path

from users.api import UserList, UserCreate, UserDetail

urlpatterns = [
  path('create/', UserCreate.as_view(), name='user-create'),
  path('users/', UserList.as_view(), name='user-list'),
  path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
]