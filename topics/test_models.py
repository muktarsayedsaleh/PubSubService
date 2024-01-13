from django.test import TestCase
from .models import Topic, Subscription, Message


class ModelTests(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Test Topic")
        self.subscription = Subscription.objects.create(
            topic=self.topic,
            subscriber="Subscriber 1",
            webhook_endpoint="https://postman-echo.com/post",
        )
        self.subscription2 = Subscription.objects.create(
            topic=self.topic,
            subscriber="Subscriber 2",
            webhook_endpoint="https://postman-echo.com/post",
        )
        self.message = Message.objects.create(
            topic=self.topic, payload={"key": "value"}
        )

    def test_topic_creation(self):
        topic = Topic.objects.get(name="Test Topic")
        self.assertEqual(topic.name, "Test Topic")

    def test_subscription_creation(self):
        subscription = Subscription.objects.get(
            topic=self.topic, subscriber="Subscriber 1"
        )
        subscription2 = Subscription.objects.get(
            topic=self.topic, subscriber="Subscriber 2"
        )
        self.assertEqual(subscription.webhook_endpoint, "https://postman-echo.com/post")
        self.assertEqual(subscription2.webhook_endpoint, "https://postman-echo.com/post")

    def test_message_creation(self):
        message = Message.objects.get(topic=self.topic, payload={"key": "value"})
        self.assertEqual(message.payload, {"key": "value"})

    def test_topic_unique_constraint(self):
        with self.assertRaises(Exception):
            Topic.objects.create(name="Test Topic")

    def test_subscriber_unique_constraint(self):
        with self.assertRaises(Exception):
            Subscription.objects.create(
                topic=self.topic,
                subscriber="Subscriber 1",
                webhook_endpoint="https://postman-echo.com/post",
            )

    def test_subscription_relationships(self):
        subscription = Subscription.objects.get(
            topic=self.topic, subscriber="Subscriber 1"
        )
        self.assertEqual(subscription.topic, self.topic)
        self.assertEqual(subscription.subscriber, "Subscriber 1")

    def test_message_relationships(self):
        message = Message.objects.get(topic=self.topic, payload={"key": "value"})
        self.assertEqual(message.topic, self.topic)
