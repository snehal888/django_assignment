from django.urls import path
from social_network.views.user import *

urlpatterns = [
    path('signup/', UserViewSet.as_view({'post': 'addUser'})),
    path('search_user/', UserAPIViewSet.as_view({'get': 'search_user'}))
]