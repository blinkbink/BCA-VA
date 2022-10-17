from rest_framework import serializers
from ..Models.Session import Session

class SessionSerializer(serializers.ModelSerializer):
	class Meta:
		db_table = 'login_session'
		model = Session
		fields = '__all__'