# -*- coding: utf-8 -*-
import traceback, lxml, re, time
import requests, pandas as pd
from bs4 import BeautifulSoup
import datetime
from PyQt5.Qt import QThread, pyqtSignal


class drawing:

    def __init__(self):
        self.data = {}

    def draw(self, keyword, error=0):
        try:
            a = []
            b = []
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',  'Cookie':self.baseData.get('cookie') or 'BAIDUID=FB54817946F4A5928512F159E5089948:FG=1; BAIDUID_BFESS=FB54817946F4A5928512F159E5089948:FG=1; BIDUPSID=FB54817946F4A5928512F159E5089948; PSTM=1682990100; delPer=0; BD_CK_SAM=1; PSINO=6; H_PS_PSSID=38515_36551_38529_38469_38366_38538_38468_38485_37938_37709_26350_38567_38546; kleck=8bb51c3ddfc1dc2213cb3e9d0d93402b; BD_UPN=12314753; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BA_HECTOR=25ah250la080008g0421841o1i50p0k1m; ZFY=SGgES1MBm1lkxFr5fJowCay4e6J9YhKtOW7KHhwq8rQ:C; BD_HOME=1; B64_BOT=1; channel=baidusearch; ispeed_lsm=0; baikeVisitId=be691125-de73-45be-8535-718bf8f4f30d; H_PS_645EC=95bfTVqTok%2BcFzJPiB0OmCjpEIB3CCR8irrEneWHE7QncyGkw71usocmdhw; BDSVRTM=0; COOKIE_SESSION=38746_0_7_4_6_13_0_1_7_6_1_2_88397_0_42_0_1683032423_0_1683032381%7C9%232759960_32_1677735967%7C9; WWW_ST=1683032588971'}
            url = 'http://www.baidu.com/s'
            print(headers)
            params = {'ie': "'utf-8'",
             'mod': "'1'",
             'isbd': "'1'",
             'isid': "'fa42a508000b72aa'",
             'f': "'8'",
             'rsv_bp': "'1'",
             'rsv_idx': "'1'",
             'tn': "'baidu'",
             'wd': keyword,
             'fenlei': "'256'",
             'oq': keyword,
             'rsv_pq': "'fa42a508000b72aa'",
             'rsv_t': "'99b6iusGWDttH3pj4Fh1LUfzZZFulA3L56iJDEOrAt4OzCD4K/2XPHFR3XQ'",
             'rqlang': "'cn'",
             'rsv_enter': "'1'",
             'rsv_dl': "'tb'",
             'rsv_btype': "'t'",
             'inputT': "'2'",
             'rsv_sug3': "'4'",
             'rsv_sug1': "'2'",
             'rsv_sug7': "'100'",
             'rsv_sug2': "'0'",
             'rsv_sug4': "'126'",
             'rsv_sug': "'1'",
             'bs': keyword,
             'rsv_sid': "'38515_36551_38529_38469_38366_38538_38468_38485_37938_37709_26350_38567_38546'",
             '_ss': "'1'",
             'hsug': "''",
             'f4s': "'1'",
             'csor': "'6'",
             '_cr1': "'49407'"}
            response = requests.get(url, headers=headers, params=params)
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            content = soup.select('#content_left>.result')
            cc = soup.select('.page-inner_2jZi2>a')
            print(f'cc的长度：{len(cc)}')
            if len(cc) <= 3:
                self.submitMessage(f"爬虫监测，{keyword} 暂停...")
                time.sleep(15)
                if error > 30:
                    return ('', '', 0)
                error += 1
                return self.draw(keyword, error)
            for index, item in enumerate(content):
                t = ''
                mu = item.attrs.get('mu')
                ok = item.select_one('.siteLink_9TPP3')
                ok8 = item.select_one('.c-container').text.strip() if item.select_one('.c-container') else ''
                print(mu)
                print("ok:",ok)
                print('ok8:',ok8)
                serial = index + 1
                pattern = re.compile('51A|五一艾|佳宁颂|嘉宁颂')
                match = pattern.search(ok8)
                if ok and ok.text.strip() == '酒店软装设计公司五一' and 'baijiahao' in mu:
                    print(serial, ok.text.strip())
                    a.append(str(serial))
                    b.append('百家号')
                    t = f"{serial} 百家号"
                else:
                    if match and 'b2b168.com' in mu:
                        print(serial, ok.text.strip())
                        a.append(str(serial))
                        b.append('八方资源网')
                        t = f"{serial} 八方资源网"
                    else:
                        if match:
                            if 'trustexporter' in mu or '11467.com' in mu:
                                print(serial, ok.text.strip())
                                a.append(str(serial))
                                b.append('顺企网')
                                t = f"{serial} 顺企网"
                if match:
                    if 'china.cn' in mu:
                        print(serial, ok.text.strip())
                        a.append(str(serial))
                        b.append('中供网')
                        t = f"{serial} 中供网"
                    else:
                        if match and '.baidu.com' in mu:
                            print(serial, ok.text.strip())
                            a.append(str(serial))
                            b.append('百家号')
                            t = f"{serial} 百家号"
                        else:
                            if match:
                                if '51sole.com' in mu:
                                    print(serial, ok.text.strip())
                                    a.append(str(serial))
                                    b.append('搜了网')
                                    t = f"{serial} 搜了网"

                if match:
                    if 'bilibili.com' in mu:
                        print(serial, ok.text.strip())
                        a.append(str(serial))
                        b.append('中供网')
                        t = f"{serial} 中供网"

                    if t:
                        self.submitMessage(f"   {t}")

            a1 = ','.join(a) if len(a) else ''
            b1 = ','.join(b) if len(b) else ''
            c1 = len(b) if len(b) else 0
            return (a1, b1, c1)
        except:
            print(traceback.print_exc())

    def main(self):
        self.fdata = pd.read_excel(self.baseData.get('path'))
        for index, row in self.fdata.iterrows():
            try:
                keyword = f"{row[0]}{row[1]}"
                self.submitMessage(f"{index + 1} {keyword}")
                a, b, c = self.draw(keyword)
                time.sleep(2)
                da = datetime.datetime.now()
                self.fdata.iloc[(index, 2)] = c
                self.fdata.iloc[(index, 3)] = f"{da.year}{da.month}{da.day}"
                self.fdata.iloc[(index, 4)] = a
                self.fdata.iloc[(index, 5)] = b
            except:
                pass

        self.fdata.to_excel('结果.xlsx')
        self.submitMessage('成功检索')

e = True

class Thread_1(QThread, drawing):
    _signal = pyqtSignal(dict)

    def __init__(self, store):
        self.baseData = store
        super(Thread_1, self).__init__()

    def run(self):
        try:
            self.exeDrawing()
        except:
            print(traceback.print_exc())

    def submitMessage(self, string, thisType='str'):
        self._signal.emit({'type':thisType,  'data':string}) if self._signal else print(string)

    def exeDrawing(self):
        try:
            self.submitMessage('初始化成功...')
            self.main()
            print(pd)
        except:
            print(traceback.print_exc())


w=drawing()
