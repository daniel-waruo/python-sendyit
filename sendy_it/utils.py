from datetime import datetime
from sendy_it.exceptions import SendyAPIError


class Person:
    """Describes a person involved in delivery

    Args:
        name - name of the person being delivered to
        email - email of the person involved
        phone - phone number of the person involved
        type - type of person whether a 'recepient' or a 'sender'
    """

    def __init__(self, name, email, phone, type, **extras):
        self.name = name
        self.email = email
        self.phone = phone
        self.extras = extras
        if type not in ['recepient', 'sender']:
            raise ValueError("Type must be either 'recepient' or 'sender' .")
        self.type = type

    def to_dict(self):
        return {
            self.type: {
                self.type + '_name': self.name,
                self.type + '_phone': self.phone,
                self.type + '_email': self.email,
                **self.extras
            }
        }


class Location:
    """ Object that describes a location
    Args:
        name - name of location to be delivered to
        lat - latitude of location to be delivered to
        long - longitude of location to be delivered to
        description - a short description of the location
        type - type of location whether to or from
    """

    def __init__(self, name, lat, long, description, type):
        self.name = name
        self.lat = lat
        self.long = long
        self.description = description
        assert type in ('to', 'from')
        self.type = type

    def to_dict(self):
        return {
            self.type: {
                self.type + '_name': self.name,
                self.type + '_lat': float(self.lat),
                self.type + '_long': float(self.long),
                self.type + '_description': self.description,
            }
        }


class Payment:
    """Manages payment in the deliveries

    Args:
        amount - Amount of money in Kenyan shilling than will be charged
        payment_method - Payment method to be used should be either 0 or 1
        
    """

    def __init__(self, amount: float, payment_method: int):
        self.amount = amount
        self.payment_method = payment_method
        assert payment_method in (1, 0)

    def to_dict(self):
        return {
            'status': True,
            'amount': str(self.amount),
            'pay_method': self.payment_method
        }


class DeliveryItem:
    """Object holds the details of an items to be delivered

    TODO:find out the units of measurement of these parameters

    Args:
        name - Name of the item to be delivered
        weight - Weight of the item to be delivered
        height - Height of the item to be delivered
        width - Width of the item to be delivered
        length - Length of the item to be delivered
    """

    def __init__(self, name, weight=None, height=None, width=None, length=None):
        self.name = name
        self.weight = weight
        self.height = height
        self.width = width
        self.length = length

    def to_dict(self):
        return {
            'weight': self.weight,
            'height': self.height,
            'width': self.width,
            'length': self.length,
            'item_name': self.name
        }


class Delivery:
    """Handles all the specific delivery details

    Args:
        items - it is a list of Delivery items to be delivered
        delivery_note - Note to be read to user during the delivery
        pickup_data - Data when the delivery will be picked up from
        express - choose whether the order should be an express order of batched with other deliveries
        return_delivery - should be True if the order is two-way and false if otherwise
        carrier_type - either 1 or 0 if 1 for a closed vehicle 0 for an open one
    """

    def __init__(self, items=None, delivery_note='', pickup_date: datetime = None, express=False,
                 return_delivery=False, carrier_type=0, payment: Payment = None):
        self.items = []
        if items is not None:
            self.add(items)
        self.delivery_note = delivery_note
        self.pickup_date = pickup_date
        self.express = express
        self.return_delivery = return_delivery
        assert carrier_type in (1, 0)
        self.carrier_type = carrier_type
        self.payment = payment

    def add(self, items: list):
        """ Add items to the list
        Args:
            items - list of DeliveryItems
        """
        if items is None:
            raise Exception("items is  None")
        items_list = list(map(
            lambda item: item.to_dict(),
            items
        ))
        items_list = items_list
        self.items += items_list

    def to_dict(self):
        data = {
            'package_size': self.items,
            'express': self.express,
            'return': self.return_delivery,
        }
        if self.delivery_note:
            data['note'] = self.delivery_note
            data['note_status'] = True
        if self.pickup_date:
            data['pick_up_date'] = self.pickup_date.isoformat()
        if self.payment:
            data['collect_payment'] = self.payment.to_dict()
        return data


def is_valid(response_data, raise_exception=True):
    """ checks if the response is valid or has an error

    Args:
        response_data - data from the request
        raise_exception - boolean value whether to raise exception or not
    """
    response_status = response_data.get('status')
    if not response_status and raise_exception:
        raise SendyAPIError(response_data.get('description', response_data.get('data')))
    return bool(response_status)
