from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .services.RestaurantService import RestaurantService

class RestaurantViewSet(viewsets.ViewSet):
	
	def create(self, request):
		data = request.data['data']['mdata']
		restservice = RestaurantService()
		response = restservice.register_restaurant(data)
		return Response(response)
