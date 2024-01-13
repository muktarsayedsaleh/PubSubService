from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Topic, Subscription


class TopicsAPITest(APITestCase):
    def setUp(self):
        # Create test data
        self.topic_name = "test_topic"
        self.topic = Topic.objects.create(name=self.topic_name)

    def test_create_topic(self):
        url = reverse("create_topic", args=[self.topic_name + "2"])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], self.topic_name + "2")

    def test_publish_message(self):
        url = reverse("publish_message", args=[self.topic_name])
        payload = {"payload": {"key": "value"}}
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["topic"],
            {
                "id": self.topic.id,
                "name": self.topic.name,
            },
        )
        self.assertEqual(response.data["payload"], payload["payload"])

    def test_subscribe_topic(self):
        url = reverse("subscribe_topic", args=[self.topic_name])
        data = {
            "subscriber": "test_subscriber",
            "webhook_endpoint": "http://example.com",
        }
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["topic"],
            self.topic_name,
        )
        self.assertEqual(response.data["subscriber"], data["subscriber"])
        self.assertEqual(response.data["webhook_endpoint"], data["webhook_endpoint"])

    def test_unsubscribe_topic(self):
        subscription = Subscription.objects.create(
            topic=self.topic,
            subscriber="test_subscriber",
            webhook_endpoint="http://example.com",
        )
        url = reverse("unsubscribe_topic", args=[self.topic_name])
        data = {"subscriber": "test_subscriber"}
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Subscription.objects.filter(pk=subscription.pk).exists())
