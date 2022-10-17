import datetime
import json
import logging
import re

from django.db import connection
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from va.Models.Bank import Bank
from va.Models.Eeuser import Eeuser
from va.Models.Mitra import Mitra
from va.Models.Payment import Payment
from ..Controller.UsersController import get_client_ip

logger = logging.getLogger(__name__)

@api_view(['POST', 'DELETE'])
def Topup(request):
	
	payload = json.dumps(request.data)
	payload = json.loads(payload)
	logger.info("Topup modul")
	logger.info("Client IP : " + get_client_ip(request))
	logger.info("Request : " + str(payload))

	if request.method == "POST":
		va = None

		bankFrom = payload['bank_from']
		bankTo = payload['bank_to']
		user = payload['user']
		product = payload['product']
		mitra = re.split('(\d+)', payload['mitra'])
		topup_type = payload['topup_type']
		source = None

		if 'source' in payload:
			source = payload['source']

		productCode = None
		if 'invoice' in payload:
			productCode = payload['invoice']

		bankfrom = Bank.objects.filter(bank_code=bankFrom).first()
		bankto = Bank.objects.filter(bank_code=bankTo).first()
		logger.info(mitra[1])
		q_mitra = Mitra.objects

		if q_mitra.filter(id=mitra[1]).count() < 1:
			return JsonResponse({"message": "Data mitra not found", "status": "01"}, status=status.HTTP_404_NOT_FOUND,
			                    safe=False)

		s_user = re.split('(\d+)', user)

		if s_user[0] == "MT":
			q_user = Mitra.objects.filter(id=s_user[1])
			if q_user.count() < 1:
				return JsonResponse({"message": "Data mitra not found", "status": "01"}, status=status.HTTP_404_NOT_FOUND,
				                    safe=False)
			instance = Eeuser.objects.filter(mitra=s_user[1], admin=True).order_by("id")[:1].get()
			logger.info(instance)
		elif s_user[0] == "ID":
			q_user = Eeuser.objects.filter(id=s_user[1]).prefetch_related('userdata')
			if q_user.count() < 1:
				return JsonResponse({"message": "Data user not found", "status": "01"}, status=status.HTTP_404_NOT_FOUND,
				                    safe=False)
			instance = Eeuser.objects.get(id=s_user[1])
		else:
			return JsonResponse({"message": "Data user not found", "status": "01"}, status=status.HTTP_404_NOT_FOUND,
			                    safe=False)

		if s_user[0] == "MT":
			default = "00000000000"[:-len(str(q_user.first().id))] + str(q_user.first().id)

			va = str(bankto.company_code) + str(default)
		elif s_user[0] == "ID":
			phone = q_user.first().userdata.no_handphone

			if phone.startswith("+62"):
				phone = phone.replace(phone[0:3], "0")

			if phone.startswith("62"):
				phone = phone.replace(phone[0:2], "0")

			phone.strip()
			logger.info(phone)
			va = bankto.company_code + re.sub("[^0-9]", "", phone)

		logger.info(va)
		payment = Payment.objects.filter(va_no=va, status=1)

		if len(payment) > 0:
			return JsonResponse({"message": "Bill virtual account is active", "status": "01"},
			                    status=status.HTTP_403_FORBIDDEN, safe=False)

		timestamps = datetime.datetime.now()
		expired = timestamps + datetime.timedelta(hours=5)

		payment_parent = None
		for i in range(0, len(product)):
			with connection.cursor() as cursor:
				cursor.execute("SELECT last_value FROM payment_seq")
				row = cursor.fetchone()

			if i == 0:
				payment_parent = row[0] + 1

			next_sequence = row[0] + 1

			with connection.cursor() as cursor:
				cursor.execute("SELECT setval('payment_seq', " + str(next_sequence) + ", true)")
				cursor.fetchone()

			payment = Payment.objects.create(id=next_sequence, bank_from=bankfrom.name, bank_to=bankto.name,
			                                 id_customer=user,
			                                 eeuser=instance,
			                                 status=1, date_update=None, date_request=timestamps,
			                                 date_confirmation=None, jml_ttd=product[i]['amount'],
			                                 amount_original=product[i]['price'], tenant=product[i]['tenant'],
			                                 amount=int(product[i]['amount']) * int(product[i]['price']),
			                                 id_invoice=None, topup_type=topup_type,
			                                 product_code=productCode,
			                                 name_source=source, va_no=va, trx_id=None, invoice=None,
			                                 exp_date=expired, payment_parent=payment_parent)

		payload = {
			"status": "00",
			"expired_date": expired,
			"virtual_account": va
		}
	else:

		payment = Payment.objects.filter(va_no=payload['virtual_account'], status=1)

		if len(payment) < 1:
			payload = {
				"status": "01",
				"message": "Virtual account not exist"
			}
		else:
			payment.update(status=4)

			payload = {
				"status": "00",
				"message": "Success cancel virtual account"
			}

	logger.info("RESPONSE : " + str(payload))
	return JsonResponse(payload, status=status.HTTP_200_OK, safe=False)