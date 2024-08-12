from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from .models import itemModel
from django.http.response import JsonResponse
import json
from .serializer import ItemSerializer

# Create your views here.
@api_view(['GET','PUT', 'DELETE'])
def get_item_view(request, id):
    
    try:
        item = itemModel.objects.get(itemId = id)
    except:
        return JsonResponse(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        
        item = itemModel.objects.get(itemId = id)
        return JsonResponse(data = {
            "name": item.name,
            "description": item.description,
            "price" : item.price
        }, status = status.HTTP_200_OK)
    
        
    elif request.method == 'PUT':
        serializer = ItemSerializer(item, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = status.HTTP_200_OK)
        else:
            return JsonResponse(status = status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        item.delete()
        return JsonResponse(status = status.HTTP_200_OK)



@api_view(['POST'])
def create_item_view(request):    
    serializer = ItemSerializer(data = request.data)    
    if serializer.is_valid():
        serializer.save()        
        return JsonResponse(serializer.data, status = status.HTTP_201_CREATED)
    else:
        return JsonResponse(status = status.HTTP_400_BAD_REQUEST)
    