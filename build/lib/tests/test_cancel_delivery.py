import unittest
import json
from sendy_it.settings import SENDY_API_KEY, SENDY_USERNAME
from sendy_it import SendyIT, Location, Person


class CancelDeliveryTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.sendy = SendyIT(SENDY_API_KEY, SENDY_USERNAME)
        self.response_data = self.sendy.make_delivery(
            recipient=Person(
                name='John Doe',
                phone='0710180542',
                email='johndoe@gmail.com',
                type='recepient'
            ),
            sender=Person(
                name="Jane King",
                phone="0797792447",
                email="sendyer@gmail.com",
                type='sender',
                sender_notes="Sender specific notes"
            ),
            to_location=Location(
                name='Green House',
                lat='-1.385',
                long='36.489',
                description='office',
                type='to'
            ),
            from_location=Location(
                name='Lavington',
                lat='-1.26869',
                long='36.885',
                description='home',
                type='from'
            )
        )

    def test_cancel_delivery(self):
        order_no = self.response_data['data']['order_no']
        self.sendy.cancel_delivery(order_no)