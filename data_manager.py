import requests
import os
from dotenv import load_dotenv

load_dotenv()

sheety_endpoint = os.getenv("SHEETY_ENDPOINT")

class DataManager:

    def read_data(self):
        response = requests.get(sheety_endpoint)
        return response.json()

    def update_price(self, city_id, new_price):
        url = f"{sheety_endpoint}/{city_id}"
        updated_data = {
            "sheet1": {
                "lowestPrice": new_price
            }
        }
        response = requests.put(url, json=updated_data)
        print(response.text)