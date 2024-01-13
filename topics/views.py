import requests
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Topic, Subscription
from .serializers import TopicSerializer, SubscriptionSerializer, MessageSerializer


@swagger_auto_schema(
    tags=["Topics"],
    operation_id="create_topic",
    operation_description="Create a new topic",
    responses={
        201: TopicSerializer(),
        400: "Bad Request",
    },
    manual_parameters=[
        openapi.Parameter(
            name="topic",
            in_=openapi.IN_PATH,
            type=openapi.TYPE_STRING,
            required=True,
            description="Topic name",
        ),
    ],
    methods=["POST"],
)
@api_view(["POST"])
def create_topic(request, topic):
    serializer = TopicSerializer(data={"name": topic})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    tags=["Topics"],
    operation_id="publish_message",
    operation_description="Publish a message to a topic",
    responses={
        201: MessageSerializer(),
        400: "Bad Request",
        404: "Not Found",
    },
    manual_parameters=[
        openapi.Parameter(
            name="topic",
            in_=openapi.IN_PATH,
            type=openapi.TYPE_STRING,
            required=True,
            description="Topic name",
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "payload": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Message payload",
            ),
        },
        required=["message"],
    ),
    methods=["POST"],
)
@api_view(["POST"])
def publish_message(request, topic):
    try:
        topic_obj = Topic.objects.get(name=topic)
    except Topic.DoesNotExist:
        return Response(
            {"error": f"Topic {topic} not found"}, status=status.HTTP_404_NOT_FOUND
        )

    data = {"topic": topic_obj.id, "payload": request.data.get("payload")}
    serializer = MessageSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        # Send message to subscribers
        # TODO: This should be done asynchronously via queues to scale well.
        #       For the sake of simplicity, we'll do it synchronously for now.
        print("Sending message to subscribers...")
        for subscription in Subscription.objects.filter(topic=topic_obj):
            try:
                response = requests.post(
                    subscription.webhook_endpoint,
                    json=request.data.get("payload")
                )
                print(response.status_code)
                print(response.json())
            except requests.exceptions.RequestException as e:
                print(e)
                # TODO: Log this error somewhere & store the message in a dead-letter queue for retrying later.
                continue

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    tags=["Topics"],
    operation_id="subscribe_topic",
    operation_description="Subscribe to a topic",
    responses={
        201: SubscriptionSerializer(),
        400: "Bad Request",
        404: "Not Found",
    },
    manual_parameters=[
        openapi.Parameter(
            name="topic",
            in_=openapi.IN_PATH,
            type=openapi.TYPE_STRING,
            required=True,
            description="Topic name",
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "subscriber": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Subscriber name",
            ),
            "webhook_endpoint": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Webhook endpoint, should be a valid URL",
            ),
        },
        required=["subscriber", "webhook_endpoint"],
    ),
    methods=["POST"],
)
@api_view(["POST"])
def subscribe_topic(request, topic):
    try:
        topic_obj = Topic.objects.get(name=topic)
    except Topic.DoesNotExist:
        return Response(
            {"error": f"Topic {topic} not found"}, status=status.HTTP_404_NOT_FOUND
        )

    data = {
        "topic": topic_obj.id,
        "subscriber": request.data.get("subscriber"),
        "webhook_endpoint": request.data.get("webhook_endpoint"),
    }
    serializer = SubscriptionSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    tags=["Topics"],
    operation_id="unsubscribe_topic",
    operation_description="Unsubscribe from a topic",
    responses={
        200: "OK",
        404: "Not Found",
    },
    manual_parameters=[
        openapi.Parameter(
            name="topic",
            in_=openapi.IN_PATH,
            type=openapi.TYPE_STRING,
            required=True,
            description="Topic name",
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "subscriber": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Subscriber name",
            ),
        },
        required=["subscriber"],
    ),
    methods=["POST"],
)
@api_view(["POST"])
def unsubscribe_topic(request, topic):
    try:
        topic_obj = Topic.objects.get(name=topic)
    except Topic.DoesNotExist:
        return Response(
            {"error": f"Topic {topic} not found"}, status=status.HTTP_404_NOT_FOUND
        )

    subscriber = request.data.get("subscriber")
    try:
        subscription = Subscription.objects.get(topic=topic_obj, subscriber=subscriber)
    except Subscription.DoesNotExist:
        return Response(
            {
                "error": f"Subscription not found for subscriber {subscriber} on topic {topic}"  # noqa
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    subscription.delete()
    return Response(
        {"success": f"Successfully unsubscribed {subscriber} from {topic}"},
        status=status.HTTP_200_OK,
    )
