from .ValidationService import ValidationService
from .SystemService import SystemService
from ..enums.RestaurantEnums import ClaimStatus, RestaurantComponents
from ..enums.ContributionEnums import ContributionTypes
from ..enums.UserEnums import UserRoles
from ..models import Restaurant
from django.contrib.auth.models import User
from ..models import CustomUser
from..models import EditHistory
from..models import EditComponent
from..models import UserEditHistoryComponent
from..models import UserEditHistoryConfirmation
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from django.db import IntegrityError
from django.core.validators import RegexValidator
import re
from .RatingService import RatingService
from ..models import Rating
from ..models import Dish
from ..models import RestaurantDish
from django.core.exceptions import ObjectDoesNotExist
import string

class RestaurantService:

    def __init__(self):
        self.data = []

    def register_restaurant(self, data):

        # retrieve request data
        try:
            username = data['user']
            rest_name = data['name'] #restaurant name #required
            # rest_address = data['address'] #restaurant address
            rest_street = data['address']['street_address'] + ', '
            rest_city = string.capwords(data['address']['city'])
            print(rest_street+ rest_city)
            rest_pnumber = data['phone_number'] #restaurant phone number
            # rest_added_by = data['user'] #restaurant is added by #required
            # rest_owner = data['owner'] #owner of the restaurant
            rest_longitude = data['longitude'] #restaurant GEO location-longitude #required
            rest_latitude = data['latitude'] #restaurant GEO location-latitude #required
            selected_role = data['role'] #user's requested role for the restaurant
        except KeyError as e:
            print(f"Key {e} not exists in the request")
            raise APIException(f"Key {e} not exists in the request")

        # set default values
        rest_code = SystemService.generate_restaurant_code()
        rest_claimed = ClaimStatus.Unclaimed.value
        rest_owner = None
        rest_address = data['address']['street_address'] + ', ' + data['address']['city']

        # validate request data for null or empty values
        if(not ValidationService.isset(value=rest_name)):
            raise APIException("Restaurant name is empty")

        if(not ValidationService.isset(value=username)):
            raise APIException("User is empty")

        if(not ValidationService.isset(value=rest_city)):
            raise APIException("City is empty")

        if(not ValidationService.isset(value=rest_longitude)):
            raise APIException("Longitude is empty")    

        if(not ValidationService.isset(value=rest_latitude)):
            raise APIException("Latitude is empty")    



        # validate request data values

        if(not isinstance(username, str)):
            raise APIException("Username should be string")

        if(not isinstance(rest_name, str)):
            raise APIException("Restaurant name should be string")            

        if(not isinstance(rest_address, str)):
            raise APIException("Restaurant address should be string")

        if(not isinstance(selected_role, str)):
            raise APIException("Role should be string")     

        try:
            float(rest_longitude)
            rest_longitude = float(data['longitude'])   
        except:
            raise APIException("Longitude should be numeric")

        try:
            float(rest_latitude)
            rest_latitude = float(data['latitude'])   
        except:
            raise APIException("Latitude should be numeric")

        if(not ValidationService.is_geo_coordinate(rest_longitude,'lo')):
            raise APIException("Longitude is invalid")

        if(not ValidationService.is_geo_coordinate(rest_latitude,'la')):
            raise APIException("Latitude is invalid")

        
        # mobile_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
        if(not ValidationService.is_phone_number(rest_pnumber)):
            raise APIException("Phone number is invalid")

        # user = User.objects.get(username='vidumini')   

        #check whether the restaurant name already exists
        if(Restaurant.objects.filter(name=rest_name).exists()):
            raise APIException(f"Restaurant name '{rest_name}' already exists")

        #check whether the username already exists
        if(not User.objects.filter(username=username).exists()):
            raise APIException(f"Username name '{username}' not exists")
        
        user = User.objects.get(username=username)    

        # check whether the user is owner - raw sql should be replaced
        users = User.objects.raw('SELECT * FROM auth_user INNER JOIN auth_user_groups ON auth_user.id=auth_user_groups.user_id WHERE auth_user_groups.group_id=1 AND auth_user.username=%s', [username])

        # print(type(users))
        if(not users):
            print("User is not an owner")
            if(selected_role=='owner'):
                raise APIException(f"User '{username}' currently not a owner")
                pass
                ###Redirect to customer-owner transformation process and end current process###
        else:
            print("User is an owner")
            rest_owner = user
            rest_claimed = ClaimStatus.Pending.value
            ### Need to send generated code ###

        # for u in users:
        #     print(u)

        # create restaurant - need to handle exceptions
        rest = Restaurant(
            name=rest_name,
            address=rest_address,
            longitude=rest_longitude,
            latitude=rest_latitude,            
            phone_number=rest_pnumber,
            claimed=rest_claimed,
            claimed_by=rest_owner,
            code=rest_code,
            created_by=user)      
         
        try: 
            rest.save()
        except IntegrityError as e:
            raise APIException(e)
        
        print(rest_owner.id if rest_owner != None else None)
        # print(type(rest))

        ### Need to add contribution points to the user ###
        # print(ContributionTypes.AddVerifiedDishRating.name)
        if(not users):
            system_service = SystemService()
            system_service.add_contribution_points(ContributionTypes.AddRestaurant.value, user)


        # this should be change by using response model
        resp={
            "success": True,
            "code": 200,
            "message": "success RegisterRestaurant",
            "data": {
                # "restaurant_id": rest.restaurant_id,
                "restaurant_name": rest.name,
                "address": rest.address,
                "logitude": rest.longitude,
                "latitude": rest.latitude,        
                "phone_number": rest.phone_number,
                "added_by": rest.created_by.id,
                "claimed_by": rest_owner.id if rest_owner != None else None,
                "code": rest.code,
                "claimed_status": ClaimStatus(rest.claimed).name,
                "created_on": rest.created_on
            }
        }

        return resp     
        
    def deregister_restaurant():
        pass    
        
    def get_restaurant(self, data):

        rest = Restaurant.objects.get(restaurant_id=data)
        rating_svc = RatingService
        rating_resp = rating_svc.get_ratings_for_restaurant(self, data)
        dishes = Dish.objects.raw("""
            SELECT restaurant_id, dish.dish_id as dish_id,
            dish_name, restaurant_dish.status as status
            FROM dish 
            INNER JOIN restaurant_dish
            ON dish.dish_id=restaurant_dish.dish_id
            WHERE restaurant_id=%s
            """, [data])

        dish_list = []
        for item in dishes:
            dish = {
            "dish_id":item.dish_id,
            "dish_name":item.dish_name,
            "added_status": item.status
            }
            dish_list.append(dish)

        resp={
            "success": True,
            "code": 200,
            "message": "success GetRestaurant",
            "data": {
                "restaurant_id": rest.restaurant_id,
                "restaurant_name": rest.name,
                "dishes": dish_list,
                "address": rest.address,
                "logitude": rest.longitude,
                "latitude": rest.latitude,        
                "phone_number": rest.phone_number,
                "added_by": rest.created_by.username,
                "claimed_by": rest.claimed_by.username if rest.claimed_by != None else None,
                "code": rest.code,
                "claimed_status": ClaimStatus(rest.claimed).name,
                "created_on": rest.created_on,
                "total_no_of_ratings": rating_resp['data']['total_no_of_ratings'],
                "dish_rating": rating_resp['data']['dish_rating'],
                "price_rating": rating_resp['data']['price_rating'],
                "service_rating": rating_resp['data']['service_rating'],
                "overall_rating": rating_resp['data']['overall_rating']
            }
        }

        return resp;

    ## should check with activity diagram
    def get_restaurant_list(self, data):

        restaurant_list = Restaurant.objects.raw("""
            SELECT *
            FROM restaurant
            """)

        list = []
        for rest in restaurant_list:
            rating_svc = RatingService
            rating_resp = rating_svc.get_ratings_for_restaurant(self, rest.restaurant_id)

            restaurant_model = {
                "restaurant_id": rest.restaurant_id,
                "restaurant_name": rest.name,
                "address": rest.address,
                "logitude": rest.longitude,
                "latitude": rest.latitude,        
                "phone_number": rest.phone_number,
                "added_by": rest.created_by.username,
                "claimed_by": rest.claimed_by.username if rest.claimed_by != None else None,
                "code": rest.code,
                "claimed_status": ClaimStatus(rest.claimed).name,
                "created_on": rest.created_on,
                "total_no_of_ratings": rating_resp['data']['total_no_of_ratings'],
                "dish_rating": rating_resp['data']['dish_rating'],
                "price_rating": rating_resp['data']['price_rating'],
                "service_rating": rating_resp['data']['service_rating'],
                "overall_rating": rating_resp['data']['overall_rating']
            }
            list.append(restaurant_model)

        list.sort(key = lambda x: x['overall_rating'], reverse=True)
        resp = {
            "success": True,
            "code": 200,
            "message": "success GetRestaurantList",
            "data": {
                "restaurant_list": list
            }
        }

        return resp
        pass

    # not pre planned
    def get_restaurant_list_for_dish(self, dish_id):

        restaurant_list = Restaurant.objects.raw("""
            SELECT *
            FROM restaurant

            """)

        list = []
        for rest in restaurant_list:
            rating_svc = RatingService
            rating_resp = rating_svc.get_ratings_for_restaurant_dish(rest.restaurant_id, dish_id)
            if rating_resp['data']['total_no_of_ratings'] == 0:
                continue

            restaurant_model = {
                "restaurant_id": rest.restaurant_id,
                "restaurant_name": rest.name,
                "address": rest.address,
                "logitude": rest.longitude,
                "latitude": rest.latitude,        
                "phone_number": rest.phone_number,
                "added_by": rest.created_by.username,
                "claimed_by": rest.claimed_by.username if rest.claimed_by != None else None,
                "code": rest.code,
                "claimed_status": ClaimStatus(rest.claimed).name,
                "created_on": rest.created_on,
                "total_no_of_ratings": rating_resp['data']['total_no_of_ratings'],
                "dish_rating": rating_resp['data']['dish_rating'],
                "price_rating": rating_resp['data']['price_rating'],
                "service_rating": rating_resp['data']['service_rating'],
                "overall_rating": rating_resp['data']['overall_rating']
            }
            list.append(restaurant_model)

        list.sort(key = lambda x: x['overall_rating'], reverse=True)
        resp = {
            "success": True,
            "code": 200,
            "message": "success GetRestaurantList",
            "data": {
                "restaurant_list": list
            }
        }
        return resp

    def add_dishes_for_the_restaurant(self, data):

        # retrieve request data
        req_user = data["user"]
        req_restaurant_id = data["restaurant_id"]
        req_dish_id = data["dish_id"]
        req_dish_name = data["dish_name"]
        new_dish = False
        system_service = SystemService()

        # validate request data for null or empty values
        # 
        # 
        if(not ValidationService.isset(value=req_dish_id)):
            if(not ValidationService.isset(value=req_dish_name)):
                raise APIException("Dish name is empty")
            new_dish = True

        # validate request data types
        # 
        # 

        # set defaults
        # 
        # 
        status = 0
        owner = False

        # validate request data for existance in db
        # 
        # 
        # new to check already exists dish name
        # 
        # 
        try: 
            restaurant = Restaurant.objects.get(restaurant_id=req_restaurant_id)
        except IntegrityError as e:
            raise APIException("Restaurant is not available in the system")

        try:
            user = User.objects.get(username=req_user)
        except ObjectDoesNotExist as e:
            raise APIException(f"Username name '{req_user}' not exists")


        ## check whether user is other restaurant owner, this restaurant owner or customer
        custom_user = CustomUser.objects.get(user_id=user)
        if(custom_user.role_id.role_id == 1):
            owner = True
            claimed_rest = Restaurant.objects.filter(restaurant_id=restaurant.restaurant_id, claimed_by=user)
            if(claimed_rest.exists() == False):
                return 'operation not permited(only allowed for restaurant owner)'


        if(new_dish == False):
            dish = Dish.objects.filter(dish_id=req_dish_id)
            print(dish[0].status)
            if(dish.exists() == True):
                if(dish[0].status == 1):
                    dish = dish
                elif(dish[0].status == 0):
                    raise APIException("Dish is in pending status for the system")
                elif(dish[0].status == 2):
                    raise APIException("Dish is in rejected status for the system")
            else:
                raise APIException("Dish is not available in the system")

            restaurantdish = None
            restaurantdish = RestaurantDish.objects.filter(dish=dish[0].dish_id, restaurant=restaurant) 

            print(restaurantdish)

            if(restaurantdish.exists() == True):
                print(restaurantdish)
                if(restaurantdish[0].status == 1):
                    raise APIException("Dish is already in the restaurant")
                elif(restaurantdish[0].status == 0):
                    raise APIException("Dish is in pending status for this restaurant")
                elif(restaurantdish[0].status == 2):
                    raise APIException("Dish is in rejected status for this restaurant")


            ## check whether dish is rejected one or already requested one
        else:
            req_dish = Dish.objects.filter(dish_name=req_dish_name)
            if(req_dish.exists() == True):
                if(req_dish[0].status == 1):
                    dish = req_dish
                    raise APIException("Dish is in already in the system")
                elif(req_dish[0].status == 0):
                    raise APIException("Dish is in pending status for the system")
                elif(req_dish[0].status == 2):
                    raise APIException("Dish is in rejected status for the system")
                
            else:
                dish = Dish(
                dish_name = req_dish_name,
                status = 1 if owner == True else 0,
                created_by = user,
                created_on = "2020-11-14"
                )
                try: 
                    dish.save()
                except IntegrityError as e:
                    raise APIException(e)

        added_dish = RestaurantDish(
            dish = dish[0],
            restaurant = restaurant,
            added_by = user,
            status = 1 if owner == True else 0,
            created_on = "2020-11-14"
            )

        try: 
            added_dish.save()
            system_service.add_contribution_points(ContributionTypes.AddDishToRestaurant.value, user)
        except IntegrityError as e:
            raise APIException(e)

        resp = {
            "success": True,
            "code": 200,
            "message": "success AddDIshesForRestaurant",
            "data": {
                "restaurant_id": added_dish.dish_id,
                "dish_id": dish[0].dish_id,
                "dish_name": dish[0].dish_name,
                "added_by": added_dish.added_by.username,
                "added_status": added_dish.status
            }
        }
        return resp

    def request_edit(self, data):

        username = 'dilshan'
        restaurant_id = data['restaurant_id']
        component = data['component']
        current_value = data['current_value']
        new_value = data['new_value']
        is_owner = False


        edit_component = EditComponent.objects.filter(component_id = component)

        if(not edit_component.exists()):
            return False

        user = User.objects.filter(username=username)
        custom_user = CustomUser.objects.filter(user_id=user[0].id)
        print(custom_user[0].level_number.allocated_comfirmation_points)

        user_role = custom_user[0].role_id.role_id
        if(user_role == UserRoles.Admin.value):
            is_owner = True
            # return True

        restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id, claimed_by=user[0])
        # print(restaurant)
        if(is_owner == True):
            if(restaurant.exists() == False):
                return False
            else:
                pass
                # return True
                self.set_history(user[0], restaurant[0], edit_component[0], current_value, new_value, status=2)
                self.update_restaurant_component_value(component, restaurant[0], new_value)
                pass
                # allow edit
        else:
            pass
            hasRecentChangesByThisUser = False
            hasRecentChangesByOtherUsers = False
            if(hasRecentChangesByThisUser):#check user has recent changes for the component
                return APIException("has recently edited")
            if(hasRecentChangesByOtherUsers):
                self.set_history(user[0], restaurant[0], edit_component[0], current_value, new_value, status=2)
                update_restaurant_component_value(component, restaurant[0], new_value)
            else:
                pass
                if(restaurant[0].claimed_status == 2):#claimed restaurant
                    self.set_history(user[0], restaurant[0], edit_component[0], current_value, new_value, status=2)
                else:
                    pass
                    self.set_history(user[0], restaurant[0], edit_component[0], current_value, new_value, status=2)

                    update_restaurant_component_value(component, restaurant[0], new_value)



        return restaurant
        #check whether the username already exists
        # if(not User):
        #     raise APIException(f"Username name '{username}' not exists")
        print(custom_user)
        return user

        pass

    def set_history(self, user, restaurant, edit_component, current_value, new_value, status=2):

        edit_history = EditHistory(
            current_value = current_value,
            requested_value = new_value,
            status = status,#approved
            confirmed_by = user
            )
        # edit_history.save()

        user_edit_history_component = UserEditHistoryComponent(
            user = user,
            history = edit_history,
            restaurant = restaurant,
            component = edit_component)
        # user_edit_history_component.save()

        user_edit_history_confirmation = UserEditHistoryConfirmation(
            user = user,
            history = edit_history,
            confirmation_points = edit_component.confirmation_point_level)

    def update_restaurant_component_value(self, component, restaurant, new_value):
        if(component == RestaurantComponents.RestaurantAddress.value):
            restaurant[0].address = new_value
        elif(component == RestaurantComponents.RestaurantEmail.value):
            pass
            # restaurant[0].email = new_value
        elif(component == RestaurantComponents.RestaurantLocation):
            pass
            # restaurant[0].address = new_value
        elif(component == RestaurantComponents.RestaurantName):
            restaurant[0].name = new_value
        elif(component == RestaurantComponents.RestaurantWebsite):
            pass
            # restaurant[0].website = new_value
        elif(component == RestaurantComponents.RestaurantPhoneNumber):
            restaurant[0].phone_number = new_value
            # restaurant[0].save()     
        pass

    def approve_edit():
        pass

    def claim_restaurant():
        pass



