from flask import Flask, request, send_file
from flask_cors import CORS
from pymongo import MongoClient
import os
import base64
from service import summarise

app = Flask(__name__)
uri = os.getenv("MONGO_DB_URL")
client = MongoClient(uri)
db = client['hackillinois']
db_requests = db['requests']

CORS(app, resources={r"*": {"origins": "*"}})

VALID_ACCESS_CODES = ['access_code1', 'access_code2', 'access_code3']

STATUS_PENDING = "pending"
STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"

RESPONSE_OK = ""
RESPONSE_PENDING = "In progress"
RESPONSE_UNAUTHORIZED = "wrong access code"
RESPONSE_UNAVAILABLE = "summary does not exist"
RESPONSE_INVALID = "request param is missing"

RESPONSE_OK_CODE = 200
RESPONSE_PENDING_CODE = 201
REPONSE_UNAUTHORIZED_CODE = 400
RESPONSE_UNAVAILABLE_CODE = 401
RESPONSE_INVALID_CODE = 405

DATA_DIRECTORY = "./data"


@app.route("/", methods=["GET"])
def GET_index():
    return "hello", 200


@app.route('/summarise', methods=['POST'])
def POST_summarise():
    access_code = request.args.get("access_code")
    url = request.args.get("url")

    if not access_code or not url:
        return RESPONSE_INVALID, RESPONSE_INVALID_CODE

    if access_code not in VALID_ACCESS_CODES:
        return RESPONSE_UNAUTHORIZED, REPONSE_UNAUTHORIZED_CODE

    encoded_bytes = base64.b64encode(url.encode('utf-8'))
    filename = os.path.join(DATA_DIRECTORY, encoded_bytes)
    f = open(filename, "w")
    f.write(request.content)

    data = summarise(db_requests, url, filename)
    if data["status"] == STATUS_COMPLETED:
        return send_file(data["output_file"]), RESPONSE_OK

    return RESPONSE_PENDING, RESPONSE_PENDING_CODE


@app.route('/summary', methods=['GET'])
def GET_summary():
    access_code = request.args.get("access_code")
    url = request.args.get("url")

    if not access_code or not url:
        return RESPONSE_INVALID, RESPONSE_INVALID_CODE

    if access_code not in VALID_ACCESS_CODES:
        return RESPONSE_UNAUTHORIZED, REPONSE_UNAUTHORIZED_CODE

    data = db_requests.find_one({"url": url})

    if not data:
        return RESPONSE_UNAVAILABLE, RESPONSE_UNAVAILABLE_CODE

    if data["status"] == STATUS_PENDING:
        return RESPONSE_PENDING, RESPONSE_PENDING_CODE

    elif data["status"] == STATUS_FAILED:
        # retry_summarise()
        # return RESPONSE_PENDING, RESPONSE_PENDING_CODE
        return "failed to get summary", 500

    elif data["status"] == STATUS_COMPLETED:
        return send_file(data["output_file"]), RESPONSE_OK

    print("unknown status for url:", url)
    return "", 500


if __name__ == '__main__':
    app.run(debug=True)
