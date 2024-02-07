from docx import Document
from collections import Counter
import re
import csv

def tokenize(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return words

doc_path = '分析高频词汇.docx'
doc = Document(doc_path)

text_content = ''
for paragraph in doc.paragraphs:
    text_content += paragraph.text + '\n'

words = tokenize(text_content)
word_counts = Counter(words)
top_100_words = word_counts.most_common(100)
csv_data = [["序号", "词", "频数"]] + [[idx + 1, word, count] for idx, (word, count) in enumerate(top_100_words)]
csv_file_path = '词频统计.csv'

with open(csv_file_path, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerows(csv_data)

