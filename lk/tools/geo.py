import requests

class Geo:
    def __init__(self, adress):
        self.adress = adress
        self.long = 0.0
        self.lat = 0.0
    
    def serializer(self, long_and_lat):
        pass