import time
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
URL = "https://tv.doutoutiao.cc/forum.php"
driver = webdriver.Chrome()

try:
    driver.get(URL)
    open_login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "已有帐号？现在登录"))
    )
    open_login_button.click()
    print("点击登录按钮成功")

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
    print("点击提交按钮成功")

    try:
        manual_redirect_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "succeedmessage_href"))
        )
        manual_redirect_link.click()
        print("手动点击跳转链接")
    except:
        print("手动跳转链接不存在，可能已经自动跳转")

    selenium_cookies = driver.get_cookies()
    requests_session = requests.Session()
    for cookie in selenium_cookies:
        requests_session.cookies.set(cookie['name'], cookie['value'])

    base_url = "https://tv.doutoutiao.cc/forum.php?mod=forumdisplay&fid=2&sortid=1&sortid=1&page="
    for page_num in range(1, 10000):
        page_url = base_url + str(page_num)
        response = requests_session.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        a_tags = soup.find_all('a', {'class': 's xst', 'style': 'font-weight: bold;color: #3C9D40;'})
        txt_mingzi=''
        jianjie=''
        cililianjie=''
        cililianjie_dicts={}
        if a_tags:
            flag=False
            for a_tag in a_tags:
                text = a_tag.get_text()
                matched = re.search(r'(.*?\[.*?\]\[.*?\])', text)
                if matched:
                    txt_mingzi=matched.group(1)
                    print(txt_mingzi)    #txt的名字
                    link_url = a_tag['href']
                    full_link_url = f"https://tv.doutoutiao.cc/{link_url}"
                    driver.get(full_link_url)
                    link_soup = BeautifulSoup(driver.page_source, 'html.parser')
                    th_tag = link_soup.find_all('th')[4]
                    td_tag =th_tag.find_next_sibling('td')
                    if td_tag.getText().strip()=='中国大陆':
                        flag=True
                    pattern = re.compile(r'◎简　　介<br/>\s*(.*?)\s*<div class="blockcode">', re.DOTALL)
                    match = pattern.search(str(link_soup))
                    if match:
                        intro_text = match.group(1)
                        jianjie = intro_text.replace(' ', '').replace('&nbsp;', '').replace('<br/>', '')
                        print(jianjie)   #需要保存的变量-简介
                    else:
                        print("未找到简介文本")
                    torrent_link = link_soup.find('a', {'onclick': re.compile(r"showWindow\('torrentInfo', this.href\)")})
                    if torrent_link:
                        href_value = torrent_link['href']
                        full_url = f"https://tv.doutoutiao.cc/{href_value}"
                        print(full_url)
                        driver.get(full_url)
                        time.sleep(2)
                        new_page_soup = BeautifulSoup(driver.page_source, 'html.parser')
                        magnet_link_size = new_page_soup.find_all('div', {'class': 'bt_right'})[1]
                        magnet_link_size=magnet_link_size.text
                        magnet_link = new_page_soup.find('a', {
                            'onclick': "setCopy(this.href, '磁力链接复制成功');return false;",
                            'class': "bt_copy",
                            'hidefocus': "true"
                        })

                        if magnet_link:
                            match = re.match(r"(magnet:\?xt=urn:btih:[a-zA-Z0-9]+&dn)", magnet_link['href'])
                            if match:
                                cililianjie = match.group(1)
                                cililianjie_dicts[magnet_link_size]=cililianjie
                                print(cililianjie)   #需要保存的变量
                            else:
                                print("未找到磁力链接的匹配部分")
                        else:
                            print("未找到磁力链接")
                if flag==False:
                    txt_mingzi = txt_mingzi.replace("[", "").replace("]", "").replace("/", "-").replace("\\", "-")
                    with open(f"./电视1/{txt_mingzi}.txt", "w", encoding="utf-8") as file:
                        file.write(jianjie+'\n')
                        for key,value in cililianjie_dicts.items():
                            file.write(f"{key}:{value}\n")

                print()
        else:
            sys.exit()
            


finally:
    time.sleep(20)
    driver.quit()
