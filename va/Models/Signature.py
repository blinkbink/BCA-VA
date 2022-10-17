import hashlib

from django.db import models

class Signature(models.Model):
	_method = models.CharField(max_length=7)
	_requestBody = models.CharField(max_length=400)
	_relativePath = models.CharField(max_length=150)
	_timestamps = models.DateTimeField()
	_accessToken = models.CharField(max_length=150)

	@property
	def method(self):
		if self._method:
			return self._method

	@method.setter
	def method(self, value):
		self._method = value

	@property
	def requestBody(self):
		if self._requestBody:
			return self._requestBody

	@requestBody.setter
	def requestBody(self, value):
		self._requestBody = value

	@property
	def relativePath(self):
		if self._relativePath:
			return self._relativePath

	@relativePath.setter
	def relativePath(self, value):
		self._relativePath = value

	@property
	def timestamps(self):
		if self._timestamps:
			return self._timestamps

	@timestamps.setter
	def timestamps(self, value):
		self._timestamps = value

	@property
	def accessToken(self):
		if self._accessToken:
			return self._accessToken

	@accessToken.setter
	def accessToken(self, value):
		self._accessToken = value

	def dataSignature(self):
		signData = hashlib.sha256(self._requestBody.encode('utf-8')).hexdigest().lower()
		return  self._method+":"+self._relativePath+":"+self.accessToken+":"+signData+":"+self._timestamps

