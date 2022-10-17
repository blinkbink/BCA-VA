import socket

class Constant():

	'''
	BCA_API : Host domain service of BCA
	BCA_VA_PAYMENTS : Flag considered as “already paid” for the specified copartner transaction
	BCA_VA_BILL : Get list of customer’s bills from copartners
	BCA_ACCESS_TOKEN : Get access token for Authorization
	BCA_TRANSFER : Fund Transfer to another BCA account
	'''

	#           Development
	# # BCA host
	# BCA_API = "https://devapi.klikbca.com:9443/"
	# # BCA Path
	# BCA_ACCESS_TOKEN = "api/oauth/token"
	# BCA_VA_BILL = "va/bills"
	# BCA_VA_PAYMENTS = "va/payments"
	# BCA_TRANSFER = "/banking/corporates/transfers"
	#
	#
	# #Billing host
	# # BILLING_API = "https://"+socket.gethostbyname('billingapi')+":1070/"
	# #Billing path
	# BILLING_TOPUP = "BillingAPI/TopupCustom.html"
	# BILLING_BALANCE = "BillingAPI/Balance.html"


	#            Production
	# # BCA host
	# BCA_API = "https://devapi.klikbca.com:9443/"
	# # BCA Path
	# BCA_ACCESS_TOKEN = "api/oauth/token"
	# BCA_VA_BILL = "va/bills"
	# BCA_VA_PAYMENTS = "va/payments"
	# BCA_TRANSFER = "/banking/corporates/transfers"
	#
	# #Billing host
	# BILLING_API = "https://"+socket.gethostbyname('billingapi')+":1070/"
	# #Billing path
	# BILLING_TOPUP = "BillingAPI/TopupCustom.html"
	# BILLING_BALANCE = "BillingAPI/Balance.html"
