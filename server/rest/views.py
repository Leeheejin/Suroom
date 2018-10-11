from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import User
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response

# Create your views here.

@api_view(['GET', 'POST'])
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except(User.DoesNotExist):
        return (HttpResponse(status=404))

    if (request.method == 'GET'):
        serializer = UserSerializer(user)
        return (JsonResponse(serializer.data))
    
    elif (request.method == 'PUT'):
        data = JSONParser().parse(request)
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return (JsonResponse(serializer.data))
        return (JsonResponse(serializer.errors, status=404))

    elif request.method == 'DELETE':
        user.delete()
        return (HttpResponse(status=204))

@api_view(['POST'])
def user_login(request):
    if (request.method == 'POST'):
        data = JSONParser().parse(request)
        print(data)
        try:
            user = User.objects.filter(auth_id = data['auth_id'])
            if (user[0].auth_pw == data['auth_pw']):
                serializer = UserSerializer(user[0])
                return (Response(data=serializer.data, status=status.HTTP_200_OK))
            else:
                return (Response(status=status.HTTP_404_NOT_FOUND))
        except(User.DoesNotExist):
            return (Response(status=status.HTTP_404_NOT_FOUND))

    else:
        return (Response(status = status.HTTP_400_BAD_REQUEST))