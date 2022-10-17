from django.db import models
from va.Models.Eeuser import Eeuser
from va.Models.Invoice import Invoice


class Payment(models.Model):

	class Meta:
		db_table = 'payment'
		managed=True

	id = models.AutoField(primary_key=True)
	photo = models.CharField(max_length=300, default='')
	product_code = models.CharField(max_length=300, default='')
	amount = models.IntegerField(default=0)
	name_source = models.CharField(max_length=300, default='')
	bank_from = models.CharField(max_length=300, default='')
	bank_to = models.CharField(max_length=300, default='')
	date_confirmation = models.DateTimeField()
	date_update = models.DateTimeField()
	status = models.IntegerField()
	id_customer = models.CharField(max_length=40)
	eeuser = models.ForeignKey(Eeuser, on_delete=models.PROTECT, db_column='eeuser')
	invoice = models.CharField(max_length=55, default='')
	date_request = models.DateTimeField()
	jml_ttd = models.IntegerField()
	amount_original = models.IntegerField()
	tenant = models.CharField(max_length=6, default='')
	id_invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, db_column='id_invoice')
	topup_type = models.CharField(max_length=15, default='PRE')
	payment_parent = models.IntegerField()
	exp_date = models.DateTimeField()
	va_no = models.CharField(max_length=25, default='')
	trx_id = models.CharField(max_length=70, default='')