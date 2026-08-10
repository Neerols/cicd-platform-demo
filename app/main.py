import os
from flask import Flask, jsonify

app = Flask(__name__)

APP_VERSION = os.environ.get("APP_VERSION", "dev")


@app.route("/")
def index():
    return jsonify(message="cicd-platform-demo is running", version=APP_VERSION)


@app.route("/health")
def health():
    return jsonify(status="ok"), 200


@app.route("/version")
def version():
    return jsonify(version=APP_VERSION)


@app.route("/fail")
def fail():
    # Endpoint used intentionally to test rollback / failed deploy scenarios
    return jsonify(status="error"), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
