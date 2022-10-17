from rest_framework import serializers
from ..Models.Topup import Topup

class TopupSerializer(serializers.ModelSerializer):
	class Meta:
		# db_table = 'payment'
		model = Topup
		fields = '__all__'