from rest_framework.exceptions import APIException
from ..models import Rating
from ..models import AddedDishRating
from ..models import AddedRating
from ..models import Dish
from ..models import Restaurant
from ..models import User
from ..models import Token
from ..models import AddedRating
from rest_framework.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist
from .ValidationService import ValidationService
from django.db import IntegrityError
from ..enums.RatingEnums import VerifiedStatus
from ..enums.ContributionEnums import ContributionTypes
from .ValidationService import ValidationService
from .SystemService import SystemService
from django.db.models import Count
from django.db.models import Avg
from django.db import connection

class RatingService:

    def __init__(self):
        self.data = [];

    # POST api/ratings
    def add_rating(self, data):
        # retrieve request data
        try:
            username = data['user']
            token_number = data['token_number']  # token number
            rest_id = data['restaurant_id']  # restaurant id #required
            dish_id = data['dish_id']  # dish id
            dish_rating = data['dish_rating']  # dish rating #required
            price_rating = data['price_rating']  # price rating #required
            service_rating = data['service_rating']  # service rating #required
            review = data['review']  # review #required
        except KeyError as e:
            raise APIException(f"Key {e} not exists in the request")

        # validate request data for null or empty values
        if(not ValidationService.isset(value=rest_id)):
            raise APIException("Restaurant id is empty")

        if(not ValidationService.isset(value=price_rating)):
            raise APIException("Price rating is empty")

        if(not ValidationService.isset(value=service_rating)):
            raise APIException("Service rating is empty")

        if(not ValidationService.isset(value=review)):
            raise APIException("Review is empty")

        # validate request data values for db existance
        if(not isinstance(username, str)):
            raise APIException("Username should be string")

        # dish rating integer validation
        # dish rating range validation
        if(not ValidationService.is_valid_rating(dish_rating)):
            raise APIException("Invalid dish rating")

        # price rating integer validation
        # price rating range validation
        if(not ValidationService.is_valid_rating(price_rating)):
            raise APIException("Invalid price rating")

        # service rating integer valiation
        # service rating range validation
        if(not ValidationService.is_valid_rating(service_rating)):
            raise APIException("Invalid service rating")

        # check user exists
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist as e:
            raise APIException(f"Username name '{username}' not exists")

        # check user logged in

        # validate restaurant id
        # check whether the restaurant id exists
        try:
            restaurant = Restaurant.objects.get(restaurant_id=rest_id)
        except ObjectDoesNotExist as e:
            raise APIException(f"Restaurant id '{rest_id}' not exists")

        # validate dish id(if exists)
        # dish = Dish.objects.get(dish_id=dish_id)

        # if(not dish):
        #     raise APIException(f"Dish id '{dish_id}' not exists")
        if(dish_id != None):
            try:
                dish = Dish.objects.get(dish_id=dish_id)
            except ObjectDoesNotExist as e:
                raise APIException(f"Dish id '{dish_id}' not exists")

        if token_number != None:            
            try:
                token = Token.objects.get(token_number=token_number, restaurant=restaurant)
            except ObjectDoesNotExist as e:
                token = None
                raise APIException(f"Token number '{token_number}' not exists for the restaurant")

            added_rating = AddedRating.objects.filter(token_number=token)
            added_dish_rating = AddedDishRating.objects.filter(token_number=token)
            if((added_rating.exists() == True) or (added_dish_rating.exists() == True)):
                raise APIException(f"Token number '{token_number}' is already used")

        else:
            token = None
        # validate rating categories

        if(token == None):
            verified = VerifiedStatus.Unverified.value
        else:
            # validate token number
            verified = VerifiedStatus.Verified.value

        rating = Rating(
          restaurant = restaurant,  
          dish_rating = dish_rating,
          price_rating = price_rating,
          service_rating = service_rating,
          verified = verified,
          created_on = "2020-06-26")

        try: 
            rating.save()
        except IntegrityError as e:
            raise APIException(e)   

        system_service = SystemService()
        if(dish_id != None):
            added_dish_rating = AddedDishRating(
            rating = rating,
            dish = dish,
            user = user,
            token_number = token)
            try: 
                # pass
                added_dish_rating.save()
                if(verified == VerifiedStatus.Verified.value):
                    system_service.add_contribution_points(ContributionTypes.AddVerifiedDishRating.value, user)
                else:
                    system_service.add_contribution_points(ContributionTypes.AddUnverifiedDishRating.value, user)
            except IntegrityError as e:
                raise APIException(e)
        else:
            added_rating = AddedRating(
                rating = rating,
                user = user,
                token_number = token
                )

            try: 
                added_rating.save()
                if(verified == VerifiedStatus.Verified.value):
                    system_service.add_contribution_points(ContributionTypes.AddVerifiedRestaurantRating.value, user)
                else:
                    system_service.add_contribution_points(ContributionTypes.AddUnverifiedRestaurantRating.value, user)
            except IntegrityError as e:
                raise APIException(e)    

        # add contribution points to the user
        

        # this should be change by using response model
        resp={
            "success": True,
            "code": 200,
            "message": "success AddRating",
            "data": {
                "rated_by": user.username,
                "verified": VerifiedStatus(rating.verified).name,
                "restaurant_id": restaurant.restaurant_id,
                "dish_id": dish.dish_id if dish_id != None else None,
                "dish_rating": rating.dish_rating,
                "price_rating": rating.price_rating,
                "service_rating": rating.service_rating
            }
        }

        return resp

    # POST api/ratings/verify/{rating_id]
    def verify_rating(self, data):
        pass

    ## should check with activity diagram
    # GET api/ratings/list
    # this gets list of ratings for all restaurants and group them by rest_id
    # this also gives average rating for each resturant
    def get_rating_list_for_all_restaurants(self, data):

        added_ratings  = Rating.objects.raw("""
            SELECT rating_id, restaurant_id, dish_rating, price_rating,
            service_rating,
            AVG(dish_rating) as avg_dish,
            AVG(price_rating) as avg_price,
            AVG(service_rating) as avg_service,
            (AVG(dish_rating)+AVG(price_rating)+AVG(service_rating))/3 as avg_total,
            COUNT(restaurant_id) as count
            FROM rating
            GROUP BY restaurant_id
            """)        

        list = []
        for item in added_ratings:
            # print(item)
            # print(1)
            added_rating_model = {
                "restaurant_id": item.restaurant_id,
                # "restaurant_id_dish": item.resd,
                # "restaurant name": "Test",
                "total_no_of_ratings": item.count,
                "overall_rating": item.avg_total,
                "dish_rating": item.avg_price,
                "price_rating": item.avg_price,
                "service_rating": item.avg_dish
            }
            list.append(added_rating_model)

        return list

    def delete_rating(self, data):
        pass;