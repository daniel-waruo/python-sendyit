# python-sendy-it

This is a python wrapper for the sendy It API.
It allows me to abstract sending requests and responses to the sendy api

## Prerequisites
In order for one to use this library one must have.
* python

## Installation
THe library can be installed by cloning the repository or
installing it using pip

**clone the repository**
```shell script
git clone https://github.com/daniel-waruo/python-sendyit.git
``` 

#### or

**install via pip**
```shell script
pip install git+https://github.com/daniel-waruo/python-sendyit.git
``` 

## Usage

```python
from sendy_it import SendyIT,Person,Location
import os

# get the api username and api key to instantiate SendyIT
SENDY_USERNAME = os.getenv("SENDY_USERNAME")
SENDY_APIKEY = os.getenv("SENDY_USERNAME")

# instantiate sendy setting production to false
# This means that the api will be using the sandbox environment
sendy = SendyIT(SENDY_APIKEY,SENDY_APIKEY,production=False)

# details of the person who is receiving the package
recipient = Person(
    name='John Doe King',
    phone='0722180542',
    email='johndoe@gmail.com',
    type='recepient'
)

# details of the person who is sending the package
sender = Person(
    name="Jane King Doe",
    phone="0797792447",
    email="sendyer@gmail.com",
    type='sender',
    sender_notes="Sender specific notes"
)

# location from where the package will be received
from_location = Location(
    name='Lavington',
    lat='-1.26869',
    long='36.885',
    description='home',
    type='from'
)

# location where the package will be delivered to
to_location = Location(
    name='Green House',
    lat='-1.385',
    long='36.489',
    description='office',
    type='to'
)
################################
#     make delivery            #
################################
response_data = sendy.make_delivery(
            recipient=recipient,
            sender=sender,
            to_location=to_location,
            from_location=from_location
        )

################################
#  get delivery rates  quotes  #
################################
response_data = sendy.get_delivery_quote(
            recipient=recipient,
            sender=sender,
            to_location=to_location,
            from_location=from_location
        )


###############################
#     complete delivery       #
###############################

# if one had previously called get_delivery_quote()
# one can complete the transaction using this method
order_no = 'Example Order No'
response_data = sendy.complete_delivery(order_no)



###############################
#     cancel delivery         #
###############################

# if one wants to cancel a delivery
response_data = sendy.cancel_delivery(order_no)


###############################
#     track the delivery      #
###############################

# if one wants to cancel a delivery
response_data = sendy.track_delivery(order_no)


```
## Running the tests
To run the tests :-

```
python -m unittest 
```

## Authors

* **Daniel Waruo** - *contact* - waruodaniel@gmail.com