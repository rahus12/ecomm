from django.shortcuts import render
from .models import CartModel
from .CartSerializer import CartSerializer
from rest_framework.decorators import api_view
from login.models import UserModel
from django.http.response import JsonResponse
from rest_framework import status

# Create your views here.
api_view(['GET'])
def CartView(request, userId):
    try:
        user = UserModel.objects.get(userID=userId)
        print (user.userName)
    except:
        return JsonResponse({"Error":"user not found"}, status = status.HTTP_404_NOT_FOUND)
    

    items = CartModel.objects.filter(userId = userId)
    serializer = CartSerializer(items, many = True)

    return JsonResponse(serializer.data, safe=False, status = status.HTTP_200_OK)

