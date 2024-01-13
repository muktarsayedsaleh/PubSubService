from rest_framework import serializers
from .models import Topic, Subscription, Message


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ["id", "name"]
    
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "name": instance.name,
        }


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["id", "topic", "subscriber", "webhook_endpoint"]
    
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "topic": instance.topic.name,
            "subscriber": instance.subscriber,
            "webhook_endpoint": instance.webhook_endpoint,
        }


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "topic", "payload"]

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "topic": TopicSerializer(instance.topic).data,
            "payload": instance.payload,
        }
