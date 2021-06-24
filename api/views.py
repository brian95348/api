from django.shortcuts import render
from rest_framework.decorators import api_view
from services.models import ServiceProvider, Message
from comments.models import Comment
from .serializers import ServiceProviderSerializer, MessageSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

class IsServiceOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class ServicesList(generics.ListAPIView):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer

class ServicesCreate(generics.CreateAPIView):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class ServicesRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer
    permission_classes = [IsServiceOwnerOrReadOnly]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def perform_update(self,serializer):
        serializer.save(user=self.request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class CommentCreate(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self,serializer):
        serviceprovider = ServiceProvider.objects.get(slug=self.kwargs['slug'])
        serializer.save(user=self.request.user,serviceprovider=serviceprovider)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class MessageListCreate(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        sp_user = ServiceProvider.objects.get(slug=self.kwargs['slug']).user
        lookups = Q(user=self.request.user,receiver=self.kwargs['slug'])\
             | Q(receiver=self.request.user.username,user=sp_user) 
        return Message.objects.filter(lookups)

@method_decorator(csrf_exempt, name='dispatch')            
class UserSignUp(APIView):
       
    def post(self,request):
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']
        User.objects.create_user(username,email,password)
        return Response(status=status.HTTP_201_CREATED)


""" @api_view(['GET','POST'])
def service_provider_non_pk(request):
    if request.method == 'GET':
        qs = ServiceProvider.objects.all()
        serializer = ServiceProviderSerializer(qs,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        serializer = ServiceProviderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT','DELETE','GET'])
def service_provider_pk(request,slug):
    obj = get_object_or_404(ServiceProvider,slug=slug)

    if request.method == 'GET':
        serializer = ServiceProviderSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = ServiceProviderSerializer(obj,data=request.data)
        if serializer.is_valid:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) """



