import requests
import json

from sendy_it.utils import is_valid, Delivery, Location, Person
from sendy_it.exceptions import MissingAPICredentions


class SendyIT:
    """Class to abstract calls to sendy it platform

    Args:
        api_key - Your Sendy API KEY
        username - Your Sendy username
        production - True it uses the production API endpoint if false it used the sandbox API environment
    """
    sandbox_url = 'https://apitest.sendyit.com/v1/'
    production_url = 'https://api.sendyit.com/v1/'

    def __init__(self, api_key: str, username: str, production: bool = False):
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

    def _request_delivery(self, recipient: Person, sender: Person, to_location: Location, from_location: Location,
                          request_type: str, vendor_type: int = 1,
                          order: bool = False, delivery_details: Delivery = None):
        """Creates a delivery request obtaining rates and estimating time of arrival
        Args:
            recipient - Person to whom the delivery will be sent to
            sender - Person to who is sending the delivery
            to_location - Location where the delivery will be sent
            from_location -Location where the delivery will be received from
            request_type - type of request whether to get a  price quotation or a delivery should be either 'quote' or 'delivery'
            vendor_type - type of vendor: 1 for bike ,2 for pickup,3 for van , 21 for runner within nairobi
            delivery_details - Details of the delivery
        """
        url_path = '{}##request'.format(self.api_url)
        assert request_type in ['quote', 'delivery']
        # delivery data of the delivery items,etx
        if delivery_details is None:
            delivery_details = Delivery()
        pay_load = {
            'command': 'request',
            'data': {
                **self.auth,
                **recipient.to_dict(),
                **sender.to_dict(),
                **to_location.to_dict(),
                **from_location.to_dict(),
                'vendor_type': vendor_type,
                "ecommerce_order": order,
                'delivery_details': {
                    'request_type': request_type,
                    **delivery_details.to_dict()
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

    def make_delivery(self, recipient, sender, to_location, from_location, delivery_details=None, vendor_type=1,
                      order=False):
        """ Make a new delivery to requested location  """
        return self._request_delivery(
            recipient=recipient,
            sender=sender,
            to_location=to_location,
            from_location=from_location,
            vendor_type=vendor_type,
            order=order,
            delivery_details=delivery_details,
            request_type='delivery',
        )

    def get_delivery_quote(self, recipient, sender, to_location, from_location,
                           delivery_details=None, vendor_type=1, order=False):
        """Gets the delivery quote of price from one place to another"""
        return self._request_delivery(
            recipient=recipient,
            sender=sender,
            to_location=to_location,
            from_location=from_location,
            vendor_type=vendor_type,
            order=order,
            delivery_details=delivery_details,
            request_type='quote'
        )

    def _delivery_operations(self, operation, order_no):
        """Bundles all order_no specific operations together"""
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
