# myapi/urls.pyfrom django.urls import include, path
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'restaurants', views.RestaurantViewSet, basename='RestaurantView')

urlpatterns = [
    path('', include(router.urls)),
    # path('restaurants/', views.RestaurantViewSet.as_view(), name='RestaurantView'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# POST  /api/restaurants
# PATCH /api/restaurants/[id]
# PUT   /api/restaurants/[id]
# GET   /api/restaurants/[id]
# GET   /api/RestaurantViewSet