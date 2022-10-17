from django.db import models

from va.Models.Eeuser import Eeuser

class Invoice(models.Model):

	class Meta:
		db_table = 'invoice'
		managed=True

	id_invoice = models.AutoField(primary_key=True)
	datetime = models.DateTimeField()
	amount = models.IntegerField()
	eeuser = models.ForeignKey(Eeuser, on_delete=models.PROTECT, db_column='eeuser')
	external_key = models.CharField(max_length=50)
	tenant = models.CharField(max_length=3)
	trx = models.CharField(max_length=2)
	kb_invoice = models.CharField(max_length=55)
	cur_balance = models.BigIntegerField()