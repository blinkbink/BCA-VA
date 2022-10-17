import hmac
import hashlib
import logging

logger = logging.getLogger(__name__)

def createSignature(api_secret, message):

	signature = hmac.new(bytes(api_secret , 'latin-1'), msg = bytes(message , 'latin-1'), digestmod = hashlib.sha256).hexdigest().upper()
	logger.info("Generated Signature : " + signature)

	return signature