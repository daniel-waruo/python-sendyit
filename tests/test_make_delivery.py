import unittest
from sendy_it.settings import SENDY_API_KEY, SENDY_USERNAME
from sendy_it import SendyIT, Location, Person


class MakeDeliveryTestCase(unittest.TestCase):
    """Test making deliveries """

    def setUp(self) -> None:
        self.sendy = SendyIT(SENDY_API_KEY, SENDY_USERNAME)
        self.recipient = Person(
            name='John Doe King',
            phone='0722180542',
            email='johndoe@gmail.com',
            type='recepient'
        )
        self.sender = Person(
            name="Jane King Doe",
            phone="0797792447",
            email="sendyer@gmail.com",
            type='sender',
            sender_notes="Sender specific notes"
        )
        self.to_location = Location(
            name='Green House',
            lat='-1.385',
            long='36.489',
            description='office',
            type='to'
        )
        self.from_location = Location(
            name='Lavington',
            lat='-1.26869',
            long='36.885',
            description='home',
            type='from'
        )

    def test_making_delivery(self):
        data = self.sendy.make_delivery(
            recipient=self.recipient,
            sender=self.sender,
            to_location=self.to_location,
            from_location=self.from_location
        )
        self.assertEqual(data['data']['order_status'], 'order_placed')

    def test_getting_delivery_quotes(self):
        data = self.sendy.get_delivery_quote(
            recipient=self.recipient,
            sender=self.sender,
            to_location=self.to_location,
            from_location=self.from_location
        )
        self.assertEqual(data['data']['order_status'], 'quote_received')
