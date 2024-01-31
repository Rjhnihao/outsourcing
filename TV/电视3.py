import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

URL = "https://www.4ksj.com/member.php?mod=logging&action=login"
driver = webdriver.Chrome()
driver.get(URL)
username_input = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.NAME, "username"))
)
username_input.send_keys("1071515307")
print("输入用户名成功")

password_input = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.NAME, "password"))
)
password_input.send_keys("1234567")
print("输入密码成功")

submit_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.NAME, "loginsubmit"))
)
submit_button.click()
print("点击登录按钮成功")

selenium_cookies = driver.get_cookies()
requests_session = requests.Session()
for cookie in selenium_cookies:
    requests_session.cookies.set(cookie['name'], cookie['value'])

try:
    manual_redirect_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "succeedmessage_href"))
    )
    manual_redirect_link.click()
    print("手动点击跳转链接")
except:
    print("手动跳转链接不存在，可能已经自动跳转")




base_url = "https://www.4ksj.com/forum-4kdianying-s7-{}.html"
for page_num in range(1, 10000):
    page_url = base_url.format(page_num)
    response = requests_session.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    a_tags = soup.find_all('div',{'class':'nex_cmo_name'})
    a_tags = [a for sublist in a_tags for a in sublist.find_all('a', {'target': '_blank'})]
    txt_mingzi=''
    jianjie=''
    cililianjie=''
    for a_tag in a_tags:
        if a_tag:
            a_tag.find_all('a',{'target':'_blank'})
            txt_mingzi=a_tag.get_text()
            link_url=a_tag['href']
            full_link_url = f"https://www.4ksj.com/{link_url}"
            print(txt_mingzi)
            print('链接：'+ full_link_url)
            driver.get(full_link_url)
            link_soup = BeautifulSoup(driver.page_source, 'html.parser')
            div_tag = link_soup.find('div', class_='nex_drama_intros') or link_soup.find('div', class_='nex_juji_intros')
            text_content = div_tag.text
            text_content = text_content.replace('简介', '', 1).strip() or text_content.replace('剧情简介', '', 1).strip()
            jianjie=text_content
            print(text_content)
            a_tag2s_mingzi=link_soup.find_all('div',{'class':'fileaq'})
            a_tag2s_link = link_soup.find_all('div',{'class':'down_2'})
            torrent_link =  [a for sublist in a_tag2s_link for a in sublist.find_all('a', {'target': '_blank'})]
            mingzi_list = [div.get_text().strip() for div in a_tag2s_mingzi]
            link_list = [a['href'] for a in torrent_link]
            if len(mingzi_list) != len(link_list):
                raise ValueError("两个列表的长度不同，无法配对。")
            result_dict = dict(zip(mingzi_list, link_list))

            td_tag = link_soup.find('td', {'class': 't_f'})

            for strong_tag in td_tag.find_all('strong'):
                text_content = strong_tag.get_text().split('【')[0].split('：')[-1].strip()
                next_sibling = strong_tag.find_next_sibling()

                if next_sibling and next_sibling.name == 'a' and 'magnet' in next_sibling['href']:
                    link_content = next_sibling['href']
                    match = re.match(r"(magnet:\?xt=urn:btih:[a-zA-Z0-9]+&dn)", link_content)
                    if match:
                        cililianjie = match.group(1)
                    result_dict[text_content] = cililianjie
            print(result_dict)     #需要保存的变量

            with open(f"./电视3/{txt_mingzi}.txt", "w", encoding="utf-8") as file:
                file.write(jianjie + '\n')
                for key, value in result_dict.items():
                    file.write(f"{key}: {value}\n")

            print()
        else:
            sys.exit()


page_url = "https://www.4ksj.com/zt/4kuhd.html"
response = requests_session.get(page_url)
soup = BeautifulSoup(response.text, 'html.parser')
a_tags = soup.find_all('span', {'style': 'font-size:15px; margin-left:10px;', 'class': 'z'})
print(len(a_tags))
a_tags = [a for sublist in a_tags for a in sublist.find_all('a', {'target': '_blank'})]
print(len(a_tags))
txt_mingzi=''
jianjie=''
cililianjie=''
for a_tag in a_tags:
    if a_tag:
        a_tag.find_all('a',{'target':'_blank'})
        txt_mingzi=a_tag.get_text()
        link_url=a_tag['href']
        full_link_url = f"{link_url}"
        print(txt_mingzi)
        print('链接：'+ full_link_url)
        driver.get(full_link_url)
        link_soup = BeautifulSoup(driver.page_source, 'html.parser')
        div_tag = link_soup.find('div', class_='nex_drama_intros') or link_soup.find('div', class_='nex_juji_intros')
        text_content = div_tag.text
        text_content = text_content.replace('简介', '', 1).strip() or text_content.replace('剧情简介', '', 1).strip()
        jianjie=text_content
        print(text_content)
        a_tag2s_mingzi=link_soup.find_all('div',{'class':'fileaq'})
        a_tag2s_link = link_soup.find_all('div',{'class':'down_2'})
        torrent_link =  [a for sublist in a_tag2s_link for a in sublist.find_all('a', {'target': '_blank'})]
        mingzi_list = [div.get_text().strip() for div in a_tag2s_mingzi]
        link_list = [a['href'] for a in torrent_link]
        if len(mingzi_list) != len(link_list):
            raise ValueError("两个列表的长度不同，无法配对。")
        result_dict = dict(zip(mingzi_list, link_list))

        td_tag = link_soup.find('td', {'class': 't_f'})

        for strong_tag in td_tag.find_all('strong'):
            text_content = strong_tag.get_text().split('【')[0].split('：')[-1].strip()
            next_sibling = strong_tag.find_next_sibling()

            if next_sibling and next_sibling.name == 'a' and 'magnet' in next_sibling['href']:
                link_content = next_sibling['href']
                match = re.match(r"(magnet:\?xt=urn:btih:[a-zA-Z0-9]+&dn)", link_content)
                if match:
                    cililianjie = match.group(1)
                result_dict[text_content] = cililianjie
        print(result_dict)     #需要保存的变量

        with open(f"./电视3/{txt_mingzi}.txt", "w", encoding="utf-8") as file:
            file.write(jianjie + '\n')
            for key, value in result_dict.items():
                file.write(f"{key}: {value}\n")

        print()
    else:
        sys.exit()



driver.quit()