import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import UserModel
from .userSerializer import UserSerializer
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status

import jwt
import datetime

# auth imports
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
# from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create your views here.

def gen_token(user):
    payload = {
        "id": user.userID,
        "exp": datetime.datetime.now() + datetime.timedelta(days=3),
        "iat": datetime.datetime.now()
    }

    token = jwt.encode(payload, 'secret')
    return token

@api_view(['POST', 'GET'])
def signup_view(request):  

    if request.method == 'POST':        
        try:            
            data = json.loads(request.body)
            userName = data.get('userName')
            password = data.get('password')

            if userName and password:
                user = UserModel(userName=userName)
                user.set_password(password)
                user.save()

                # token = Token.objects.create(user = user)
                token = gen_token(user)

                response = JsonResponse({"token": token})
    
                response.set_cookie(
                    key='jwt', 
                    value=token, 
                    httponly=True,  # Helps prevent XSS attacks
                )
                return response


            else:
                return JsonResponse({"error": "username or password not found"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)

        except():
            return JsonResponse({'error':"username and password are required"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)
    
    elif request.method == 'GET':
        users = UserModel.objects.all()        
        serialzer = UserSerializer(users, many = True)        
        return JsonResponse(serialzer.data, safe=False)


@api_view(['POST'])
def login_view(request):

    userName = request.data["userName"]
    password = request.data["password"]

    user = UserModel.objects.get(userName = userName)

    if user is None or not user.verify_password(password):
        return JsonResponse({"error": "username or password incorrect"}, status = status.HTTP_401_UNAUTHORIZED)      

    token = gen_token(user)

    response = JsonResponse({"token": token})
    
    response.set_cookie(
        key='jwt', 
        value=token, 
        httponly=True,  # Helps prevent XSS attacks   
    )
    return response


@csrf_exempt
@api_view(['PUT'])
def forgot_password(request, id):
    try:
        user = UserModel.objects.get(userID=id)
        user.set_password(request.data.get('new_password'))
        user.save()
        return JsonResponse({"success": "Password changed successfully"})
    except UserModel.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



