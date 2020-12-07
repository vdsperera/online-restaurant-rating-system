from django.utils.crypto import get_random_string
from .ValidationService import ValidationService
from ..models import Token
from ..models import Restaurant
from ..models import Contribution
from ..models import ContributionType
from django.contrib.auth.models import User
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from django.db import IntegrityError
import string
import random

class SystemService:

    def __init__(self):
    	self.data = []
    	
    @staticmethod
    def generate_restaurant_code():
    	return get_random_string(length=20)

    @staticmethod
    def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def generate_tokens_for_restaurant(self, data):

        restaurant_id = data['restaurant_id']
        username = data['user']
        generate_size = data['generate_size']

        try: 
            restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
        except IntegrityError as e:
            raise APIException("Restaurant is not available in the system")

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist as e:
            raise APIException(f"Username name '{username}' not exists")

        i=0
        token_number_list = []
        while i < generate_size:
            i = i + 1
            token_number = SystemService.id_generator() 
            check_token = Token.objects.filter(token_number=token_number)

            if(check_token.exists()):
                i = i - 1
                continue
            try:
                token = Token(
                    token_number = token_number,
                    restaurant = restaurant,
                    created_on = '2020-11-15',
                    created_by = user
                    )
                token.save()
            except IntegrityError as e:
                raise APIException("Adding token is failed")
            token_number_model = {
              "token_number": token_number
            }
            token_number_list.append(token_number_model)

        resp = {
        "success": True,
        "code": 200,
        "message": "success GenerateTokesForRestaurant",
        "data": {
            "restaurant_id": restaurant_id,
            "generate_size": generate_size,
            "added_by": user.username,
            "tokens": token_number_list,
        }
        }

        return resp   

    def get_tokens_for_restaurant(self, data):
        
        restaurant_id = data['restid'][0]
        try: 
            restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
        except IntegrityError as e:
            raise APIException("Restaurant is not available in the system")

        tokens = Token.objects.filter(restaurant=restaurant)
        print(tokens.exists())
        if(not tokens.exists()):
            raise APIException("Currently no token for this restaurant")

        token_list = []
        for item in tokens:
            token_model = {
            "token_number":item.token_number
            }
            token_list.append(token_model)

        resp = {
            "success": True,
            "code": 200,
            "message": "success GetTokensForRestaurant",
            "data": {
              "restaurant_id": restaurant_id,
              "tokens": token_list
            }
        }
        return resp   