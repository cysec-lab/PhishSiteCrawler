import collections
import re

def load_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()
    

if __name__ == "__main__":
    filePath = "scraped_text.txt"
    text = load_file(filePath).lower()
    text = text.split(" ")
    
    c = collections.Counter(text)
    
    csv = "word,count\n"
    for word, count in c.most_common():
        if(len(word) > 3) and re.match(r"^[a-zA-Z]*$", word):
            csv += f"{word},{count}\n"
    
    with open("word_count.csv", "w", encoding="utf-8") as f:
        f.write(csv)