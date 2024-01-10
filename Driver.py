from selenium import webdriver
import os
import json
import datetime
from logger import success, error
from urllib.parse import urlparse


class Driver:
    def __init__(self):
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Remote(
            command_executor=os.environ["SELENIUM_URL"],
            options=options,
        )
        self.driver.set_page_load_timeout(3)

    def __exit__(self):
        self.driver.quit()

    def url2domain(self, url):
        parsed = urlparse(url)
        return parsed.netloc

    def get_html(self, url):
        try:
            self.driver.get(url)
            return self.driver.page_source
        except Exception as e:
            error(e)
            error(f"{url} is not available.")
            return ""

    def save(self, dirpath, filepath, content):
        try:
            if os.path.exists(dirpath) == False:
                os.mkdir(dirpath)
            with open(os.path.join(dirpath, filepath), "w", encoding="utf-8") as f:
                f.write(content)
            success(f"Saved {filepath} -> {os.path.join(dirpath, filepath)}")
        except Exception as e:
            error(e)

    def save_meta(self, dirpath, url):
        metadir = os.path.join(dirpath, ".metainfo")
        if os.path.exists(metadir) == False:
            os.mkdir(metadir)
        with open(os.path.join(metadir, "meta.json"), "w", encoding="utf-8") as f:
            meta = {"url": url, "date": datetime.datetime.now().isoformat()}
            json.dump(meta, f, indent=2)
        success(f"Saved meta.json -> {os.path.join(metadir, 'meta.json')}")

    def screen_shot(self, dirpath):
        metadir = os.path.join(dirpath, ".metainfo")
        if os.path.exists(metadir) == False:
            os.mkdir(metadir)
        try:
            self.driver.save_screenshot(os.path.join(metadir, "screen_shot.png"))
            success(
                f"Saved screen_shot.png -> {os.path.join(metadir, 'screen_shot.png')}"
            )
        except Exception as e:
            error(e)