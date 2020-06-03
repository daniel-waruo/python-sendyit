import requests
import json

from sendy_it.utils import is_valid
from sendy_it.exceptions import MissingAPICredentions


class SendyIT:
    """Class to abstract calls to sendy it platform"""
    sandbox_url = 'https://apitest.sendyit.com/v1/'
    production_url = 'https://api.sendyit.com/v1/'

    def __init__(self, api_key, username, production=False):
        self.api_key = api_key
        self.username = username
        if not (self.api_key or self.username):
            raise MissingAPICredentions("Make sure the API Key and Username are filled")
        # set api url as production_url if production is true
        self.api_url = self.production_url if production else self.sandbox_url

    @property
    def auth(self):
        return {
            'api_key': self.api_key,
            'api_username': self.username
        }

    def _request_delivery(self, recipient, sender, to_location, from_location, request_type):
        """Creates a delivery request obtaining rates and estimating time of arrival"""
        url_path = '{}##request'.format(self.api_url)
        pay_load = {
            'command': 'request',
            'data': {
                **self.auth,
                **recipient.to_dict(),
                **sender.to_dict(),
                **to_location.to_dict(),
                **from_location.to_dict(),
                'delivery_details': {
                    'request_type': request_type
                }
            }
        }
        headers = {'content-type': 'application/json'}
        response = requests.post(
            url_path,
            data=json.dumps(pay_load),
            headers=headers
        )
        response.raise_for_status()
        response_data = response.json()
        # check if response was successful else raise and error
        is_valid(response_data, raise_exception=True)
        return response_data

    def make_delivery(self, **kwargs):
        return self._request_delivery(request_type='delivery', **kwargs)

    def get_delivery_quote(self, **kwargs):
        return self._request_delivery(request_type='quote', **kwargs)

    def _delivery_operations(self, operation, order_no):
        """ Create a commone interface where all delivery specific operations will be performed """
        url_path = '{}#{}'.format(self.api_url, operation)
        pay_load = {
            'command': operation,
            'data': {
                **self.auth,
                'order_no': order_no
            }
        }
        headers = {'content-type': 'application/json'}
        response = requests.post(
            url_path,
            data=json.dumps(pay_load),
            headers=headers
        )
        response.raise_for_status()
        response_data = response.json()
        # check if response was successful else raise and error
        is_valid(response_data, raise_exception=True)
        return response_data

    def complete_delivery(self, order_no):
        """Creates a delivery request obtaining rates and estimating time of arrival"""
        return self._delivery_operations('complete', order_no)

    def cancel_delivery(self, order_no):
        """ Cancels delivery of a certain good """
        return self._delivery_operations('cancel', order_no)

    def track_delivery(self, order_no):
        """ Tracks the delivery """
        return self._delivery_operations('track', order_no)
