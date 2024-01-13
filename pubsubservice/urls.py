from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from topics.views import (
    create_topic, publish_message, subscribe_topic, unsubscribe_topic
)


schema_view = get_schema_view(
    openapi.Info(
        title="PubSub Service APIs",
        default_version="v1",
        description="APIs for PubSub Service",
        contact=openapi.Contact(email="muktar@monjz.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),

    path(
        '<str:topic>/',
        create_topic,
        name='create_topic'
    ),
    path(
        '<str:topic>/publish/',
        publish_message,
        name='publish_message'
    ),
    path(
        '<str:topic>/subscribe/',
        subscribe_topic,
        name='subscribe_topic'
    ),
    path(
        '<str:topic>/unsubscribe/',
        unsubscribe_topic,
        name='unsubscribe_topic'
    ),
]
