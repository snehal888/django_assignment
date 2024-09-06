from django.shortcuts import render
from rest_framework import viewsets, status
from setup.models import FriendRequest   
from social_network.serializers.friend_request import *
from django.http import JsonResponse
from configuration.authentication import JWTAuthenticationUser

class FriendRequestViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthenticationUser]

    def sendRequest(self, request):
        try:
            from_user = request.user  
            one_minute_ago = timezone.now() - timedelta(minutes=1)

            recent_requests_count = FriendRequest.objects.filter(
                from_user=from_user,
                created_at__gte=one_minute_ago
            ).count()

            if recent_requests_count >= 3:
                return JsonResponse({
                    "success": False,
                    "status": status.HTTP_429_TOO_MANY_REQUESTS,
                    "message": "You can send only 3 friend requests in one minute."
                })

            obj = FriendRequest(from_user=from_user)
            serializer = FriendRequestSerializer(obj, data=request.data)
            
            if serializer.is_valid():
                serializer.save()

                return JsonResponse({
                    "success": True,
                    "status": status.HTTP_201_CREATED,
                    "message": "FriendRequest created Successfully",
                    "request_id": obj.id
                })
                
            else:
                errors = serializer.errors
                return JsonResponse({
                    "success": False,
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Invalid data",
                    "errors": errors
                })
        except:
            return JsonResponse({
                "success": False,
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Failed to create FriendRequest"
            })
            
    def acceptRequest(self, request):
        try:
            request_id = request.data.get('request_id') 
            user = FriendRequest.objects.get(id=request_id)
            print(user)
            
            user.status = 'accept'
            user.save() 
            
            return JsonResponse({
                "success": True,
                "status": status.HTTP_201_CREATED,
                "message": "FriendRequest Updated",
                "request_id": user.id
            })
        except:
            return JsonResponse({
                "success": False,
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Failed to Updated FriendRequest"
            })
            
    def rejectRequest(self, request):
        try:
            request_id = request.data.get('request_id') 
            user = FriendRequest.objects.get(id=request_id)
            print(user)
            
            user.status = 'reject'
            user.save() 
            
            return JsonResponse({
                "success": True,
                "status": status.HTTP_201_CREATED,
                "message": "FriendRequest Rejected",
                "request_id": user.id
            })
        except:
            return JsonResponse({
                "success": False,
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Failed to Reject FriendRequest"
            })
        
    def accept_request_list(self, request):
        try:
            user_id = request.GET.get('user_id')
            users = FriendRequest.objects.filter(from_user= user_id,status='accept')
            serializer = AcceptFriendRequestSerializer(users, many=True)
            
            return JsonResponse({
                "success": True,
                "status": status.HTTP_201_CREATED,
                "message": "Accept request list retrieved successfully",
                "data": serializer.data
            })
        except:
            return JsonResponse({
                "success": False,
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Failed to get accepted friend request list"
            })
            
    def received_request_list(self, request):
        try:
            user_id = request.GET.get('user_id')
            users = FriendRequest.objects.filter(from_user= user_id,status='send')
            serializer = ReceivedFriendRequestSerializer(users, many=True)
            
            return JsonResponse({
                "success": True,
                "status": status.HTTP_201_CREATED,
                "message": "Received request list retrieved successfully",
                "data": serializer.data
            })
        except:
            return JsonResponse({
                "success": False,
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Failed to get Received request list"
            })
            
        
              
            