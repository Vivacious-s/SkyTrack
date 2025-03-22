from flask import Flask, jsonify, request
import requests
import csv
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)  # Initialize Swagger

API_KEY = "5b580bdca7c7ca7a6cc1143d8c3305d1"

def fetch_flight_data():
    """Fetch flight data from the API."""
    API_URL = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}"
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        return {"error": f"Error fetching flight data: {response.status_code}"}

@app.route("/flights", methods=["GET"])
def get_flights():
    """
    Fetch flight data with optional filtering.
    ---
    parameters:
      - name: airline
        in: query
        type: string
        required: false
        description: Filter by airline name.
      - name: departure_time
        in: query
        type: string
        required: false
        description: Filter by departure time.
      - name: departure_airport
        in: query
        type: string
        required: false
        description: Filter by departure airport.
      - name: arrival_time
        in: query
        type: string
        required: false
        description: Filter by arrival time.
      - name: arrival_airport
        in: query
        type: string
        required: false
        description: Filter by arrival airport.
      - name: delay
        in: query
        type: string
        required: false
        description: Filter by delay.
    responses:
      200:
        description: A list of filtered flight data.
    """
    airline = request.args.get("airline")
    departure_time = request.args.get("departure_time")
    departure_airport = request.args.get("departure_airport")
    arrival_time = request.args.get("arrival_time")
    arrival_airport = request.args.get("arrival_airport")
    delay = request.args.get("delay")

    flights = fetch_flight_data()

    filtered_flights = [
        flight for flight in flights
        if (not airline or flight.get("airline", {}).get("name") == airline) and
           (not departure_time or flight.get("departure", {}).get("estimated") == departure_time) and
           (not departure_airport or flight.get("departure", {}).get("airport") == departure_airport) and
           (not arrival_time or flight.get("arrival", {}).get("estimated") == arrival_time) and
           (not arrival_airport or flight.get("arrival", {}).get("airport") == arrival_airport) and
           (not delay or str(flight.get("departure", {}).get("delay")) == delay)
    ]

    return jsonify(filtered_flights)

if __name__ == "__main__":
    app.run(debug=True)
    
