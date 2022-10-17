from rest_framework.decorators import api_view
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def oAuth2(request):
	return None