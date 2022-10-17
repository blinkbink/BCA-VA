from rest_framework import serializers
from ..Models.Auth import Auth

class AuthSerializer(serializers.ModelSerializer):
	class Meta:
		db_table = 'login'
		model = Auth
		fields = '__all__'