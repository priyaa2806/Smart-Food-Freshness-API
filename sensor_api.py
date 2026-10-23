
from flask import Flask, request, jsonify
from datetime import datetime, timezone

app = Flask(__name__)

latest_reading = None


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Smart Food Freshness Sensor API is running"
    })


@app.route("/receive_data", methods=["POST"])
def receive_data():
    global latest_reading

    data = request.form

    try:
        temperature = float(data["temp"])
        humidity = float(data["hum"])
        gas_raw = int(data["gas"])
        sensor_status = data.get("status", "UNKNOWN").upper()
    except (KeyError, ValueError):
        return jsonify({"error": "Invalid or missing sensor data"}), 400

    latest_reading = {
        "temperature": temperature,
        "humidity": humidity,
        "gas_raw": gas_raw,
        "sensor_status": sensor_status,
        "received_at": datetime.now(timezone.utc).isoformat()
    }

    print("Received sensor reading:", latest_reading)

    return jsonify({
        "message": "Sensor data received successfully",
        "data": latest_reading
    }), 200


@app.route("/latest", methods=["GET"])
def latest():
    if latest_reading is None:
        return jsonify({"message": "No sensor readings received yet"}), 404

    return jsonify(latest_reading)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
