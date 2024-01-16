import os
import requests
from bs4 import BeautifulSoup
from logger import success, error
from urllib.parse import urlparse


class AssertDownloader:
    def __init__(self, html, url):
        self.html = html
        self.url = url

    def parse(self):
        soup = BeautifulSoup(self.html, "html.parser")

        # htmlを解析し、<link>タグと<img>タグ,<script>タグのsrc/href属性を抽出
        resources_links = (
            [link.get("href") for link in soup.find_all("link")]
            + [img.get("src") for img in soup.find_all("img")]
            + [img.get("srcset") for img in soup.find_all("img")]
            + [script.get("src") for script in soup.find_all("script")]
            # FIXME: background-imageなどCSSやJavaScriptの中身は解析できない
        )

        resources_links = [link for link in resources_links if link]

        # 相対パスのリソースURLを絶対パスに変換
        # FIXME: 別ドメインの場合どうするか考えられていない
        self.links = []
        self.external_domains = []
        for link in resources_links:
            if link.startswith("data:"):
                continue
            if " " in link:
                link = link.split(" ")[0]
            if link.startswith("http://") or link.startswith("https://"):
                self.external_domains.append(f"{urlparse(link).scheme}://{urlparse(link).netloc}")
                self.links.append(link)
            else:
                self.links.append(requests.compat.urljoin(self.url, link))

    def url2filename(self, url):
        parsed = urlparse(url)
        return "/".join(parsed.path[1:].split("/")[:-1]), parsed.path.split("/")[-1]

    def replace_external_domains(self, html):
        for domain in self.external_domains:
            html = html.replace(domain, f"/{urlparse(domain).netloc}")
        return html

    def download_files(self, dirpath):
        if os.path.exists(dirpath) == False:
            os.mkdir(dirpath)
        for url in self.links:
            dirname, filename = self.url2filename(url)
            try:
                if os.path.exists(os.path.join(dirpath, dirname)) == False:
                    os.makedirs(os.path.join(dirpath, dirname))
                if url.startswith("https://") or url.startswith("http://"):
                    if os.path.exists(os.path.join(dirpath, urlparse(url).netloc, dirname)) == False:
                        os.makedirs(os.path.join(dirpath, urlparse(url).netloc, dirname))
                    filepath = os.path.join(dirpath, urlparse(url).netloc, dirname, filename)
                else:
                    filepath = os.path.join(dirpath, dirname, filename)
                with requests.get(url, stream=True) as r:
                    r.raise_for_status()
                    with open(filepath, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                success(f"Saved {filename} -> {filepath}")
            except Exception as e:
                error(e)
