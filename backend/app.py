from flask import Flask, request, send_file
from flask_cors import CORS
from pymongo import MongoClient
import os
import base64
from service import summarise, STATUS_COMPLETED, STATUS_PENDING, STATUS_FAILED
from urllib.parse import unquote

app = Flask(__name__)
uri = os.getenv("MONGO_DB_URL")
client = MongoClient(uri)
db = client['hackillinois']
db_requests = db['requests']

print("dropping all rows...")
db_requests.drop()

CORS(app, resources={r"*": {"origins": "*"}})

VALID_ACCESS_CODES = ['access_code1', 'access_code2', 'access_code3']

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
print("cleaning data directory...")
os.system("rm -rf data && mkdir -p data")


@app.route("/", methods=["GET"])
def GET_index():
    return "hello", 200


@app.route('/summarise', methods=['POST'])
def POST_summarise():
    access_code = request.args.get("access_code")
    url = request.args.get("url")

    if not access_code or not url:
        print("the access code or url is missing")
        return RESPONSE_INVALID, RESPONSE_INVALID_CODE

    if access_code not in VALID_ACCESS_CODES:
        print("the access code is invalid")
        return RESPONSE_UNAUTHORIZED, REPONSE_UNAUTHORIZED_CODE

    url = unquote(url)
    print("decoded url: ", url)

    encoded_bytes = base64.b64encode(url.encode('utf-8')).decode('utf-8')
    filename = os.path.join(DATA_DIRECTORY, encoded_bytes)

    with open(filename, "w") as f:
        f.write(request.data.decode("utf-8"))

    print("saved input data to file: ", filename)

    data = summarise(db_requests, url, filename)
    if data["status"] == STATUS_COMPLETED:
        print("output file already exists!")
        return send_file(data["output_file"])

    print("output file is in progress")
    return RESPONSE_PENDING, RESPONSE_PENDING_CODE


@app.route('/summary', methods=['GET'])
def GET_summary():
    access_code = request.args.get("access_code")
    url = request.args.get("url")

    if not access_code or not url:
        print("the access code or url is missing")
        return RESPONSE_INVALID, RESPONSE_INVALID_CODE

    if access_code not in VALID_ACCESS_CODES:
        print("the access code is invalid")
        return RESPONSE_UNAUTHORIZED, REPONSE_UNAUTHORIZED_CODE

    data = db_requests.find_one({"url": url})
    print("db result: ", data)

    if not data:
        print("url does not exist in database...")
        return RESPONSE_UNAVAILABLE, RESPONSE_UNAVAILABLE_CODE

    if data["status"] == STATUS_PENDING:
        print("the output is still in progress!")
        return RESPONSE_PENDING, RESPONSE_PENDING_CODE

    if data["status"] == STATUS_FAILED:
        print("failure")
        return "failed to get summary", 500

    if data["status"] == STATUS_COMPLETED:
        print("success")
        return send_file(data["output_file"])

    print("unknown status for url:", url, data["status"])
    return "", 500


if __name__ == '__main__':
    app.run(debug=True)
