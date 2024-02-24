from datetime import datetime, timedelta
from llm_query.prompts import terms_conditions
import llm_query.gpt_query
import threading
from pymongo import MongoClient

# check db if entry for url exists,
# if exists, send row as json
# else, create row and start llm process in background.
# also, return row as json

def summarise(db, url, input_file_name):

    query_result = db.find_one({"url": url})
    if query_result != None:
        if query_result["timestamp"] < datetime.now() - timedelta(days=1):
            status = query_result["status"]
            output_file = query_result["output_file"]
            return {"status":status, "output_file":output_file}
        else:
            result = db.update_one({"url": url}, {"$set" : {"timestamp":datetime.now(), "status":"pending"}})
            return { "status" : "pending", "output_file":'out_' + input_file_name }
    
    new_row = {
        "url": url,
        "timestamp":datetime.now(),
        "status":"progress",
        "input_file" : input_file_name,
        "output_file": 'out_' + input_file_name,
        }
    insert_result = db.insert_one(new_row)

    query_engine = llm_query.gpt_query()
    background_thread_for_query = threading.Thread(target=query_engine.request(db,url))

    return { "status" : "pending", "output_file":'' }

# return db entry if exists, or None
def get_summary(db, url):
    pass