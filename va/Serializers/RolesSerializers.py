from rest_framework import serializers
from ..Models.Roles import Roles

class RolesSerializer(serializers.ModelSerializer):
	class Meta:
		db_table = 'roles'
		model = Roles
		fields = '__all__'