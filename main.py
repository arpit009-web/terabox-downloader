from fastapi import FastAPI
from fastapi.responses import JSONResponse
from playwright.sync_api import sync_playwright
import re

app = FastAPI()

@app.get("/download")
def get_terabox_link(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=60000)
            page.wait_for_timeout(5000)
            html = page.content()
            browser.close()

            match = re.search(r'https:\\/\\/.*?terabox.*?\\.mp4.*?"', html)
            if match:
                raw_url = match.group(0).strip('"')
                direct_link = raw_url.replace('\\/', '/')
                return JSONResponse({"download_url": direct_link})
            else:
                return JSONResponse({"error": "Video link not found"}, status_code=404)

        except Exception as e:
            browser.close()
            return JSONResponse({"error": str(e)}, status_code=500)
