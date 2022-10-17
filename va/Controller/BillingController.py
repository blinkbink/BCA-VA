import json
import traceback
import urllib3
import traceback

import urllib3
import environ


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests
import logging

logger = logging.getLogger(__name__)
# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

def updateTopup (invoice):

	url = env('DIGISIGN_DASHBOARD_API') + env('DIGISIGN_DASHBOARD_UPDATE_TOPUP')

	payload = json.dumps({
		"invoice": invoice
	})

	headers = {
		'token': 'd3e3e4baf71fa1952a4fb0f8e8614f106fc4d8bb',
		'Content-Type': 'application/json'
	}

	try:
		response = requests.request("PATCH", url, headers=headers, data=payload)
		logger.info(response.text)

		return response.json()
	except Exception as e:
		logger.error(traceback.print_exc())
		return False


def billingTopup(external_key, amount, tenant):

	url = env('BILLING_API')+env('BILLING_TOPUP')
	logger.info("URL : " + url)

	if tenant == '1':
		tenant = 'personal'
	if tenant == '2':
		tenant = 'document'
	if tenant == '4':
		tenant = 'sms'
	if tenant == '5':
		tenant = 'verifikasi'
	if tenant == '6':
		tenant = 'seal'
	if tenant == '7':
		tenant = 'verify_text'
	if tenant == '8':
		tenant = 'verify_selfie'


	try:
		payload = {}
		jsonFile = {}
		jsonFile["externalkey"] = external_key
		jsonFile["amount"] = amount
		jsonFile["tenant"] = tenant
		payload["JSONFile"] = jsonFile
		logger.info("Request billing payload : " + str(payload))

		files = {"jsonfield":(None, str(payload).encode("utf-8"), "application/json")}
		data = {'jsonfield': str(payload).encode("utf-8")}

		response = requests.post(url, files = files, verify=False)
		logger.info(response.text)

		return response.json()
	except Exception as e:
		logger.error(traceback.print_exc())
		return False