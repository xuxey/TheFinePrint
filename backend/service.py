from datetime import datetime, timedelta
from llm_query.gpt_query import LLM_query
import threading
import urllib.request
import base64
import os

STATUS_PENDING = "pending"
STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"


def function_caller(db, url):
    k = str(url.split('.'))
    if k[-1] == 'pdf':
        pdf_file(url)
    elif k[-1] in ['jpeg', 'jpg', 'png', 'tiff']:
        image_file(url)
    try:
        query_result = db.find_one({"url": url})
        input_file = query_result["input_file"]
        output_file = input_file + "_out"

        query_engine = LLM_query()
        query_engine.request(input_file, output_file)

        db.update_one({"url": url}, {
                      "$set": {"status": STATUS_COMPLETED, "output_file": output_file}})
        print(f"completed summary for url: {url}")

    except Exception as e:
        print(f"failed to get summary for url: {url}: {e}")
        db.update_one(
            {"url": url}, {"$set": {"status": STATUS_FAILED}})


def pdf_file(url):
    response = urllib.request.urlopen(url)
    encoded_bytes = base64.b64encode(url.encode('utf-8')).decode('utf-8')
    pdf_file = os.path.join("data", encoded_bytes + ".pdf")
    text_file = os.path.join("data", encoded_bytes)
    with open(pdf_file, 'wb') as file:
        file.write(response.read())

    print("PDF save Completed")
    os.system(f"pdftotext {pdf_file} {text_file}")
    print("PDF to TEXT completed")


def image_file(url):
    response = urllib.request.urlopen(url)
    encoded_bytes = base64.b64encode(url.encode('utf-8')).decode('utf-8')

    image_file = os.path.join("data", encoded_bytes + ".jpeg")
    text_file = os.path.join("data", encoded_bytes)

    with open(image_file, 'wb') as file:
        file.write(response.read())

    print("Image save Completed")
    os.system(f"tesseract {image_file} {text_file}")
    os.system(f"mv {text_file}.txt {text_file}")
    print("Image to TEXT Completed")


def summarise(db, url, input_file_name):
    query_result = db.find_one({"url": url})

    if query_result is not None:
        # validate if the file is a day old
        if query_result["timestamp"] >= datetime.now() - timedelta(days=1):
            return query_result
        else:
            db.update_one({"url": url}, {"$set": {
                "timestamp": datetime.now(), "status": STATUS_PENDING, "output_file": ""}})
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
    image_file(
        "https://img.freepik.com/free-photo/painting-mountain-lake-with-mountain-background_188544-9126.jpg")
    pdf_file(
        "https://saurabhg.web.illinois.edu/teaching/ece549/sp2024/slides/lec02_perspective.pdf")
