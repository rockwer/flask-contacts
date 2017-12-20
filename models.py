from mongoengine import *

class Contact(Document):
    name = StringField(max_length=50)
    email = StringField(max_length=50)  #required=True)
    phone = StringField(max_length=10)
    registration_date = StringField(max_length=50)