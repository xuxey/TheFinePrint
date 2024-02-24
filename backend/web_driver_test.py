import asyncio
from pyppeteer import launch
import time


async def main():
    browser = await launch()
    page = await browser.newPage()
    url = "https://www.facebook.com/privacy/policy"
    await page.goto(url)
    time.sleep(4)

    content = await page.evaluate("document.body.innerText", force_expr=True)
    print(content)

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
