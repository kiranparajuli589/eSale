from .models import Item
from rest_framework import serializers


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'item_code', 'item_name', 'quantity', 'buying_rate', 'selling_rate')

