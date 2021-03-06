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

    ## should check with activity diagram
    # GET api/ratings/list?restid=23
    # this gets list of ratings for the restaurant
    # this also gives for the restaurant
    # def get rating list_for_the_restaurant()
    def get_ratings_for_restaurant(self, rest_id):

        ratings = Rating.objects.raw("""
            SELECT rating.rating_id, restaurant_id, dish_id, dish_rating,
            price_rating, service_rating, verified,
            added_dish_rating.user_id as dish_user_id,
            added_rating.user_id as restaurant_user_id
            FROM rating
            LEFT JOIN added_dish_rating
            ON added_dish_rating.rating_id=rating.rating_id
            LEFT JOIN added_rating
            ON added_rating.rating_id = rating.rating_id 
            WHERE restaurant_id=%s""",
            [rest_id])

        list = []

        total_dish_rating = 0
        total_price_rating = 0
        total_service_rating = 0
        total_no_of_ratings = 0
        overall_rating = 0

        avg_dish_rating = 0
        avg_price_rating = 0
        avg_service_rating = 0
        overall_rating = 0

        if not ratings:
            resp = {
                "success": True,
                "code": 200,
                "message": "success GetRating",
                "data": {
                    "restaurant_id": rest_id,
                    "total_no_of_ratings": total_no_of_ratings,
                    "overall_rating": overall_rating,
                    "dish_rating": avg_dish_rating,
                    "price_rating": avg_price_rating,
                    "service_rating": avg_service_rating,
                    "ratings": list
                }
            }
            return resp


        for item in ratings:
            total_no_of_ratings = total_no_of_ratings + 1
            total_dish_rating = total_dish_rating + item.dish_rating
            total_price_rating = total_price_rating + item.price_rating
            total_service_rating = total_service_rating + item.service_rating

            rating_model = {
                "rating_id": item.rating_id,
                "dish_id": item.dish_id,
                "overall_rating": (item.dish_rating + item.price_rating + item.service_rating)/3,
                "dish_rating": item.dish_rating,
                "price_rating": item.price_rating,
                "service_rating": item.service_rating,
                "added_by": item.restaurant_user_id if item.restaurant_user_id != None else item.dish_user_id,
                "verified": item.verified
            }
            list.append(rating_model)

        avg_dish_rating = total_dish_rating/total_no_of_ratings
        avg_price_rating = total_price_rating/total_no_of_ratings
        avg_service_rating = total_service_rating/total_no_of_ratings
        overall_rating = (avg_dish_rating + avg_price_rating + avg_service_rating)/3

        resp = {
            "success": True,
            "code": 200,
            "message": "success GetRating",
            "data": {
                "restaurant_id": rest_id,
                "total_no_of_ratings": total_no_of_ratings,
                "overall_rating": overall_rating,
                "dish_rating": avg_dish_rating,
                "price_rating": avg_price_rating,
                "service_rating": avg_service_rating,
                "ratings": list
            }
        }

        return resp

    def delete_rating(self, data):
        pass;

    ## should check with activity diagram
    # created for restaurant service(not pre planned function)
    # now this seems to be unnecesary and this can be achieved by above function - get_ratings_for_restaurant
    def get_detail_ratings_for_restaurant(self, rest_id):

        added_ratings  = Rating.objects.raw("""
            SELECT rating_id, restaurant_id, dish_rating, price_rating,
            service_rating
            WHERE restaurant_id = %s
            FROM rating
            """, [rest_id])        

        list = []

        dish_rating = 0
        price_rating = 0
        service_rating = 0
        total_no_of_ratings = 0
        overall_rating = 0

        for item in added_ratings:
            # print(item)
            # print(1)
            total_no_of_ratings = total_no_of_ratings + 1
            dish_rating = dish_rating + item.dish_rating
            price_rating = price_rating + item.price_rating
            service_rating = service_rating + item.service_rating

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

        avg_dish_rating = dish_rating/total_no_of_ratings
        avg_price_rating = price_rating/total_no_of_ratings
        avg_service_rating = service_rating/total_no_of_ratings
        avg_overall_rating = (avg_dish_rating + avg_price_rating + avg_service_rating)/3

        resp = {
            "success": True,
            "code": 200,
            "message": "success GetDetailedRatingsForRestaurant",
            "data": {
                "restaurant_id": rest_id,
                "total_no_of_ratings": total_no_of_ratings,
                "overall_rating": avg_overall_rating,
                "dish_rating": avg_dish_rating,
                "price_rating": avg_price_rating,
                "service_rating": avg_service_rating
            }
        }

        return list

        return 'get ratings list for all restaurants(group by rest)(with average ratings)'

    ## should check with activity diagram
    # GET api/ratings/dishes/list?dishid=2
    # this gets list of dish ratings for all restaurants for a specific dish and group them by restid
    # this also gives average ratings
    def get_dish_rating_list_for_all_restaurant_for_the_dish(self, dish_id):

        added_dish_ratings = AddedDishRating.objects.raw("""
            SELECT added_dish_rating.rating_id, restaurant_id,
            dish_rating, price_rating,service_rating,
            COUNT(added_dish_rating.rating_id) as count,
            AVG(dish_rating) as avg_dish,
            AVG(price_rating) as avg_price,
            AVG(service_rating) as avg_service,
            (AVG(dish_rating)+AVG(price_rating)+AVG(service_rating))/3 as avg_total
            FROM added_dish_rating
            INNER JOIN rating
            ON added_dish_rating.rating_id=rating.rating_id
            WHERE dish_id=%s
            GROUP BY restaurant_id
            ORDER BY avg_dish DESC
            """, [dish_id])

        ratings = []

        for rating in added_dish_ratings:
            res = {
                "restaurant_id": rating.restaurant_id,
                "total_no_of_ratings": rating.count,
                "overall_rating": rating.avg_total,
                "dish_rating": rating.avg_dish,
                "price_rating": rating.avg_price,
                "service_rating": rating.avg_service
            }
            ratings.append(res)

        resp = {
            "success": True,
            "code": 200,
            "message": "success GetDishRatings",
            "data": {
                "dish_id": dish_id,
                "ratings": ratings
            }
        }

        return resp

    # GET api/ratings/dishes?restid=22
    # this gives list of dish ratings for the restaurant and group them by dish id
    # this also gives average ratings
    def get_dish_rating_list_for_the_restaurant(self, rest_id):

        added_dish_ratings = Rating.objects.raw("""
            SELECT rating.rating_id, rating.restaurant_id, dish_id, dish_rating
            price_rating, service_rating,
            AVG(dish_rating) as avg_dish_rating,
            AVG(price_rating) as avg_price_rating,
            AVG(service_rating) as avg_service_rating,
            (AVG(dish_rating) + AVG(price_rating) + AVG(service_rating))/3 as avg_overall_rating,
            COUNT(rating.rating_id) as count
            FROM rating
            INNER JOIN added_dish_rating
            ON rating.rating_id = added_dish_rating.rating_id
            WHERE restaurant_id = %s
            GROUP BY dish_id
            """, [rest_id])

        list = []

        for item in added_dish_ratings:
            dish = Dish.objects.get(dish_id=item.dish_id)
            dish_rating = {
                "dish_id": item.dish_id,
                "dish_name": dish.dish_name,
                "no_of_ratings": item.count,
                "overall_rating": item.avg_dish_rating,
                "overall_dish_rating": item.avg_price_rating,
                "overall_price_rating": item.avg_service_rating,
                "overall_service_rating": item.avg_overall_rating
            }
            list.append(dish_rating)

        resp = {
            "success": True,
            "code": 200,
            "message": "success GetDishRatingListForTheRestaurant",
            "data": {
                "restaurant_id": rest_id,
                "dish_ratings": list
            }
        }
        return resp
        return 'get dish rating list for a restaurant'

    # def get_restaurant_rating_list(self, data):
    #     pass

    #  # customer can see ratings for each dish of that restaurant
    # def get_restaurant_dish_ratings(self, data):
    #     pass
    
    # # customer can see list of ratings for for all restaurants
    # def get_all_restaurant_ratings():
    #     pass

    # duplicate of get_dish_rating_list_for_all_restaurant_for_the_dish
    # customer can see list of  dish ratings  for all restaurants for specific dish
    # get_all_restaurant_dish_ratings(dish_id)
    def get_ratings_for_dish(self, dish_id):

        added_dish_ratings = AddedDishRating.objects.raw("""
            SELECT added_dish_rating.rating_id, restaurant_id
            dish_rating, price_rating,service_rating,
            AVG(dish_rating) as avg_dish,
            AVG(price_rating) as avg_price,
            AVG(service_rating) as avg_service,
            (AVG(dish_rating)+AVG(price_rating)+AVG(service_rating))/3 as avg_total
            FROM added_dish_rating INNER JOIN rating
            ON added_dish_rating.rating_id=rating.rating_id
            WHERE dish_id=%s
            GROUP BY restaurant_id
            ORDER BY avg_dish DESC
            """, [dish_id])

        ratings = []

        for rating in added_dish_ratings:
            res = {
                "restaurant_id": rating.restaurant_id,
                "average_dish_rating": rating.avg_dish,
                "average_price_rating": rating.avg_price,
                "average_price_rating": rating.avg_service,
                "average_total_rating": rating.avg_total
            }
            ratings.append(res)

        resp = {
            "success": True,
            "code": 200,
            "message": "success GetDishRatings",
            "data": {
                "dish_id": dish_id,
                "ratings": ratings
            }
        }

        return resp

    ## should check with activity diagram
    # customer can see the ratings for of a restaurant for a specific dish
    def get_ratings_for_restaurant_dish(rest_id, dish_id):

        added_dish_ratings = AddedDishRating.objects.raw("""
            SELECT added_dish_rating.rating_id, dish_rating, price_rating,
            service_rating
            FROM added_dish_rating
            INNER JOIN rating ON added_dish_rating.rating_id=rating.rating_id
            WHERE restaurant_id=%s AND dish_id=%s""",
            [rest_id, dish_id])

        dish_rating = 0
        price_rating = 0
        service_rating = 0
        total_no_of_ratings = 0
        overall_rating = 0

        for rating in added_dish_ratings:
            total_no_of_ratings = total_no_of_ratings + 1
            dish_rating = dish_rating + rating.dish_rating
            price_rating = price_rating + rating.price_rating
            service_rating = service_rating + rating.service_rating

        if(total_no_of_ratings != 0):
            dish_rating = dish_rating / total_no_of_ratings
            price_rating = price_rating / total_no_of_ratings
            service_rating = service_rating / total_no_of_ratings
            overall_rating = (dish_rating + price_rating + service_rating) / 3

        resp = {
            "success": True,
            "code": 200,
            "message": "success GetDishRating",
            "data": {
                "restaurant_id": rest_id,
                "dish_id": dish_id,
                "total_no_of_ratings": total_no_of_ratings,
                "dish_rating": dish_rating,
                "price_rating": price_rating,
                "service_rating": service_rating,
                "overall_rating": overall_rating
            }
        }

        return resp


