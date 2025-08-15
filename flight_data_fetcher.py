import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

"""
flight_data_fetcher.py
---------------------

This module provides the FlightDataFetcher class for fetching flight offers from the Amadeus API
and extracting airline names from the IATA website. It supports searching for flights over a date range
and returning structured flight data.
"""

class FlightDataFetcher:
    def __init__(
        self,
        api_key,
        api_secret,
        origin,
        destination,
        start_date,
        end_date,
        max_price=50000,
        travel_class="ECONOMY"
    ):
        """
        Initialize the FlightDataFetcher with API credentials and search parameters.
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.origin = origin.upper()
        self.destination = destination.upper()
        self.start_date = start_date
        self.end_date = end_date
        self.max_price = max_price
        self.travel_class = travel_class
        self.token = self.get_access_token()

    def get_access_token(self):
        """
        Request an OAuth access token from Amadeus API.

        Returns:
            str: Access token string.
        """
        url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.api_secret
        }
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return response.json()['access_token']

    def search_flights(self, date):
        """
        Search for flight offers for a specific date using Amadeus API.

        Args:
            date (str): Date in 'YYYY-MM-DD' format.

        Returns:
            list: List of flight offer dictionaries.
        """
        url = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {
            'originLocationCode': self.origin,
            'destinationLocationCode': self.destination,
            'departureDate': date,
            'adults': 1,
            'currencyCode': 'INR',
            'travelClass': self.travel_class,
            'maxPrice': self.max_price,
            'max': 20
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()['data']

    def get_airline_name(self, airline_code):
        """
        Look up the airline name for a given IATA airline code using the IATA website.

        Args:
            airline_code (str): IATA airline code.

        Returns:
            str or None: Airline name if found, else None.
        """
        url = f"https://www.iata.org/en/publications/directories/code-search?airline.search={airline_code}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.select_one("table.datatable")
        if not table:
            return None
        tbody = table.find("tbody")
        if not tbody:
            return None
        first_row = tbody.find("tr")
        if not first_row:
            return None
        first_cell = first_row.find("td")
        return first_cell.get_text(strip=True) if first_cell else None

    def get_dates_range(self):
        """
        Generate a list of date strings from start_date to end_date (inclusive).

        Returns:
            list: List of date strings in 'YYYY-MM-DD' format.
        """
        start = datetime.strptime(self.start_date, "%Y-%m-%d")
        end = datetime.strptime(self.end_date, "%Y-%m-%d")
        delta = (end - start).days
        return [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(delta + 1)]

    def fetch(self):
        """
        Fetch flight offers for all dates in the range and return structured flight data.

        Returns:
            list: List of flight details, each as a list of values.
        """
        all_flights = []
        dates = self.get_dates_range()
        for date in dates:
            print(f"Searching flights from {self.origin} to {self.destination} on {date}...")
            flights = self.search_flights(date)
            for offer in flights:
                # Extract flight details from offer
                itinerary = offer['itineraries'][0]['segments'][0]
                airline = self.get_airline_name(itinerary['carrierCode'])
                aircraft = itinerary.get('aircraft', {}).get('code', 'Unknown')
                duration = offer['itineraries'][0]['duration'].replace('PT', '').replace('H', 'h ').replace('M', 'm')
                price = offer['price']['total']
                all_flights.append([
                    self.origin,
                    self.destination,
                    date,
                    airline,
                    price,
                    duration,
                    aircraft
                ])
        return all_flights