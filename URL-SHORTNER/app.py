from flask import Flask, jsonify, redirect, request

import shortener as sh

app = Flask(__name__)


@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json(silent=True)

    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' in request body"}), 400

    url = data["url"].strip()
    if not url:
        return jsonify({"error": "'url' must not be empty"}), 400

    code = sh.shorten(url)
    return jsonify({"code": code, "short_url": f"/{code}"}), 200


@app.route("/<code>", methods=["GET"])
def redirect_to_url(code):
    original = sh.resolve(code)
    if original is None:
        return jsonify({"error": "Short code not found"}), 404
    return redirect(original, code=302)


if __name__ == "__main__":
    app.run(debug=True)