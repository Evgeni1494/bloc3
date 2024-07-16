import requests
import pandas as pd
import sqlite3
import os

# Define your API key here
API_KEY = 'e0d45f151ed52f150d8c7554f340f027'

# Define the base URL for the OpenWeatherMap Geocoding API
BASE_URL = "http://api.openweathermap.org/geo/1.0/direct"

# Define the central cities and their corresponding state codes
state_info = {
    "Alabama": ("Birmingham", "AL"),
    "Alaska": ("Anchorage", "AK"),
    "Arizona": ("Phoenix", "AZ"),
    "Arkansas": ("Little Rock", "AR"),
    "California": ("Los Angeles", "CA"),
    "Colorado": ("Denver", "CO"),
    "Connecticut": ("Hartford", "CT"),
    "Delaware": ("Dover", "DE"),
    "District of Columbia": ("Washington", "DC"),
    "Florida": ("Miami", "FL"),
    "Georgia": ("Atlanta", "GA"),
    "Hawaii": ("Honolulu", "HI"),
    "Idaho": ("Boise", "ID"),
    "Illinois": ("Chicago", "IL"),
    "Indiana": ("Indianapolis", "IN"),
    "Iowa": ("Des Moines", "IA"),
    "Kansas": ("Wichita", "KS"),
    "Kentucky": ("Louisville", "KY"),
    "Louisiana": ("New Orleans", "LA"),
    "Maine": ("Portland", "ME"),
    "Maryland": ("Baltimore", "MD"),
    "Massachusetts": ("Boston", "MA"),
    "Michigan": ("Detroit", "MI"),
    "Minnesota": ("Minneapolis", "MN"),
    "Mississippi": ("Jackson", "MS"),
    "Missouri": ("Kansas City", "MO"),
    "Montana": ("Billings", "MT"),
    "Nebraska": ("Omaha", "NE"),
    "Nevada": ("Las Vegas", "NV"),
    "New Hampshire": ("Manchester", "NH"),
    "New Jersey": ("Newark", "NJ"),
    "New Mexico": ("Albuquerque", "NM"),
    "New York": ("New York", "NY"),
    "North Carolina": ("Charlotte", "NC"),
    "North Dakota": ("Fargo", "ND"),
    "Ohio": ("Columbus", "OH"),
    "Oklahoma": ("Oklahoma City", "OK"),
    "Oregon": ("Portland", "OR"),
    "Pennsylvania": ("Philadelphia", "PA"),
    "Rhode Island": ("Providence", "RI"),
    "South Carolina": ("Charleston", "SC"),
    "South Dakota": ("Sioux Falls", "SD"),
    "Tennessee": ("Nashville", "TN"),
    "Texas": ("Houston", "TX"),
    "Utah": ("Salt Lake City", "UT"),
    "Vermont": ("Burlington", "VT"),
    "Virginia": ("Richmond", "VA"),
    "Washington": ("Seattle", "WA"),
    "West Virginia": ("Charleston", "WV"),
    "Wisconsin": ("Milwaukee", "WI"),
    "Wyoming": ("Cheyenne", "WY"),
}

# Function to get latitude and longitude from OpenWeatherMap API
def get_lat_lon(city, state, country='US'):
    try:
        response = requests.get(BASE_URL, params={
            'q': f"{city},{state},{country}",
            'limit': 1,
            'appid': API_KEY
        })
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        if data:
            return data[0]['lat'], data[0]['lon']
    except requests.RequestException as e:
        print(f"Error fetching data for {city}, {state}: {e}")
    return None, None

# Read the CSV file
try:
    df = pd.read_csv('/home/utilisateur/Documents/Certification_IA/END_Project/bloc3/archive/emissions.csv')
except FileNotFoundError as e:
    print(f"CSV file not found: {e}")
    exit(1)
except pd.errors.EmptyDataError as e:
    print(f"CSV file is empty: {e}")
    exit(1)
except pd.errors.ParserError as e:
    print(f"Error parsing CSV file: {e}")
    exit(1)

# Create a dictionary to store latitude and longitude for each state
state_coordinates = {}

# Get latitude and longitude for each state
for state, (city, state_code) in state_info.items():
    lat, lon = get_lat_lon(city, state_code)
    state_coordinates[state] = (lat, lon)

# Add latitude and longitude to the dataframe
df['latitude'] = df['state-name'].map(lambda x: state_coordinates.get(x, (None, None))[0])
df['longitude'] = df['state-name'].map(lambda x: state_coordinates.get(x, (None, None))[1])

# Rename DataFrame columns to match the database table columns
df.rename(columns={
    'state-name': 'state_name',
    'sector-name': 'sector_name',
    'fuel-name': 'fuel_name'
}, inplace=True)

# Save the updated dataframe to a new CSV file
try:
    df.to_csv('combined_api_csv_data.csv', index=False)
except IOError as e:
    print(f"Error saving CSV file: {e}")
    exit(1)

# Create SQLite3 database and insert data
database_path = 'data_expo_bdd/exposition_database.db'
os.makedirs(os.path.dirname(database_path), exist_ok=True)  # Ensure the directory exists

try:
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    # Create table state
    c.execute('''
        CREATE TABLE IF NOT EXISTS state (
            state_name TEXT PRIMARY KEY,
            latitude REAL,
            longitude REAL
        )
    ''')
    # Create table emissions
    c.execute('''
        CREATE TABLE IF NOT EXISTS emissions (
            year INTEGER,
            state_name TEXT,
            sector_name TEXT,
            fuel_name TEXT,
            value REAL,
            latitude REAL,
            longitude REAL,
            FOREIGN KEY (state_name) REFERENCES state(state_name)
        )
    ''')
    # Insert state data into the table
    state_data = [{'state_name': k, 'latitude': v[0], 'longitude': v[1]} for k, v in state_coordinates.items()]
    state_df = pd.DataFrame(state_data)
    state_df.to_sql('state', conn, if_exists='append', index=False)
    # Insert emissions data into the table
    df.to_sql('emissions', conn, if_exists='append', index=False)
    # Commit and close the connection
    conn.commit()
    conn.close()
except sqlite3.Error as e:
    print(f"Error with SQLite database: {e}")
    exit(1)

print("Data has been updated and saved to the SQLite database.")
