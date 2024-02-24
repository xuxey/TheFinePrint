from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# uri = f"mongodb+srv://{atlas_username}:{atlas_password}" \
#     "@cluster0.tq3ny.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

uri = os.getenv("MONGO_DB_URL")
client = MongoClient(uri)
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
