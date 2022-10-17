from django.db import models

from va.Models.Mitra import Mitra
from va.Models.Userdata import Userdata

class Eeuser(models.Model):

	class Meta:
		db_table = 'eeuser'
		managed=True

	id = models.AutoField(primary_key=True)
	nick = models.CharField(max_length=80, default='')
	name = models.CharField(max_length=150, default='')
	deleted = models.BooleanField()
	userdata = models.ForeignKey(Userdata, on_delete=models.PROTECT, db_column='userdata')
	time = models.DateTimeField()
	status = models.CharField(max_length=2, default='')
	pay_type = models.CharField(max_length=2)
	mitra = models.ForeignKey(Mitra, on_delete=models.PROTECT, db_column='mitra')
	admin = models.BooleanField()