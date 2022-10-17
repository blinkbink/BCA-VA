import datetime

import requests
import logging
import environ



from ..Helper.Constant import Constant as var
from ..Controller.oAuthController import oAuthController as oAuth
from ..Models.Bank import Bank
from ..Models.Payment import Payment

logger = logging.getLogger(__name__)
# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

def listBill(customerNumber):

	data = oAuth()
	auth = data.oAuthRequest()

	bank = Bank.objects.filter(bank_code = '014').first()
	payment = Payment.objects.filter(va_no=customerNumber)

	if len(payment) < 1:
		return False

	companyCode = bank.company_code

	if bank.session is None:
		data = oAuth()
		auth = data.oAuthRequest()
		token = auth['access_token']
	else:
		token = bank.session

	response = requests.get(env('BCA_API')+env('BCA_VA_PAYMENT')+"CompanyCode="+companyCode+"&"+"CustomerNumber="+customerNumber, headers=data.Header(token=token, relativePath=env('BCA_VA_PAYMENT')+"CompanyCode="+companyCode+"&"+"CustomerNumber="+customerNumber, requestBody=""))
	logger.info("asdddddddddddddddd")
	logger.info(response.text)
	logger.info(response.status_code)
	logger.info(response.json())

	return response

def Balance():

	payload = {
		"CorporateID":"",
		"AccountNumber":""
	}

	return None

def AccountStatement():

	payload = {
		"CorporateID":"",
		"AccountNumber":"",
		"StartDate":"",
		"EndDate":""
	}
	return None

def Transfer():

	payload = {
		"CorporateID":"",
		"SourceAccountNumber":"",
		"TransactionID":"",
		"TransactionDate":"",
		"ReferenceID":"",
		"CurrencyCode":"",
		"Amount":"",
		"BeneficiaryAccountNumber":"",
		"Remark1":"",
		"Remark2":""
	}

	return None

def Bill():

	payload = {
		"CompanyCode": "12345",
		"CustomerNumber": "ABC0012300DEF",
		"RequestID": "201507131507262221400000001975",
		"ChannelType": "6014",
		"TransactionDate": "15/03/2014 22:07:40",
		"AdditionalData": ""
	}

	return None

def Payments():

	payload = {
		"CompanyCode": "12345",
		"CustomerNumber": "ABC0012300DEF",
		"RequestID": "201507131507262221400000001975",
		"ChannelType": "6014",
		"CustomerName": "Customer BCA Virtual Account",
		"CurrencyCode": "IDR",
		"PaidAmount": "150000.00",
		"TotalAmount": "150000.00",
		"SubCompany": "00001",
		"TransactionDate": "15/03/2014 22:07:40",
		"Reference": "1234567890",
		"DetailBills": [],
		"FlagAdvide": "N",
		"Additionaldata": ""
	}

	return None

def validateDate(date_text):
	try:
		datetime.datetime.strptime(date_text, '%d/%m/%Y %H:%M:%S')
		return True
	except ValueError:
		return False