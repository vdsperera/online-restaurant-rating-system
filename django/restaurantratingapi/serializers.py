from .models import UserRole
from .models import Restaurant
from .models import Rating
from rest_framework import serializers
from django.contrib.auth.models import User
from .serializers import *

class UserRoleSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = UserRole
		fields = ['role_id', 'role_name']

class RestaurantSerializer(serializers.ModelSerializer):
	class Meta:
		model = Restaurant
		fields = ['restaurant_id', 'name', 'address', 'longitude','latitude', 'phone_number', 'code','claimed', 'claimed_by', 'created_by']

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username']

class RatingSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Rating
		fields = ['rating_id', 'dish_rating', 'price_rating', 'service_rating', 'verified', 'created_on', 'updated_on']