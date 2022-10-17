from django.db import models

from va.Models.Mitra import Mitra

class Userdata(models.Model):

	class Meta:
		db_table = 'userdata'
		managed=True

	id = models.AutoField(primary_key=True)
	no_identitas = models.CharField(max_length=300, default='')
	nama = models.CharField(max_length=300, default='')
	jk = models.CharField(max_length=15)
	tempat_lahir = models.CharField(max_length=300, default='')
	tgl_lahir = models.CharField(max_length=300, default='')
	no_handphone = models.CharField(max_length=300, default='')
	mitra = models.ForeignKey(Mitra, on_delete=models.PROTECT, db_column='mitra')