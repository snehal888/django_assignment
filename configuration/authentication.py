from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from setup.models import User

class JWTAuthenticationUser(JWTAuthentication):
    
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization', '')
        try:
            request_user_id = request.GET.get('user_id')
        except:
            pass

        if not auth_header.startswith('Bearer'):
            raise exceptions.AuthenticationFailed('Invalid authentication header')

        token = auth_header.split(' ')[1].strip()
        try:
            decoded_token = AccessToken(str(token)).payload

            user_id = decoded_token.get('user_id')
            if str(user_id) == str(request_user_id):
                user = User.objects.get(id=user_id)
                return user, decoded_token
        except TokenError as e:
            raise exceptions.AuthenticationFailed('Token is invalid or expired')
        
        