import datetime
import traceback
from decimal import Decimal

from rest_framework.decorators import api_view

import json
import logging

from ..Controller.BankingController import validateDate, listBill
from django.http.response import JsonResponse, HttpResponse
from rest_framework import status, permissions
from django.contrib.auth.decorators import login_required
from ..Models.Bank import Bank
from ..Models.Eeuser import Eeuser
from ..Models.Invoice import Invoice
from ..Models.Mitra import Mitra
from ..Models.Payment import Payment
from ..Controller.BillingController import billingTopup, updateTopup
from ..Controller.UsersController import get_client_ip
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope, OAuth2Authentication

logger = logging.getLogger(__name__)

class VAView():

	@api_view(['POST'])
	def Bill(request):
		authentication_classes = [OAuth2Authentication]
		permission_classes = [TokenHasScope]
		logger.info(request.data)
		payload = json.dumps(request.data)
		payload = json.loads(payload)
		logger.info('Bill modul')
		logger.info('Client IP : ' + get_client_ip(request))
		logger.info('REQUEST : ' + str(payload))

		inquiryStatus = "00"
		tenant = None
		e_tenant = None
		totalAmount = Decimal(0)
		reason = None
		e_reason = None
		null_check = False
		validate = False
		response_payload = {}

		CompanyCode = payload['CompanyCode']
		CustomerNumber = payload['CustomerNumber']
		RequestID = payload['RequestID']
		ChannelType = payload['ChannelType']
		TransactionDate = payload['TransactionDate']
		AdditionalData = payload['AdditionalData']

		if not CompanyCode:
			inquiryStatus = "01"
			reason = "Input CompanyCode kosong"
			e_reason = "Input CompanyCode is empty"
		if not CustomerNumber:
			inquiryStatus = "01"
			reason = "Input CustomerNumber kosong"
			e_reason = "Input CustomerNumber is empty"
		if not RequestID:
			inquiryStatus = "01"
			reason = "Input RequestID kosong"
			e_reason = "Input RequestID is empty"
		if not ChannelType:
			inquiryStatus = "01"
			reason = "Input ChannelType kosong"
			e_reason = "Input ChannelType is empty"
		if not TransactionDate:
			inquiryStatus = "01"
			reason = "Input TransactionDate kosong"
			e_reason = "Input TransactionDate is empty"

		if validateDate(TransactionDate) is False:
			inquiryStatus = "01"
			validate = True
			reason = "Input TransactionDate format tidak sesuai"
			e_reason = "Input TransactionDate format not valid"

		data_payment = Payment.objects.filter(va_no=CustomerNumber, status=1)

		payment = Payment.objects.filter(va_no=CustomerNumber).first()
		bank = Bank.objects.filter(company_code=CompanyCode).first()

		if payment is not None and bank is not None:
			logger.info(payment.id_customer)

			if payment.id_customer.startswith("MT"):
				id = payment.id_customer.replace("MT", "")
				logger.info("id mitra " + id)
				user = Mitra.objects.filter(id=id).first()
				user = user.name
			else:
				id = payment.id_customer.replace("ID", "")
				logger.info("id user " + id)
				user = Eeuser.objects.filter(id=id).prefetch_related("userdata").first()
				user = user.userdata.nama

			if len(data_payment) < 1:
				reason = "Sukses"
				e_reason = "Success"

		else:
			user = ""
			if null_check is False and validate is False:
				inquiryStatus = "01"
				if payment is None:
					reason = "VA tidak valid"
					e_reason = "VA not valid"
				if bank is None and payment is not None:
					reason = "Company code tidak ditemukan"
					e_reason = "Company code not found"

		if len(data_payment) < 1 or inquiryStatus == "01":

			response_payload['CompanyCode'] = CompanyCode
			response_payload['CustomerNumber'] = CustomerNumber
			response_payload['RequestID'] = RequestID
			response_payload['InquiryStatus'] = inquiryStatus
			response_payload['InquiryReason'] = {}
			response_payload['InquiryReason']["Indonesian"] = reason
			response_payload['InquiryReason']["English"] = e_reason
			response_payload['CustomerName'] = user
			response_payload['CurrencyCode'] = "IDR"
			response_payload['TotalAmount'] = "0.00"
			response_payload['SubCompany'] = "00000"
			list_detail_bill = []
			response_payload['DetailBills'] = list_detail_bill

			if payment is None:
				free_text_data = {}
				free_text = []
				free_text_data['Indonesian'] = "Gagal, pastikan input data dengan benar"
				free_text_data['English'] = "Failed, make sure the data input is correct"

				free_text.append(free_text_data)

				response_payload['FreeTexts'] = free_text
			elif inquiryStatus == "00":
				response_payload['FreeTexts'] = []
			else:
				free_text_data = {}
				free_text = []
				free_text_data['Indonesian'] = "Gagal, pastikan input data dengan benar"
				free_text_data['English'] = "Failed, make sure the data input is correct"

				free_text.append(free_text_data)
				response_payload['FreeTexts'] = free_text

			response_payload['AdditionalData'] = ""

			return JsonResponse(response_payload, status=status.HTTP_200_OK, safe=False)

		list_detail_bill = []
		subCompany = None
		productCode = None

		for data in data_payment:

			subCompany = data.payment_parent
			productCode = data.product_code
			bill = {}

			if data.tenant == '1':
				tenant = 'Tandatangan'
				e_tenant = 'Signature'
			if data.tenant == '2':
				tenant = 'Dokumen'
				e_tenant = 'Document'
			if data.tenant == '4':
				tenant = 'SMS OTP'
				e_tenant = 'SMS OTP'
			if data.tenant == '5':
				tenant = 'E-KYC'
				e_tenant = 'E-KYC'
			if data.tenant == '6':
				tenant = 'E-Seal'
				e_tenant = 'E-Seal'
			if data.tenant == '7':
				tenant = 'Verifikasi Text'
				e_tenant = 'Text Verification'
			if data.tenant == '8':
				tenant = 'Verifikasi Selfie'
				e_tenant = 'Selfie Verification'

			bill['BillDescription'] = {}
			bill['BillDescription']['Indonesian'] = tenant
			bill['BillDescription']['English'] = e_tenant
			bill['BillAmount'] = format(data.amount, '.2f')
			bill['BillNumber'] = data.id
			bill['BillSubCompany'] = subCompany

			logger.info(bill)
			list_detail_bill.append(bill)

			totalAmount = totalAmount + data.amount

		response_payload['CompanyCode'] = CompanyCode
		response_payload['CustomerNumber'] = CustomerNumber
		response_payload['RequestID'] = RequestID
		response_payload['InquiryStatus'] = inquiryStatus
		response_payload['InquiryReason'] = {}
		response_payload['InquiryReason']["Indonesian"] = "Sukses"
		response_payload['InquiryReason']["English"] = "Success"
		response_payload['CustomerName'] = user
		response_payload['CurrencyCode'] = "IDR"
		response_payload['TotalAmount'] = format(totalAmount, '.2f')
		response_payload['SubCompany'] = subCompany

		response_payload['DetailBills'] = list_detail_bill
		free_text = []

		free_text_data = [{
			"Indonesian": "Pembelian produk Digisign",
			"English": "Purchase Digisign products"
		}, {
			"Indonesian": productCode,
			"English": productCode
		}]

		free_text.append(free_text_data)

		response_payload['FreeTexts'] = free_text
		response_payload['AdditionalData'] = AdditionalData

		logger.info("RESPONSE : " + str(response_payload))
		return JsonResponse(response_payload, status=status.HTTP_200_OK, safe=False)


	@api_view(['POST'])
	def Payments(request):
		logger.info(request.data)
		payload = json.dumps(request.data)
		payload = json.loads(payload)
		logger.info('Payment modul')
		logger.info('Client IP : ' + get_client_ip(request))
		logger.info('REQUEST : ' + str(payload))

		response_payload = {}
		PaymentFlagStatus = "00"
		reason = "Sukses"
		e_reason = "Success"
		validate = False


		CompanyCode = payload['CompanyCode']
		CustomerNumber = payload['CustomerNumber']
		RequestID = payload['RequestID']
		ChannelType = payload['ChannelType']
		TransactionDate = payload['TransactionDate']
		AdditionalData = payload['AdditionalData']
		PaidAmount = payload['PaidAmount']
		CustomerName = payload['CustomerName']
		CurrencyCode = payload['CurrencyCode']
		TotalAmount = payload['TotalAmount']
		FlagAdvice = payload['FlagAdvice']
		DetailBills = payload['DetailBills']
		SubCompany = payload['SubCompany']
		Reference = payload['Reference']

		if not CompanyCode:
			PaymentFlagStatus = "01"
			reason = "Input CompanyCode kosong"
			e_reason = "Input CompanyCode is empty"
		if not CustomerNumber:
			PaymentFlagStatus = "01"
			reason = "Input CustomerNumber kosong"
			e_reason = "Input CustomerNumber is empty"
		if not RequestID:
			PaymentFlagStatus = "01"
			reason = "Input RequestID kosong"
			e_reason = "Input RequestID is empty"
		if not ChannelType:
			PaymentFlagStatus = "01"
			reason = "Input ChannelType kosong"
			e_reason = "Input ChannelType is empty"
		if not TransactionDate:
			PaymentFlagStatus = "01"
			reason = "Input TransactionDate kosong"
			e_reason = "Input TransactionDate is empty"
		if not PaidAmount:
			PaymentFlagStatus = "01"
			reason = "Input PaidAmount kosong"
			e_reason = "Input PaidAmount is empty"
		if not CustomerName:
			PaymentFlagStatus = "01"
			reason = "Input CustomerName kosong"
			e_reason = "Input CustomerName is empty"
		if not CurrencyCode:
			PaymentFlagStatus = "01"
			reason = "Input CurrencyCode kosong"
			e_reason = "Input CurrencyCode is empty"
		if not TotalAmount:
			PaymentFlagStatus = "01"
			reason = "Input TotalAmount kosong"
			e_reason = "Input TotalAmount is empty"
		if not FlagAdvice:
			PaymentFlagStatus = "01"
			reason = "Input FlagAdvice kosong"
			e_reason = "Input FlagAdvice is empty"
		if not SubCompany:
			PaymentFlagStatus = "01"
			reason = "Input SubCompany kosong"
			e_reason = "Input SubCompany is empty"
		if not Reference:
			PaymentFlagStatus = "01"
			reason = "Input Reference kosong"
			e_reason = "Input Reference is empty"
		if FlagAdvice not in ["Y", "N"]:
			PaymentFlagStatus = "01"
			reason = "Input FlagAdvice tidak valid"
			e_reason = "Invalid input FlagAdvice"

		if validateDate(TransactionDate) is False:
			PaymentFlagStatus = "01"
			validate = True
			reason = "Input TransactionDate format tidak sesuai"
			e_reason = "Input TransactionDate format not valid"

		data_payment = Payment.objects.filter(va_no=CustomerNumber, status=1)

		payment = Payment.objects.filter(va_no=CustomerNumber).first()

		bank = Bank.objects.filter(company_code=CompanyCode).first()

		if payment is not None and bank is not None:
			logger.info(payment.id_customer)

			if payment.id_customer.startswith("MT"):
				id = payment.id_customer.replace("MT", "")
				logger.info("id mitra " + id)
				user = Mitra.objects.filter(id=id).first()
				user = user.name
			else:
				id = payment.id_customer.replace("ID", "")
				logger.info("id user " + id)
				user = Eeuser.objects.filter(id=id).prefetch_related("userdata").first()
				user = user.userdata.nama

			if len(data_payment) < 1 and validate is False:
				reason = "Sukses"
				e_reason = "Success"

		else:
			user = ""

			PaymentFlagStatus = "01"
			if payment is None:
				reason = "VA tidak valid"
				e_reason = "VA not valid"
			if bank is None and payment is not None:
				reason = "Company code tidak ditemukan"
				e_reason = "Company code not found"

		totalAmount = float(0.00)
		for total in data_payment:
			totalAmount = totalAmount + total.amount

		if format(totalAmount, '.2f') != TotalAmount:
			PaymentFlagStatus = "01"
			reason = "TotalAmount tidak sama dengan tagihan"
			e_reason = "TotalAmount not the same as the bill"

		if PaymentFlagStatus == "01" or len(data_payment) < 1:
			response_payload['CompanyCode'] = CompanyCode
			response_payload['CustomerNumber'] = CustomerNumber
			response_payload['RequestID'] = RequestID
			response_payload['PaymentFlagStatus'] = PaymentFlagStatus
			response_payload['PaymentFlagReason'] = {
				"Indonesian": reason,
				"English": e_reason
			}
			response_payload['CustomerName'] = user
			response_payload['CurrencyCode'] = "IDR"
			response_payload['PaidAmount'] = "0.00"
			response_payload['TotalAmount'] = "0.00"
			response_payload['TransactionDate'] = TransactionDate
			response_payload['DetailBills'] = []
			response_payload['FreeTexts'] = [
				{"Indonesian": "",
				 "English": ""},
				{"Indonesian": "",
				 "English": ""},
				{"Indonesian": "",
				 "English": ""}
			]
			return JsonResponse(response_payload, status=status.HTTP_200_OK, safe=False)


		newTransactionDate = datetime.datetime.strptime(TransactionDate, '%d/%m/%Y %H:%M:%S')
		logger.info(newTransactionDate)

		for bill in data_payment:
			if bill.name_source != "internal":
				try:
					topup = billingTopup(external_key=bill.id_customer, amount=bill.jml_ttd, tenant=bill.tenant)
					if topup is not False:
						jsonFile = topup['JSONFile']
						if jsonFile['result'] == "00":
							# Generate data invoice on Database
							invoice = Invoice.objects.create(datetime=newTransactionDate, amount=bill.jml_ttd, eeuser=bill.eeuser,
							                                 external_key=bill.id_customer, tenant=bill.tenant, trx=1,
							                                 kb_invoice=jsonFile['invoiceid'],
							                                 cur_balance=jsonFile['current_balance'])

							# Update data payment by id
							update_payment = Payment.objects.get(id=bill.id)
							update_payment.id_invoice = invoice
							update_payment.invoice = jsonFile['invoiceid']
							update_payment.status = 3
							update_payment.trx_id = RequestID
							update_payment.date_confirmation = newTransactionDate
							update_payment.date_update = newTransactionDate
							update_payment.save()
						else:
							# save to message broker to retry
							PaymentFlagStatus = "01"
							reason = "Gagal proses topup"
							e_reason = "Failed topup process"
							response_payload['CompanyCode'] = CompanyCode
							response_payload['CustomerNumber'] = CustomerNumber
							response_payload['RequestID'] = RequestID
							response_payload['PaymentFlagStatus'] = PaymentFlagStatus
							response_payload['PaymentFlagReason'] = {
								"Indonesian": reason,
								"English": e_reason
							}
							response_payload['CustomerName'] = user
							response_payload['CurrencyCode'] = "IDR"
							response_payload['PaidAmount'] = PaidAmount
							response_payload['TotalAmount'] = TotalAmount
							response_payload['TransactionDate'] = TransactionDate
							response_payload['DetailBills'] = []
							response_payload['FreeTexts'] = [
								{"Indonesian": "",
								 "English": ""},
								{"Indonesian": "",
								 "English": ""},
								{"Indonesian": "",
								 "English": ""}
							]
							return JsonResponse(response_payload, status=status.HTTP_200_OK, safe=False)
					else:
						PaymentFlagStatus = "01"
						reason = "Gagal proses topup"
						e_reason = "Failed topup process"
						response_payload['CompanyCode'] = CompanyCode
						response_payload['CustomerNumber'] = CustomerNumber
						response_payload['RequestID'] = RequestID
						response_payload['PaymentFlagStatus'] = PaymentFlagStatus
						response_payload['PaymentFlagReason'] = {
							"Indonesian": reason,
							"English": e_reason
						}
						response_payload['CustomerName'] = user
						response_payload['CurrencyCode'] = "IDR"
						response_payload['PaidAmount'] = PaidAmount
						response_payload['TotalAmount'] = TotalAmount
						response_payload['TransactionDate'] = TransactionDate
						response_payload['DetailBills'] = []
						response_payload['FreeTexts'] = [
							{"Indonesian": "",
							 "English": ""},
							{"Indonesian": "",
							 "English": ""},
							{"Indonesian": "",
							 "English": ""}
						]
						return JsonResponse(response_payload, status=status.HTTP_200_OK, safe=False)
				except Exception as e:
					logger.error(traceback.print_exc())
					return JsonResponse(response_payload, status=status.HTTP_200_OK, safe=False)

		response_payload['CompanyCode'] = CompanyCode
		response_payload['CustomerNumber'] = CustomerNumber
		response_payload['RequestID'] = RequestID
		response_payload['PaymentFlagStatus'] = PaymentFlagStatus
		response_payload['PaymentFlagReason'] = {
			"Indonesian": reason,
			"English": e_reason
		}
		response_payload['CustomerName'] = user
		response_payload['CurrencyCode'] = "IDR"
		response_payload['PaidAmount'] = PaidAmount
		response_payload['TotalAmount'] = TotalAmount
		response_payload['TransactionDate'] = TransactionDate
		response_payload['DetailBills'] = []
		response_payload['FreeTexts'] = [
			{"Indonesian": "",
			 "English": ""},
			{"Indonesian": "",
			 "English": ""},
			{"Indonesian": "",
			 "English": ""}
		]

		logger.info("Update data topup on API Dashboard")
		for b in data_payment:
			updateTopup(b.product_code)
		logger.info("Done")

		logger.info("RESPONSE : " + str(response_payload))
		return JsonResponse(response_payload, status=status.HTTP_200_OK, safe=False)

	@api_view(['POST'])
	def CheckBill(request):

		logger.info(request.data)
		payload = json.dumps(request.data)
		payload = json.loads(payload)
		logger.info('Payment modul')
		logger.info('Client IP : ' + get_client_ip(request))
		logger.info('REQUEST : ' + str(payload))

		CustomerNumber = payload['virtual_account']

		list = listBill(CustomerNumber)
		logger.info(list)

		response_payload = {}

		if list is False:
			response_payload['message'] = "Failed"
			response_payload['result'] = "01"
			response_payload['data'] = "null"
		else:
			response_payload['message'] = "Success"
			response_payload['result'] = "00"
			response_payload['data'] = "list"

		return JsonResponse(response_payload, status=status.HTTP_200_OK, safe=False)