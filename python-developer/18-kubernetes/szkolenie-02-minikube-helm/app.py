from flask import Flask, jsonify
import socket

app = Flask(__name__)


@app.route("/")
def index():
    # Zwracamy hostname – przydatne do weryfikacji load balancingu
    return jsonify({
        "wiadomosc": "Witaj z Kubernetes!",
        "hostname": socket.gethostname(),
        "status": "ok"
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
