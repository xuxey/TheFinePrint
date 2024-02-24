import asyncio
import os
from pyppeteer import launch
import subprocess
import time
from pymongo import MongoClient
uri = os.getenv("MONGO_DB_URL")
client = MongoClient(uri)
db = client['hackillinois']
db_requests = db['requests']


async def render_link(url, filename):
    browser = await launch()
    page = await browser.newPage()
    url = "https://www.facebook.com/privacy/policy"
    await page.goto(url)
    time.sleep(4)

    content = await page.evaluate("document.body.innerText", force_expr=True)
    print(content)

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
