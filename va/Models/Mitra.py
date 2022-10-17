from django.db import models

class Mitra(models.Model):

	class Meta:
		db_table = 'mitra'
		managed=True

	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=150, default='')
	address = models.CharField(max_length=300, default='')
	phone = models.CharField(max_length=15)