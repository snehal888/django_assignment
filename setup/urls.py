from django.urls import path
from setup.views import LogInClass

urlpatterns = [
    path('login/', LogInClass.as_view({'post': 'logIn'}))
]