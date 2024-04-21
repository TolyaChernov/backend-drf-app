from rest_framework import serializers

from .models import Collection, Link


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = "__all__"
        # fields = ["id", "title", "description", "created_at", "updated_at"]


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = [
            "id",
            "title",
            "description",
            "url",
            "image",
            "link_type",
            "created_at",
            "updated_at",
            "collections",
            "user",
        ]
