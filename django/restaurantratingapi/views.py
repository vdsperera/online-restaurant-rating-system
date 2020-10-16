from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .services.RestaurantService import RestaurantService

class UserRoleViewSet(viewsets.ModelViewSet):
	queryset = UserRole.objects.all().order_by('role_name')
	serializer_class = UserRoleSerializer

class RestaurantViewSet(viewsets.ViewSet):
	
	def create(self, request):
		data = request.data['data']['mdata']
		restservice = RestaurantService()
		response = restservice.register_restaurant(data)
		return Response(response)
