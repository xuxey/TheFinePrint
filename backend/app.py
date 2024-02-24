from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)
uri = os.getenv("MONGO_DB_URL")
client = MongoClient(uri)
db = client['hackillinois']
collection = db['requests']

# List of valid access codes
VALID_ACCESS_CODES = ['access_code1', 'access_code2', 'access_code3']


@app.route('/summarise', methods=['POST'])
def summarise():
    data = request.json
    access_code = data.get('access_code')
    url = data.get('url')

    if not access_code or not url:
        return jsonify({'error': 'Missing required parameters.'}), 400

    if access_code not in VALID_ACCESS_CODES:
        return jsonify({'error': 'Unauthorized'}), 401

    # Your summarization logic here

    return jsonify({'message': 'Summarization successful'}), 200


@app.route('/summary', methods=['GET'])
def summary():
    access_code = request.args.get('access_code')
    url = request.args.get('url')

    if not access_code or not url:
        return jsonify({'error': 'Missing required parameters.'}), 400

    if access_code not in VALID_ACCESS_CODES:
        return jsonify({'error': 'Unauthorized'}), 401

    # Your logic to retrieve summary from MongoDB based on URL and access_code

    return jsonify({'summary': 'Your summary content'}), 200


if __name__ == '__main__':
    app.run(debug=True)
