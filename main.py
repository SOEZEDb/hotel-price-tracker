from data_manager import DataManager
from hotel_search import HotelSearch
from requests.exceptions import RequestException, Timeout, ConnectionError
from  json.decoder import JSONDecodeError

hotel_search = HotelSearch()
data_manager = DataManager()
sheety_data = data_manager.read_data()
cities = sheety_data['sheet1']
for city in cities:
    try:
        dest_id = hotel_search.get_destination_id(city['city'])
        hotel_name, price, url = hotel_search.search_hotel(dest_id)

        if hotel_name is not None:
            print(f"Skipping {city['city']} - no valid hotel prices found.")
            continue
        if  price < city['lowestPrice']:
            print(f"Alert! {hotel_name} in {city['city']} has a price of {price}! Book here: {url}.")
            data_manager.update_price(city['id'], price)
        print(city['city'], hotel_name, price, url)
    except ValueError as e:
        print(f"City not found: {city['city']} - {e}")
    except (ConnectionError, Timeout) as e:
        print(f"Network issue for {city['city']}: {e}")
    except KeyError as e:
        print(f"Unexpected API response for {city['city']}: missing {e}")
    except Exception as e:
        print(f"Unexpected exception for {city['city']}: {e}")
    except JSONDecodeError as e:
        print(f"Invalid Json from API for {city['city']}: {e}")