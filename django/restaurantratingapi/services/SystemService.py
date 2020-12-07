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