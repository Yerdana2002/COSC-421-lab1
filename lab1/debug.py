import requests
import os
import json
from datetime import datetime, timedelta

# --- Configuration ---
API_KEY = os.getenv("AEROAPI_KEY")
ORIGIN_AIRPORT_CODE = "CYVR"

# --- Use the exact 24-hour window from your last successful log ---
# This ensures we are debugging the exact query that is failing in Phase 2.
start_time_str = "2025-09-13T23:10:00Z"
end_time_str = "2025-09-14T23:10:00Z"

# --- API Request ---
AEROAPI_BASE_URL = "https://aeroapi.flightaware.com/aeroapi"

if not API_KEY:
    raise ValueError("AEROAPI_KEY environment variable not set.")

print(f"--- Debugging: Fetching the FIRST page for {ORIGIN_AIRPORT_CODE} ---")
print(f"Window: {start_time_str} to {end_time_str}")

try:
    endpoint = f"/airports/{ORIGIN_AIRPORT_CODE}/flights"
    url = AEROAPI_BASE_URL + endpoint
    headers = {"x-apikey": API_KEY}
    params = {
        "type": "departure",
        "start": start_time_str,
        "end": end_time_str
    }

    response = requests.get(url, headers=headers, params=params)
    
    print(f"\n1. HTTP Status Code: {response.status_code}")
    response.raise_for_status() # This will still raise an error for 4xx/5xx codes

    # Try to parse the JSON and catch potential errors
    try:
        data = response.json()
    except json.JSONDecodeError:
        print("\n2. ERROR: Could not decode JSON. The response body is likely empty or not valid JSON.")
        print(f"   Response Text: {response.text}")
        data = None

    # --- Print Detailed Analysis of the Response ---
    print("\n--- Analysis of Response ---")
    print(f"3. Is the parsed data None?       : {data is None}")
    print(f"4. What is the type of the data? : {type(data)}")

    if isinstance(data, dict):
        print(f"5. Keys found in the data        : {list(data.keys())}")
        
        # Check for the 'links' key and the nested 'next' link
        links = data.get("links")
        print(f"6. Is the 'links' key present?   : {'Yes' if links else 'No'}")
        
        if links:
            next_link = links.get("next")
            print(f"7. Value of the 'next' link    : {next_link}")
        else:
            print("7. Value of the 'next' link    : N/A (because 'links' key is missing)")
            
        # Pretty-print the full JSON response for manual inspection
        print("\n--- Full JSON Response (first page) ---")
        print(json.dumps(data, indent=2))
        
    elif data is not None:
        print("\n--- Full Response (not a dictionary) ---")
        print(data)

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    print(f"Response content: {response.text}")
except Exception as err:
    print(f"An other error occurred: {err}")