from django.shortcuts import render, redirect
from .models import CartModel
from .CartSerializer import CartSerializer
from rest_framework.decorators import api_view
from login.models import UserModel
from django.http.response import JsonResponse
from rest_framework import status
import jwt

# Create your views here.
api_view(['GET'])
def CartView(request):
    token = request.COOKIES.get('jwt')
    if not token:
        # return redirect("login/")  # wont work with my setup yet
        return JsonResponse({"error":"not authenticated, token not found"}, status = status.HTTP_404_NOT_FOUND)
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        payload_userid = payload.get('id')
        print(payload)        
        user = UserModel.objects.get(userID=payload_userid)
        # print (user)
    except:
        return JsonResponse({"Error":"user not found"}, status = status.HTTP_404_NOT_FOUND)
    
    

    items = CartModel.objects.filter(userId = payload_userid)
    serializer = CartSerializer(items, many = True)

    return JsonResponse(serializer.data, safe=False, status = status.HTTP_200_OK)

