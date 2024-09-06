from django.shortcuts import render
from rest_framework import viewsets, status
from setup.models import User   
from social_network.serializers.user import *
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
import datetime
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from configuration.authentication import JWTAuthenticationUser
from django.db.models import Q
from django.core.paginator import Paginator


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    def addUser(self, request):
        try:
            obj = User()
            serializer = UserSerializer(obj, data= request.data)
            
            if serializer.is_valid():
                serializer.save()

                token= RefreshToken.for_user(User.objects.get(id=obj.id))
            
                token_json = {'access' :{} , 'refresh' : {}}
                token_json['access']['token'] = str(token.access_token) 
                token_json['refresh']['token'] = str(token)
                
                decoded_token = RefreshToken(str(token)).payload
                expiry_time = decoded_token["exp"]
                token_json['refresh']['expiry'] = str(datetime.datetime.fromtimestamp(expiry_time))
                
                decoded_token = AccessToken(str(token.access_token)).payload
                expiry_time = decoded_token["exp"]
                token_json['access']['expiry'] = str(datetime.datetime.fromtimestamp(expiry_time))

                return JsonResponse({
                    "success": True,
                    "status": status.HTTP_201_CREATED,
                    "message": "User created Successfully",
                    "user_id": obj.id,
                    "token": token_json
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
                "message": "Failed to create user"
            })
            
class UserAPIViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthenticationUser]
    
    def search_user(self, request):
        try:
            keyword = request.GET.get('keyword')
            page_number = request.GET.get('page', 1)  
            page_size = 10  

            # Step 1: Check if the keyword matches an exact email
            try:
                user = User.objects.get(email=keyword)
                serializer = GetUserByMailSerializer(user)
                return JsonResponse({
                    "success": True,
                    "status": status.HTTP_200_OK,
                    "message": "User found by exact email match",
                    "data": [serializer.data]
                })
            except User.DoesNotExist:
                # Step 2: If no exact email match, search by name or email part
                users = User.objects.filter(Q(name__icontains=keyword) | Q(email__icontains=keyword))
                
                if not users.exists():
                    return JsonResponse({
                        "success": False,
                        "status": status.HTTP_404_NOT_FOUND,
                        "message": "No users found matching the search keyword"
                    })

                # Step 3: Paginate the results
                paginator = Paginator(users, page_size)
                page_obj = paginator.get_page(page_number)
                serializer = GetUserByMailSerializer(page_obj, many=True)

                return JsonResponse({
                    "success": True,
                    "status": status.HTTP_200_OK,
                    "message": "Users found matching the search keyword",
                    "data": serializer.data,
                    "page": page_number,
                    "total_pages": paginator.num_pages,
                    "total_results": paginator.count
                })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Failed to retrieve users",
                "errors": str(e)
            })
    
