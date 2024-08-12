from rest_framework import serializers
from .models import itemModel

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = itemModel
        fields = "__all__"