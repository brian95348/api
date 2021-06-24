
from django.urls import path, re_path, include
from .views import (ServicesCreate, ServicesList, ServicesRetrieveUpdateDestroy,
                     MessageListCreate)
from comments.views import CommentCreate

#app_name = 'serviceproviders'
urlpatterns = [
    path('', ServicesList.as_view(), name='api-services-list'),
    path('create/', ServicesCreate.as_view(), name='api-service-create'),
    re_path(r'^(?P<slug>[\w-]+)/$', ServicesRetrieveUpdateDestroy.as_view(), name='api-service-detail'),
    re_path(r'^(?P<slug>[\w-]+)/comment$', CommentCreate.as_view(), name='api-comment-create'),
    re_path(r'^(?P<slug>[\w-]+)/chat$', MessageListCreate.as_view(), name='api-service-chat'),
    path('auth/',include('rest_framework.urls')),
]

"""path('search/', ServiceSearchListView.as_view(),name='services-search'),
    re_path(r'^(?P<slug>[\w-]+)/$', ServicesDetailAPIView.as_view(), name='service-detail'),
    re_path(r'^(?P<slug>[\w-]+)/comment$', CommentCreateAPIView.as_view(), name='comment-create'),
    re_path(r'^(?P<slug>[\w-]+)/edit$', ServiceUpdateView.as_view(), name='service-update'),
    re_path(r'^(?P<slug>[\w-]+)/delete$', ServiceDeleteView.as_view(), name='service-delete'), """
