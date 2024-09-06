from django.urls import path
from social_network.views.friend_request import *

urlpatterns = [
    path('send-request/', FriendRequestViewSet.as_view({'post': 'sendRequest'})),
    path('accept-request/', FriendRequestViewSet.as_view({'put': 'acceptRequest'})),
    path('reject-request/', FriendRequestViewSet.as_view({'put': 'rejectRequest'})),
    path('accept-request_list/', FriendRequestViewSet.as_view({'get': 'accept_request_list'})),
    path('received_request_list/', FriendRequestViewSet.as_view({'get': 'received_request_list'})),
]

