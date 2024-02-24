from datetime import datetime, timedelta
from llm_query.prompts import terms_conditions
from llm_query.gpt_query import *
import threading
import urllib.request
import base64
from pymongo import MongoClient

# check db if entry for url exists,
# if exists, send row as json
# else, create row and start llm process in background.
# also, return row as json

def function_caller(db, url):
    query_engine = LLM_query()
    query_engine.request(db, url)

def pdf_file(url):
    response = urllib.request.urlopen(url)
    file = open("./data/document.pdf", 'wb')
    file.write(response.read())
    file.close()
    print("PDF save Completed")
    encoded_bytes = base64.b64encode(url.encode('utf-8')).decode('utf-8')
    os.system("pdftotext ./data/document.pdf ./data/"+encoded_bytes[:20])

def image_file(url):
    response = urllib.request.urlopen(url)
    file = open("./data/image.jpeg", 'wb')
    file.write(response.read())
    file.close()
    print("Image save Completed")
    encoded_bytes = base64.b64encode(url.encode('utf-8')).decode('utf-8')[:20]
    os.system("tesseract ./data/image.jpeg ./data/"+encoded_bytes)
    os.rename('./data/'+encoded_bytes+'.txt','./data/'+encoded_bytes)


def summarise(db, url, input_file_name):
    # get the results in db if any
    query_result = db.find_one({"url": url})
    if query_result != None:
        # validate if the file is a day old
        if query_result["timestamp"] >= datetime.now() - timedelta(days=1):
            status = query_result["status"]
            output_file = query_result["output_file"]
            return {"status": status, "output_file": output_file}
        else:
            result = db.update_one({"url": url}, {"$set": {"timestamp": datetime.now(), "status": "pending", "output_file": ""}})
            threading.Thread(target=function_caller, args=[db, url]).start()
            return {"status": "pending", "output_file": ''}    

    new_row = {
        "url": url,
        "timestamp": datetime.now(),
        "status": "progress",
        "input_file": input_file_name,
        "output_file": "",
    }
    insert_result = db.insert_one(new_row)
    threading.Thread(target=function_caller, args=[db, url]).start()
    return {"status": "pending", "output_file": ''}    

# return db entry if exists, or None


def get_summary(db, url):
    pass

if __name__ == "__main__":
    image_file("https://www.lifewire.com/thmb/lWlCQDkZkvbWxKhkJZ6yjOJ_J4k=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/ScreenShot2020-04-20at10.03.23AM-d55387c4422940be9a4f353182bd778c.jpg")