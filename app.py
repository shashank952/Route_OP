from flask import Flask, request, jsonify, render_template
from route import calculate_route_with_alternatives, places

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", places=places)

@app.route("/optimize", methods=["POST"])
def optimize():
    data = request.json or {}

    source = data.get("source")
    destination = data.get("destination")
    passengers = int(data.get("passengers", 1))
    fuel_available = int(data.get("fuel_available", 0))
    mileage = float(data.get("mileage", -1))
    vehicle_type = data.get("vehicle_type", "Car")

    result = calculate_route_with_alternatives(
        source,
        destination,
        passengers,
        fuel_available,
        mileage,
        vehicle_type
    )

    # If result is an error dict, return it directly
    if isinstance(result, dict) and result.get("error"):
        return jsonify(result)

    # Otherwise return list of routes under "routes"
    return jsonify({"routes": result})

if __name__ == "__main__":
    app.run(debug=True)
