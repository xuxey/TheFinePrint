from datetime import datetime, timedelta
from llm_query.gpt_query import LLM_query
import threading
import urllib.request
import os
import time
from pyppeteer import launch

STATUS_PENDING = "pending"
STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"


def function_caller(db, url):
    try:
        query_engine = LLM_query()
        query_result = db.find_one({"url": url})
        query_engine.request(
            query_result["input_file"], query_result["output_file"])

        db.update_one({"url": url}, {"$set": {"status": STATUS_COMPLETED}})
        print(f"completed summary for url: {url}")

    except Exception as e:
        print(f"failed to get summary for url: {url}: {e}")
        db.update_one(
            {"url": url}, {"$set": {"status": STATUS_FAILED}})


async def render_link(db, url, filename, timeout=4):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    time.sleep(timeout)

    content = await page.evaluate("document.body.innerText", force_expr=True)
    with open(filename, "w") as f:
        f.write(content)
        print(f"saved rendered text to file: {filename}")

    await browser.close()


def pdf_file(pdf_file, text_file):
    #response = urllib.request.urlopen(url)
    #pdf_file = text_file + ".pdf"

    os.system(f"pdftotext {pdf_file} {text_file}")
    print("PDF to TEXT completed")


def image_file(image_file, text_file):
    #response = urllib.request.urlopen(url)
    #image_file = text_file + ext

    print("Image save Completed")
    os.system(f"tesseract {image_file} {text_file}")
    os.system(f"mv {text_file}.txt {text_file}")
    print("Image to TEXT Completed")


def summarise(db, url, input_file_name):
    output_file_name = input_file_name + "_out"
    query_result = db.find_one({"url": url})

    if query_result is not None:
        print("found row for url: ", url, query_result)
        # validate if the file is a day old
        if query_result["status"] == STATUS_COMPLETED and query_result["timestamp"] >= datetime.now() - timedelta(days=1):
            return query_result
        else:
            db.update_one({"url": url}, {
                          "$set": {"timestamp": datetime.now(), "status": STATUS_PENDING}})
            # generate summary in background thread
            threading.Thread(target=function_caller, args=[db, url]).start()
            return query_result
    else:
        db.insert_one({
            "url": url,
            "timestamp": datetime.now(),
            "status": STATUS_PENDING,
            "input_file": input_file_name,
            "output_file": output_file_name
        })
        threading.Thread(target=function_caller, args=[db, url]).start()
        return db.find_one({"url": url})


if __name__ == "__main__":
    #image_file("https://www.lifewire.com/thmb/lWlCQDkZkvbWxKhkJZ6yjOJ_J4k=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/ScreenShot2020-04-20at10.03.23AM-d55387c4422940be9a4f353182bd778c.jpg")
    #image_file("https://img.freepik.com/free-photo/painting-mountain-lake-with-mountain-background_188544-9126.jpg")
    pdf_file("https://tmpfiles.org/4309934/skm_c450i17122309020.pdf",'greens')
