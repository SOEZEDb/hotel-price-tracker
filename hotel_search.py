import requests
import os
from dotenv import load_dotenv


load_dotenv()

class HotelSearch:
    def get_destination_id(self, city_name):
        dest_url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"
        headers = {
            "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
            "x-rapidapi-host": "booking-com.p.rapidapi.com"
        }

        parameters = {
            "name": city_name,
            "locale": "en-gb"
        }

        response = requests.get(dest_url, headers=headers, params=parameters)
        data = response.json()
        for item in data:
            if item["dest_type"] == "city":
                return (item["dest_id"])
        raise ValueError(f"{city_name} could not be found.")

    def search_hotel(self, dest_id):
        search_url = "https://booking-com.p.rapidapi.com/v1/hotels/search"

        headers = {
            "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
            "x-rapidapi-host": "booking-com.p.rapidapi.com"
        }

        parameters = {
            "dest_id": dest_id,
            "dest_type": "city",
            "units": "metric",
            "locale": "en-gb",
            "filter_by_currency": "USD",
            "order_by": "price",
            "checkin_date": "2026-09-18",
            "checkout_date": "2026-09-19",
            "room_number": "1",
            "adults_number": "1",
        }
        response = requests.get(search_url, headers=headers, params=parameters)
        data = response.json()
        #return response.json()

        prices = []
        for item in data['result']:
            if item['min_total_price'] is not None:
                prices.append(item['min_total_price'])
        if not prices:
                print(f"No valid prices found for {dest_id}")
                return None, None, None
        cheapest = min(prices)
        for item in data['result']:
            if item['min_total_price'] == cheapest:
                return item['hotel_name'], cheapest, item['url']








