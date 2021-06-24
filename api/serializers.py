from services.models import Message, ServiceProvider, ServiceProviderImage
from comments.models import Comment
from rest_framework.serializers import ModelSerializer

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        exclude = ['user','sender','is_service_owner','group']
        extra_kwargs = {
            'receiver':{'read_only':True}
        }

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['user','serviceprovider']

class ServiceProviderSerializer(ModelSerializer):
    class Meta:
        model = ServiceProvider
        exclude = ['user','slug']
        extra_kwargs = {
            'rating':{'read_only':True},
            'jobs_completed':{'read_only':True},
            'number_of_clients':{'read_only':True},
        }
