from flask import Flask, jsonify
from flask_cors import CORS
from advisary import get_advisory_data

app = Flask(__name__)
CORS(app)  # allows frontend (HTML/JS) to access API


@app.route("/api/advisory/<commodity>", methods=["GET"])
def advisory(commodity):
    try:
        data = get_advisory_data(commodity)
        return jsonify(data)
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


@app.route("/")
def home():
    return jsonify({
        "status": "APMC Price Advisory API is running",
        "usage": "/api/advisory/<commodity>"
    })


if __name__ == "__main__":
    app.run(debug=True)
