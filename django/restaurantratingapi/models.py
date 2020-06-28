from django.db import models
from django.contrib.auth.models import User

class UserRole(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = 'user_role'

class UserLevel(models.Model):
    level_number = models.PositiveSmallIntegerField(primary_key=True)
    points_level = models.PositiveIntegerField()
    allocated_comfirmation_points = models.PositiveIntegerField()
    created_on = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, db_column='created_by', blank=True, null=True, related_name='user_level_reated_by')
    updated_on = models.DateTimeField()
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, db_column='updated_by', blank=True, null=True, related_name='user_level_updated_by')

    class Meta:
    	managed = True
    	db_table = 'user_level'

class CustomUser(models.Model):
	user = models.OneToOneField(User, models.CASCADE, primary_key=True)
	account_status = models.PositiveSmallIntegerField()
	level_number = models.ForeignKey(UserLevel, on_delete=models.PROTECT, db_column='level_number')
	role_id = models.ForeignKey(UserRole, on_delete=models.PROTECT, db_column='role_id')
	email_code = models.CharField(max_length=255)
	email_verified = models.PositiveSmallIntegerField()	
	birthday = models.DateField()
	gender = models.PositiveSmallIntegerField()
	address = models.CharField(max_length=255)
	phone_number = models.CharField(max_length=50)
	profile_picture = models.ImageField(null=True)
	updated_on = models.DateTimeField()
	updated_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='updated_by', blank=True, null=True, related_name='custom_user_updated_by')

	class Meta:
		managed = True
		db_table = 'custom_user'
