from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .services.RestaurantService import RestaurantService

class UserRoleViewSet(viewsets.ModelViewSet):
	queryset = UserRole.objects.all().order_by('role_name')
	serializer_class = UserRoleSerializer

class RestaurantViewSet(viewsets.ViewSet):

    queryset = Restaurant.objects.all().order_by('restaurant_id')
    serializer_class = RestaurantSerializer		
	def create(self, request):
		data = request.data['data']['mdata']
		restservice = RestaurantService()
		response = restservice.register_restaurant(data)
		return Response(response)

class RatingViewSet(viewsets.ViewSet):

    serializer_class = RestaurantSerializer

    def create(self, request):
        data = request.data['data']['mdata']
        rating_service = RatingService()
        qry = rating_service.add_rating(data)
        return Response(qry)
