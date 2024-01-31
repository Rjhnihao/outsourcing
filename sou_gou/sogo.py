import requests
import random
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import os
import threading
import queue

requests.adapters.DEFAULT_RETRIES = 5
folder_path = 'D:\pycharm\pycharm_project\sou_gou\导入文件夹'
ua = UserAgent()
num = 1
api_url = f"https://dps.kdlapi.com/api/getdps/?secret_id=o5u60m2gtx0085hwv72h&num={num}&signature=h1ikh9rtkzt9wo6wtyc6xmknvi8tza5v&pt=1&sep=1&format=json"
proxy_ip = requests.get(api_url).json()['data']['proxy_list']
username = "d4997483143"
password = "tap2a2bc"
url = 'https://www.sogou.com/web'
visited = set()

def get_initial_keywords(folder_path):
    all_files = os.listdir(folder_path)
    keywords_by_file = {}
    for file in all_files:
        if file.endswith('.txt'):
            with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as f:
                keywords = [line.strip() for line in f.readlines() if line.strip()]
                keywords_by_file[file] = keywords
    return keywords_by_file

def sogo(q2, lock, filename, keyword):
    thread_name = threading.current_thread().name
    next_keywords = []
    lock.acquire()
    if keyword in visited:
        lock.release()
        return
    visited.add(keyword)
    lock.release()
    for page in range(1, 6):
        turn = 0
        while turn <= 10:
            proxies = {
                "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {'user': username, 'pwd': password,
                                                                'proxy': random.choice(proxy_ip)},
                "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {'user': username, 'pwd': password,
                                                                 'proxy': random.choice(proxy_ip)}
            }
            params = {
                'query': keyword,
                'page': str(page),
                'ie': 'utf8'
            }
            headers = {
                'User-Agent': ua.random,
                'Connection': 'close'
            }

            try:
                response = requests.get(url=url, params=params, headers=headers, proxies=proxies ,timeout=20)
            except:
                turn += 1
                continue
            text = response.text
            soup = BeautifulSoup(text, 'lxml')
            table = soup.find('table', {'id': 'hint_container'})
            hint_div = soup.find('div', {'class': 'hint-mid'})

            if not table and not hint_div:
                turn += 1
                continue

            related_search_fields = []
            table_rows = table.find_all('tr') if table else []
            for row in table_rows:
                cells = row.find_all('td')
                for cell in cells:
                    anchor = cell.find('a')
                    if anchor:
                        related_search_fields.append(anchor.text)
                        next_keywords.append(anchor.text)

            everyone_searching_fields = []
            hint_spans = hint_div.find_all('span') if hint_div else []
            for span in hint_spans:
                anchor = span.find('a')
                if anchor:
                    everyone_searching_fields.append(anchor.text)
                    next_keywords.append(anchor.text)

            with open(f'D:\pycharm\pycharm_project\sou_gou\导出文件夹/{filename}', 'a', encoding='utf-8') as f:
                unique_everyone_search = list(set(everyone_searching_fields))
                for value in unique_everyone_search:
                    f.write(value + '\n')
                unique_relative_search = list(set(related_search_fields))
                for value in unique_relative_search:
                    f.write(value + '\n')
            lock.acquire()
            q2.put(next_keywords.copy())
            lock.release()
            break

if __name__ == "__main__":
    rounds = int(input("请输入联想轮数："))
    max_threads = 1000
    THREADS_PER_KEYWORD = 100
    keywords_by_file = get_initial_keywords(folder_path)

    for filename, initial_keywords in keywords_by_file.items():
        for _ in range(rounds):
            lock = threading.Lock()
            q2 = queue.Queue()
            threads = []
            for kw in initial_keywords:
                for _ in range(THREADS_PER_KEYWORD):
                    if len(threads) >= max_threads:
                        for t in threads:
                            t.join()
                        threads = []
                    t = threading.Thread(target=sogo, args=(q2, lock, filename, kw))
                    t.start()
                    threads.append(t)
            for t in threads:
                t.join()
            initial_keywords = []
            while not q2.empty():
                initial_keywords += q2.get()