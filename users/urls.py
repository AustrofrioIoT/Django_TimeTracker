from django.urls import path
from users.views import *
app_name = 'users'

urlpatterns = [
    path('list/', UsuarioList.as_view(), name='list_user'),
    # path('add/', UserCreate.as_view(), name='create_user'),
    # path('<pk>/delete/', UserDelete.as_view(), name='delete_user'),
    # path('<pk>/edit/', UserUpdate.as_view(), name='update_user'),
]
