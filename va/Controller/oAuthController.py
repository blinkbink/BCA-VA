import base64
import datetime
import logging
import requests
import os

from coreva.settings import BASE_DIR
from ..Helper.Constant import Constant as var
from ..Models.Bank import Bank
from ..Models.Signature import Signature as signModel
from ..Utils.Signature import createSignature

logger = logging.getLogger(__name__)

class oAuthController:

	def __init__(self):

		try:
			bank = Bank.objects.filter(bank_code='014').first()

			self.api_key = bank.api_key
			self.api_secret = bank.api_secret
			self.client_id  = bank.client_id
			self.client_secret = bank.client_secret

		except Exception as e:
			logger.error(e)

	def Header(self, token, relativePath, requestBody):

		timestamps = str(datetime.datetime.now().isoformat())

		sign=signModel()
		sign.method = 'POST'
		sign.requestBody = requestBody
		sign.relativePath = relativePath
		sign.timestamps = timestamps
		sign.accessToken = token

		theSignature = createSignature(self.api_secret, sign.dataSignature())

		headers = {
			'Authorization':'Bearer '+token,
			'Content-Type':'application/json',
			'Origin':'https://api.digisign.id',
			'X-BCA-Key':self.api_secret,
			'X-BCA-Timestamp':timestamps,
			'X-BCA-Signature':theSignature
		}

		logger.info("HEADER : "+ str(headers))

		return headers

	def oAuthRequest(self):
		logger.info("Request Access token")

		url = var.BCA_API+var.BCA_ACCESS_TOKEN

		logger.info("URL : " + url)

		Authorize = str(self.client_id)+":"+str(self.client_secret)

		Authorize = base64.b64encode(Authorize.encode('ascii')).decode("utf-8")
		logger.info(Authorize)
		payload = "grant_type=client_credentials"
		headers = {
			'Content-Type': 'application/x-www-form-urlencoded',
			'Authorization': 'Basic ' + Authorize
		}

		response = requests.request("POST", url, headers=headers, data=payload)
		logger.info("RESPONSE : " + str(response.json()))
		token = response.json()['access_token']

		bank =	Bank.objects.filter(bank_code='014')
		bank.update(session=token)

		return response.json()