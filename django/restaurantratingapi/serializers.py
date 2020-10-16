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