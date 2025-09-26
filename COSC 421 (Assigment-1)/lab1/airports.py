# this is my initial plan for collecting airport arrivals and departures as a csv

# I record the information in a csv list under 2 columns: airport1 and airport2 where columns are codenames. I also will not record repeated flights.

# lets start from Toronto
# actually lets only do the first page and then manually jump to the next page and we need to record the datetime too


import requests
import os
import time
from datetime import datetime, timedelta, timezone

# --- Configuration ---
API_KEY = os.getenv("AEROAPI_KEY")
ORIGIN_AIRPORT_CODE = "CYAX"

# --- API Request ---
AEROAPI_BASE_URL = "https://aeroapi.flightaware.com/aeroapi"



try:
    # =========================================================================
    # PHASE 1: Find the departure time of the first available flight
    # =========================================================================
    print(f"--- Phase 1: Finding the first departure from {ORIGIN_AIRPORT_CODE} ---")
    
    endpoint = f"/airports/{ORIGIN_AIRPORT_CODE}/flights"
    url = AEROAPI_BASE_URL + endpoint
    headers = {"x-apikey": API_KEY}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    # This check handles if the very first API call is empty
    if not data:
        raise ValueError("Initial API response was empty. Cannot determine a start time.")

    start_time = None
    all_departures = data.get("scheduled_departures", []) # I will only take scheduled departures

    if not all_departures:
        print(f"No departures found for {ORIGIN_AIRPORT_CODE}. Exiting.")
    else:
        for flight in all_departures:
            time_str = flight.get("scheduled_out")
            if time_str:
                current_flight_time = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
                if start_time is None or current_flight_time < start_time:
                    start_time = current_flight_time

    if start_time:
        end_time = start_time + timedelta(hours=24)
        print(f"First departure found at: {start_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        print(f"Fetching flights until:   {end_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")

        # =====================================================================
        # PHASE 2: Fetch all flights within that 24-hour window
        # =====================================================================
        print("\n--- Phase 2: Fetching all flights in the 24-hour window ---")
        destination_codes = set()
        
        url = AEROAPI_BASE_URL + endpoint
        params = {
            "type": "departure",
            "start": start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "end": end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        }

        while url:
            print(f"URL is now: {url}")
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            paged_data = response.json()

            # --- THIS IS THE FIX ---
            # Add the check here to handle empty pages during pagination.
            if not paged_data:
                print("Received an empty response page. Ending pagination.")
                break
                # actually lets make a tuple for destination codes
            departures_on_page = paged_data.get("scheduled_departures", [])
            if not departures_on_page:
                print("No departures found on this page.")
                print(f"Start time: {start_time} End time {end_time} destination codes {destination_codes}")
                break

            for flight in departures_on_page:
                if flight and flight.get("destination"):
                    dest_code = flight["destination"].get("code")
                    if dest_code.startswith("C") and dest_code != ORIGIN_AIRPORT_CODE:
                        destination_codes.add((ORIGIN_AIRPORT_CODE, dest_code))
                        print(f"Destination code is {dest_code}")
            
            print(f"Start time: {start_time} End time {end_time} destination codes {destination_codes}")

            next_page_link = paged_data.get("links", {}).get("next")
            if next_page_link:
                url = AEROAPI_BASE_URL + next_page_link
                params = {}
                print("Fetching next page...")
                print("Waiting to respect rate limit...")
                time.sleep(6.1)
            else:
                print("No more pages to fetch.")
                url = None
        

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    print(f"Response content: {response.text}")
except Exception as err:
    print(f"An other error occurred: {err}")

