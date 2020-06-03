from sendy_it.exceptions import SendyAPIError


class Person:
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
    def __init__(self, name, lat, long, description, type):
        self.name = name
        self.lat = lat
        self.long = long
        self.description = description
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


def is_valid(response_data, raise_exception=True):
    response_status = response_data.get('status')
    if not response_status and raise_exception:
        raise SendyAPIError(response_data.get('description', response_data.get('data')))
    return bool(response_status)
