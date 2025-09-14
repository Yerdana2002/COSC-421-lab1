import csv
import pandas as pd

# now I will clean csv file and only include airports from the dataset
"""
filename = 'flightnetwork.csv'

with open(filename, mode='r', newline='') as file:
    reader = csv.reader(file)
    filtered_rows = []
    seen = set()  # To track unique (airport1, airport2) pairs

    for row in reader:
        airport1, airport2 = row
        if airport1.startswith('C') and airport2.startswith('C'):
            pair = (airport1, airport2)
            if pair not in seen:
                seen.add(pair)
                filtered_rows.append(row)

"""


# --- Configuration ---
# Set the names of your input and output files here
allowed_airports_file = '/Users/yerdanamaulenbay/Documents/COSC 421/canadian_airports.csv' # Your file with columns: city,code (e.g., Toronto,YYZ)
all_routes_file = 'flightnetwork.csv'           # Your file with columns: airport1,airport2 (e.g., CYLW,CYQQ)
output_file = 'filtered_routes.csv'          # The name of the file to save the results to

# --- Script Logic ---
try:
    # 1. Read the two CSV files into pandas DataFrames
    allowed_df = pd.read_csv(allowed_airports_file)
    routes_df = pd.read_csv(all_routes_file)

    # 2. Create a set of the allowed 3-letter airport codes for fast lookups
    # A set is much more efficient for checking if a value exists than a list.
    allowed_codes = set(allowed_df['code'])

    # 3. Filter the routes DataFrame
    # This keeps a row only if the last 3 letters of BOTH airport1 AND airport2
    # are present in the 'allowed_codes' set.
    filtered_routes_df = routes_df[
        routes_df['airport1'].str[-3:].isin(allowed_codes) &
        routes_df['airport2'].str[-3:].isin(allowed_codes)
    ].copy() # .copy() is used to avoid a SettingWithCopyWarning

    # 4. Save the filtered DataFrame to a new CSV file
    # index=False prevents pandas from writing the DataFrame index as a column
    filtered_routes_df.to_csv(output_file, index=False)

    print(f"✅ Success! Filtered data has been saved to '{output_file}'")
    print("\n--- Filtered Routes ---")
    print(filtered_routes_df)

except FileNotFoundError as e:
    print(f"❌ Error: Could not find the file '{e.filename}'. Please make sure it's in the same directory as the script.")
except KeyError as e:
    print(f"❌ Error: A required column {e} was not found in one of your CSV files. Please check the column names.")