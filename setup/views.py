from setup.models import User
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework import status
import csv
import datetime
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
 
class LogInClass(viewsets.ModelViewSet):

    permission_classes = [AllowAny]

    def logIn(self,request):        
        email = request.data.get('email')
        password1 = request.data.get('password')

        try:
            user = User.objects.get(email__iexact=email, password=password1)
        except User.DoesNotExist:
            return JsonResponse({
                "success": False,
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Incorrect Login ID or password"
            })

        token= RefreshToken.for_user(User.objects.get(id=user.id))

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
            "status": status.HTTP_200_OK,                
            "message": "Log-in successfully",
            'token': token_json,
            "data": {
                'user_id' : user.id
            },
            "registration_token":  "create_user.token"  
        })

            