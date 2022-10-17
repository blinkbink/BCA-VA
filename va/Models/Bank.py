from django.db import models

class Bank(models.Model):

	class Meta:
		db_table = 'bank'
		managed=True

	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=80)
	bank_code = models.CharField(max_length=10)
	rekening = models.CharField(max_length=25)
	aquirer = models.BooleanField()
	company_code = models.CharField(max_length=30)
	api_key = models.CharField(max_length=60)
	api_secret = models.CharField(max_length=60)
	client_id = models.CharField(max_length=60)
	client_secret = models.CharField(max_length=60)
	session = models.CharField(max_length=45)