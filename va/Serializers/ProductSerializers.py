from rest_framework import serializers
from ..Models.Signature import Product

class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		# db_table = 'mitra'
		model = Product
		fields = '__all__'