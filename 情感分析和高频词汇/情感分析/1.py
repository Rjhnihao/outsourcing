from docx import Document
import csv
import collections
from textblob import TextBlob

# 读取上传的 Word 文档
doc_path = '分析情感倾向.docx'
doc = Document(doc_path)

# 提取文档中的所有标题文本
titles = [paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip() != '']

# 进行情感分析
rows = []
sentiment_counts = collections.Counter()
for title in titles:
    blob = TextBlob(title)
    sentiment = blob.sentiment.polarity
    category = '积极' if sentiment > 0 else '消极' if sentiment < 0 else '中性'
    sentiment_counts[category] += 1
    rows.append([title.strip(), category])


csv_file_path = '情感分析.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['标题', '情感'])
    writer.writerows(rows)

print(f'积极的标题: {sentiment_counts["积极"]}')
print(f'消极的标题: {sentiment_counts["消极"]}')
print(f'中性的标题: {sentiment_counts["中性"]}')

