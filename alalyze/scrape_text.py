from bs4 import BeautifulSoup
import glob
from tqdm import tqdm

def scrape_text(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    text = soup.get_text()
    return text

def load_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def file_append(path, content):
    with open(path, "a", encoding="utf-8") as f:
        f.write(content)
        
def file_save(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    filePath = "scraped_text.txt"
    with open(filePath, "w", encoding="utf-8") as f:
        f.write("")
    
    paths = glob.glob("out/**/*.html")
    print("file:", len(paths))
    
    count = 0
    text = ""
    
    for path in tqdm(paths):
        html = load_file(path)
        text += f"{scrape_text(html)}\n"
        count += 1
        if count % 300 == 0 or count == len(paths):
            file_append(filePath, text)
            text = ""
    
    text = load_file(filePath)
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    while "  " in text:
        text = text.replace("  ", " ")
        
    text = text.replace("\n", " ").strip()
    
    file_save(filePath, text)