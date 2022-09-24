import sqlite3, requests, json
from sqlite3 import Error
from pprint import pprint
from datetime import datetime, timezone
from auth import *

def get_timestamp():
    now = datetime.now(tz=timezone.utc)
    return now.isoformat().split('.')[0]

url = "http://test.api.amadeus.com"
api_key = get_stored_auth()
url = "https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode=MNL&destinationLocationCode=BKK&departureDate=2022-11-01&adults=1&nonStop=false&max=250"

headers = {
    "accept": "application/vnd.amadeus+json",
    "Authorization": f"Bearer {api_key}"
}

r = requests.get(url, headers=headers)
response = r.json()

for flight in response.get('data'):
    for segment in flight['itineraries'][0]['segments']:
        departure = segment['departure']['at']
        arrival = segment['arrival']['at']
        depart_code = segment['departure']['iataCode']
        arrive_code = segment['arrival']['iataCode']
        airline = segment['carrierCode']
        aircraft = segment['aircraft']['code']

        where = [
            f"departure = '{departure}'",
            f"arrival = '{arrival}'",
            f"airline = '{airline}'",
            f"depart_code = '{depart_code}'",
            f"arrive_code = '{arrive_code}'",
        ]
        existing = select(fields=['id'], table='flights', where=where)
        if len(existing) > 0:
            pass
        else:
            data = {
                "test": 1,
                "departure": departure,
                "arrival": arrival,
                "depart_code": depart_code,
                "arrive_code": arrive_code,
                "airline": airline,
                "aircraft": aircraft,
                "last_updated": get_timestamp()
            }
            insert(table='flights',
                   data=data)
