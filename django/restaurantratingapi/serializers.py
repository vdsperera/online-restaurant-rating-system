from .models import Restaurant
from rest_framework import serializers

class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Restaurant
		fields = ('restaurant_id', 'name', 'address', 'longitude','latitude', 'phone_number', 'claimed', 'claimed_by', 'code', 'created_by')