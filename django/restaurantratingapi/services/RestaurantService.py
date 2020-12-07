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
        
    def get_restaurant():
        pass

    def get_restaurant_list():
        pass

    def request_edit():
        pass

    def approve_edit():
        pass

    def claim_restaurant():
        pass



