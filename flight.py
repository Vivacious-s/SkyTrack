import requests
import mysql.connector

# Replace with your actual MySQL credentials
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Hello@15byMNHV",
    "database": "flights_data"
}

# API Key (Replace with your actual key)
API_KEY = "5b580bdca7c7ca7a6cc1143d8c3305d1"
API_URL = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}"

# Connect to MySQL
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Fetch data from the API
response = requests.get(API_URL)

if response.status_code == 200:
    data = response.json()
    flights = data.get("data", [])

    if flights:
        for flight in flights:
            flight_number = flight["flight"]["iata"] if flight["flight"] else "N/A"
            airline = flight["airline"]["name"] if flight["airline"] else "N/A"
            departure_airport = flight["departure"]["airport"] if flight["departure"] else "N/A"
            arrival_airport = flight["arrival"]["airport"] if flight["arrival"] else "N/A"
            departure_time = flight["departure"]["estimated"] if flight["departure"] else None
            arrival_time = flight["arrival"]["estimated"] if flight["arrival"] else None
            status = flight["flight_status"]

            # Insert flight data into MySQL (if not exists, update status)
            sql = """
                INSERT INTO flights (flight_number, airline, departure_airport, arrival_airport, departure_time, arrival_time, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE status = VALUES(status), last_updated = CURRENT_TIMESTAMP;
            """
            values = (flight_number, airline, departure_airport, arrival_airport, departure_time, arrival_time, status)

            cursor.execute(sql, values)
        
        conn.commit()  # Save changes to the database
        print("Flight data stored/updated in MySQL.")
    else:
        print("No flight data found.")
else:
    print(f"Error fetching flight data: {response.status_code}")

# Close connection
cursor.close()
conn.close()
