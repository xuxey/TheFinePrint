from datetime import datetime, timedelta
from llm_query.prompts import terms_conditions
from llm_query.gpt_query import *
import threading
import urllib.request
import base64
import os

STATUS_PENDING = "pending"
STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"


def function_caller(db, url):
    k = str(url.split('.'))
    if k[-2] == 'pdf':
        pdf_file(url)
    elif k[-2] in ['jpeg','jpg','png','tiff']:
        image_file(url)
    try:
        query_result = db.find_one({"url": url})
        input_file = query_result["input_file"]
        output_file = input_file + "_out"

        query_engine = LLM_query()
        query_engine.request(input_file, output_file)

        db.update_one({"url": url}, {"$set": {"status": STATUS_COMPLETED, "output_file": output_file}})
        print(f"completed summary for url: {url}")

    except Exception as e:
        print(f"failed to get summary for url: {url}: {e}")
        result = db.update_one({"url": url}, { "$set": {"status": STATUS_FAILED}})

def pdf_file(url):
    response = urllib.request.urlopen(url)
    encoded_bytes = base64.b64encode(url.encode('utf-8')).decode('utf-8')
    file = open("./data/" + encoded_bytes[:50] +".pdf", 'wb')
    file.write(response.read())
    file.close()
    print("PDF save Completed")
    os.system("pdftotext ./data/" + encoded_bytes[:50] +".pdf ./data/"+encoded_bytes)


def image_file(url):
    response = urllib.request.urlopen(url)
    encoded_bytes = base64.b64encode(url.encode('utf-8')).decode('utf-8')
    file = open("./data/" + encoded_bytes[:50] +".jpeg", 'wb')
    file.write(response.read())
    file.close()
    print("Image save Completed")
    os.system("tesseract ./data/" + encoded_bytes[:50] +".jpeg ./data/"+encoded_bytes)
    os.rename('./data/'+encoded_bytes+'.txt','./data/'+encoded_bytes)

def summarise(db, url, input_file_name):
    query_result = db.find_one({"url": url})

    if query_result is not None:
        # validate if the file is a day old
        if query_result["timestamp"] >= datetime.now() - timedelta(days=1):
            return query_result
        else:
            result = db.update_one({"url": url}, {"$set": {"timestamp": datetime.now(), "status": STATUS_PENDING, "output_file": ""}})
            # generate summary in background thread
            threading.Thread(target=function_caller, args=[db, url]).start()
            return query_result
    else:
        new_row = {
            "url": url,
            "timestamp": datetime.now(),
            "status": STATUS_PENDING,
            "input_file": input_file_name,
            "output_file": "",
        }
        insert_result = db.insert_one(new_row)
        threading.Thread(target=function_caller, args=[db, url]).start()
        return new_row


if __name__ == "__main__":
    image_file("https://www.lifewire.com/thmb/lWlCQDkZkvbWxKhkJZ6yjOJ_J4k=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/ScreenShot2020-04-20at10.03.23AM-d55387c4422940be9a4f353182bd778c.jpg")
    pdf_file("https://saurabhg.web.illinois.edu/teaching/ece549/sp2024/slides/lec02_perspective.pdf")
