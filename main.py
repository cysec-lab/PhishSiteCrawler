import os
import csv
from logger import info
from save_resource import AssertDownloader
from Driver import Driver

def load_dataset(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        return [row[1] for row in reader][1:]

if __name__ == "__main__":
    if os.path.exists("out") == False:
        os.mkdir("out")
    
    dataset_path = "phishurls.csv"
    urls = load_dataset(dataset_path)
    urls_len = len(urls)
    
    driver = Driver()
    for idx, url in enumerate(urls):
        info(f"({idx}/{urls_len}) Start scraping {url}")
        html = driver.get_html(url)
        if html == "":
            continue
        dirpath = os.path.join("out", driver.url2domain(url))

        downloader = AssertDownloader(html, url)
        downloader.parse()
        html = downloader.replace_external_domains(html)
        downloader.download_files(dirpath)
        
        driver.save(dirpath, "index.html", html)
        driver.save_meta(dirpath, url)
        driver.screen_shot(dirpath)

        info(f"Finish scraping {url}")
    driver.__exit__()

