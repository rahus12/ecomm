import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import UserModel
from .userSerializer import UserSerializer

from rest_framework import status

# Create your views here.

@api_view(['POST', 'GET'])
def login_view(request):  

    if request.method == 'POST':        
        try:            
            data = json.loads(request.body)
            userName = data.get('userName')
            password = data.get('password')

            if userName and password:
                user = UserModel(userName=userName)
                user.set_password(password)
                user.save()

                return JsonResponse({"success": "User created successfully"} , status = status.HTTP_201_CREATED)
            else:
                return JsonResponse({"error": "username or password not found"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)

        except():
            return JsonResponse({'error':"username and password are required"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)
    
    elif request.method == 'GET':
        users = UserModel.objects.all()        
        serialzer = UserSerializer(users, many = True)        
        return JsonResponse(serialzer.data, safe=False)





