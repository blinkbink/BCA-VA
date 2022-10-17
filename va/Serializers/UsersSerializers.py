from rest_framework import serializers
from ..Models.Payment import Users

class UsersSerializer(serializers.ModelSerializer):
	class Meta:
		db_table = 'users'
		model = Users
		fields = '__all__'