from flask import Flask, request, send_file
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os
import base64
import asyncio
from service import summarise, STATUS_COMPLETED, STATUS_PENDING, STATUS_FAILED, pdf_file, image_file, render_link
from urllib.parse import unquote

app = Flask(__name__)
uri = os.getenv("MONGO_DB_URL")
client = MongoClient(uri)
db = client['hackillinois']['requests']

print("dropping all rows...")
db.drop()

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

    k = str(url.split('.'))
    if k[-1] == 'pdf':
        pdf_file(url)
    elif k[-1] in ['jpeg', 'jpg', 'png', 'tiff']:
        image_file(url)

    encoded_bytes = base64.b64encode(url.encode('utf-8')).decode('utf-8')
    filename = os.path.join(DATA_DIRECTORY, encoded_bytes)

    with open(filename, "w") as f:
        f.write(request.data.decode("utf-8"))

    print("saved input data to file: ", filename)

    data = summarise(db, url, filename)
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

    data = db.find_one({"url": url})
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


@app.route('/summarise_link', methods=['POST'])
def POST_summarise_link():
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

    print("looking for url in database...")
    query_result = db.find_one({"url": url})

    # process pdf/image/html to generate input file as plain text
    if query_result is None:
        db.insert_one({
            "url": url,
            "timestamp": datetime.now(),
            "status": STATUS_PENDING,
            "input_file": filename,
            "output_file": filename + "_out",
        })

        k = str(url.split('.'))
        if k[-1] == 'pdf':
            pdf_file(url, filename)
        elif k[-1] in ['jpeg', 'jpg', 'png', 'tiff']:
            image_file(url, filename, k[-1])
        else:
            pid = os.fork()
            if pid == 0:
                asyncio.get_event_loop().run_until_complete(render_link(db, url, filename))
                exit(0)
            else:
                os.wait()

    print("summarising input text...")
    data = summarise(db, url, filename)
    if data["status"] == STATUS_COMPLETED:
        print("output file already exists!")
        return send_file(data["output_file"])

    print("output file is in progress")
    return RESPONSE_PENDING, RESPONSE_PENDING_CODE


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6969, debug=True)
