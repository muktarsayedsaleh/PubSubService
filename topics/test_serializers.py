from rest_framework.test import APITestCase
from .models import Topic
from .serializers import (
    TopicSerializer, SubscriptionSerializer, MessageSerializer
)


class TopicSerializerTest(APITestCase):
    def test_topic_serializer(self):
        topic_data = {'name': 'Test Topic'}
        serializer = TopicSerializer(data=topic_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, topic_data)


class SubscriptionSerializerTest(APITestCase):
    def test_subscription_serializer(self):
        topic = Topic.objects.create(name="Test Topic")
        subscription_data = {
            "topic": topic.id,
            "subscriber": "Test Subscriber",
            "webhook_endpoint": "http://example.com/webhook",
        }
        serializer = SubscriptionSerializer(data=subscription_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["topic"], topic)
        self.assertEqual(serializer.validated_data["subscriber"], "Test Subscriber")
        self.assertEqual(
            serializer.validated_data["webhook_endpoint"], "http://example.com/webhook"
        )


class MessageSerializerTest(APITestCase):
    def test_message_serializer(self):
        topic = Topic.objects.create(name="Test Topic")
        message_data = {"topic": topic.id, "payload": {"key": "value"}}
        serializer = MessageSerializer(data=message_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["topic"], topic)
        self.assertEqual(serializer.validated_data["payload"], {"key": "value"})
