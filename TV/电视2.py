import time
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
URL = "https://www.grab4k.com/index.php/user/login.html"
driver = webdriver.Chrome()

try:
    driver.get(URL)

    username_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "user_name"))
    )
    username_input.send_keys("1071515307")
    print("输入登录账号成功")

    password_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "user_pwd"))
    )
    password_input.send_keys("1234567")
    print("输入密码成功")

    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btn_submit"))
    )
    submit_button.click()
    print("点击登录成功")

    selenium_cookies = driver.get_cookies()
    requests_session = requests.Session()
    for cookie in selenium_cookies:
        requests_session.cookies.set(cookie['name'], cookie['value'])

    base_url = 'https://www.grab4k.com/vod/show/id/suoyin/page/{}.html'
    for page in range(1, 10000):
        url = base_url.format(page)
        response = requests_session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find_all('div', {'class': 'module-item-pic'})
        a_tags = [div.find('a') for div in divs]
        txt_mingzi=''
        jianjie=''
        cililianjie=''
        for a_tag in a_tags:
            if a_tag:
                text = a_tag['title'] if a_tag else None
                txt_mingzi = text
                print(text)
                link_url = a_tag['href']
                full_link_url = f"https://www.grab4k.com/{link_url}"
                driver.get(full_link_url)
                print(full_link_url)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                html_content = driver.page_source
                pattern = re.compile(r'<div class="video-info-item video-info-content vod_content"><span>(.*?)</span></div>', re.DOTALL)
                match = pattern.search(html_content)
                if match:
                    span_content = match.group(1)
                    jianjie=span_content  #保存的简介
                    print(span_content)
                else:
                    print("没有找到匹配的内容")
                cililianjie_dict={}
                cililianjie_name_s=soup.find_all('h4')
                cililianjie_name_s = [cililianjie_name.get_text() for cililianjie_name in cililianjie_name_s]
                cililianjie_s=[]
                a_tags = soup.find_all('a', {'class': 'module-row-text copy'})
                for a_tag in a_tags:
                    if a_tag:
                        magnet_link = a_tag['data-clipboard-text']
                        pattern = re.compile(r"(magnet:\?xt=urn:btih:[A-Za-z0-9]+)")
                        match = pattern.match(magnet_link)
                        if match:
                            extracted_magnet_link = match.group(1)
                            magnet_link=extracted_magnet_link
                        else:
                            magnet_link = magnet_link
                        cililianjie_s.append(magnet_link)
                        print(magnet_link)
                    else:
                        print("没有找到匹配的<a>标签")
                print()
                cililianjie_dict=dict(zip(cililianjie_name_s, cililianjie_s))
                print(cililianjie_dict)
                with open(f"./电视2/{txt_mingzi}.txt", "w", encoding="utf-8") as file:
                    file.write(jianjie+'\n')
                    for key,value in cililianjie_dict.items():
                        file.write(f"{key}:{value}\n")
                print()
            else:
                sys.exit()

    base_url = 'https://www.grab4k.com/vod/show/id/juji/page/{}.html'
    for page in range(1, 10000):
        url = base_url.format(page)
        response = requests_session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find_all('div', {'class': 'module-item-pic'})
        a_tags = [div.find('a') for div in divs]
        txt_mingzi=''
        jianjie=''
        cililianjie=''
        for a_tag in a_tags:
            if a_tag:
                text = a_tag['title'] if a_tag else None
                txt_mingzi = text
                print(text)
                link_url = a_tag['href']
                full_link_url = f"https://www.grab4k.com/{link_url}"
                driver.get(full_link_url)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                html_content = driver.page_source
                pattern = re.compile(r'<div class="video-info-item video-info-content vod_content"><span>(.*?)</span></div>', re.DOTALL)
                match = pattern.search(html_content)
                if match:
                    span_content = match.group(1)
                    jianjie=span_content  #保存的简介
                    print(span_content)
                else:
                    print("没有找到匹配的内容")
                cililianjie_s=[]
                a_tags = soup.find_all('a', {'class': 'module-row-text copy'})
                for a_tag in a_tags:
                    if a_tag:
                        magnet_link = a_tag['data-clipboard-text']
                        pattern = re.compile(r"(magnet:\?xt=urn:btih:[A-Za-z0-9]+)")
                        match = pattern.match(magnet_link)
                        if match:
                            extracted_magnet_link = match.group(1)
                            magnet_link=extracted_magnet_link
                        else:
                            magnet_link = magnet_link
                        cililianjie_s.append(magnet_link)
                        print(magnet_link)
                    else:
                        print("没有找到匹配的<a>标签")
                print()

                with open(f"./电视/{txt_mingzi}.txt", "w", encoding="utf-8") as file:
                    file.write(jianjie+'\n')
                    for cililianjie in cililianjie_s:
                        file.write(cililianjie+'\n')
                print()
            else:
                sys.exit()

finally:
    time.sleep(20)
    driver.quit()