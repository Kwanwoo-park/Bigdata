import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from itertools import count
from selenium import webdriver
import time


def get_request_url(url, enc='utf-8'):
    req = urllib.request.Request(url)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            try:
                rcv = response.read()
                ret = rcv.decode(enc)
            except UnicodeDecodeError:
                ret = rcv.decode(enc, 'replace')

            return ret

    except Exception as e:
        print(e)
        print("[%s] Error for URL: %s" % (datetime.datetime.now(), url))
        return None


def getBBQAddress(result):
    BBQ_URL = 'https://www.bbq.co.kr/shop/shopList.asp?page=1&pagesize=2000&gu=&si='
    print(BBQ_URL)

    rcv_data = get_request_url(BBQ_URL)
    soupData = BeautifulSoup(rcv_data, 'html.parser')

    tbody = soupData.find('tbody')

    tr_tag = []

    for store_tr in tbody.findAll('tr'):
        tr_tag = list(store_tr.strings)
        store_name = tr_tag[1]
        store_address = tr_tag[3]
        store_sido_gu = store_address.split()[:2]

        result.append([store_name] + store_sido_gu + [store_address])

    return


def getPelicanaAddress(result):
    for page_idx in count():
        Pelicana_URL = 'http://www.pelicana.co.kr/store/stroe_search.html?&branch_name=&gu=&si=&page=%s' % str(page_idx+1)
        print("[Pericana Page] : [%s]" % (str(page_idx+1)))

        rcv_data = get_request_url(Pelicana_URL)
        soupData = BeautifulSoup(rcv_data, 'html.parser')
        store_table = soupData.find('table', attrs={'class':'table mt20'})
        tbody = store_table.find('tbody')
        bEnd = True

        for store_tr in tbody.findAll('tr'):
            bEnd = False
            tr_tag = list(store_tr.strings)
            store_name = tr_tag[1]
            store_address = tr_tag[3]
            store_sido_gu = store_address.split()[:2]

            result.append([store_name] + store_sido_gu + [store_address])

        if bEnd == True:
            return

    return


def getNeneAddress(result):
    for page_idx in count():
        Nene_URL = 'https://nenechicken.com/17_new/sub_shop01.asp?page=%s&ex_select=1&ex_select2=&IndexSword=&GUBUN=A' % str(page_idx)
        print(Nene_URL)
        rcv_data = get_request_url(Nene_URL)

        soup_data = BeautifulSoup(rcv_data, 'html.parser')
        store_table = soup_data.find('table', attrs={'class':'shopTable'})
        tbody = store_table.find('tbody')

        for store_tr in tbody.findAll('tr'):
            tr_tags = list(store_tr.string)

            if tr_tags[0] == '게시물이 없습니다.':
                return

            store_name = tr_tags[1]
            store_address = tr_tags[3]
            store_sido_gu = store_address.split()[:2]

            result.append([store_name] + store_sido_gu + [store_address])

    return


def getKyochonAddress(sido1, result):
    for sido2 in count():
        Kyochon_URL = 'http://www.kyochon.com/shop/domestic.asp?txtsearch=&sido1=%s&sido2=%s' % (str(sido1), str(sido2))
        print(Kyochon_URL)

        try:
            rcv_data = get_request_url(Kyochon_URL)
            soupData = BeautifulSoup(rcv_data, 'html.parser')

            ul_tag = soupData.find('ul', attrs={'class':'list'})

            for store_data in ul_tag.findall('a', href=True):
                store_name = store_data.find('dt').get_text()
                store_address = store_data.find('dd').get_text().strip().split('/r')[0]
                store_sido_gu = store_address.split()[:2]
                result.append([store_name] + store_sido_gu + [store_address])
        except:
            break

    return


def CheogajipAddress(result):
    for page_idx in count():
        Cheogajip_URL = 'http://www.cheogajip.co.kr/bbs/board.php?bo_table=store&page=%s' % str(page_idx+1)

        print(Cheogajip_URL)
        response = urllib.request.urlopen(Cheogajip_URL)
        soupData = BeautifulSoup(response.read().decode('utf-8'), 'html.parser')

        store_table = soupData.find('table')
        tbody = store_table.find('tbody')

        for store_tr in tbody.findAll('tr'):
            tr_tag = list(store_tr.strings)
            if tr_tag[0] != '게시물이 없습니다.':
                store_name = tr_tag[3]
                store_address = tr_tag[5]
                store_sido_gu = store_address.split()[:2]

                result.append([store_name] + store_sido_gu + [store_address])
            else:
                return


    return


def GoobneAddress(result):
    Goobne_URL = 'http://www.goobne.co.kr/store/search_store.jsp'

    wd = webdriver.Chrome('c:/Users/lg/AppData/Local/Programs/Python/Python39/WebDriver/chromedriver.exe')
    wd.get(Goobne_URL)
    time.sleep(10)

    for page_idx in count():
        wd.execute_script("store.getList(%s)" % str(page_idx+1))
        print("PageIndex [%s] Called" % (str(page_idx+1)))

        time.sleep(5)

        rcv_data = wd.page_source

        soupData = BeautifulSoup(rcv_data, 'html.parser')

        for store_list in soupData.findAll('tbody', attrs={'id':'store_list'}):
            for store_tr in store_list:
                tr_tag = list(store_tr.strings)

                if tr_tag[0] == '등록된 데이터가 없습니다.':
                    return result

                store_name = tr_tag[1]

                if tr_tag[3] == '':
                    store_address = tr_tag[5]
                else:
                    store_address = tr_tag[6]

                store_sido_gu = store_address.split()[:2]

                result.append([store_name] + store_sido_gu + [store_address])

    return


def main():
    result = []

    # print('BBQ ADDRESS CRAWLING START')
    # getBBQAddress(result)
    # bbq_table = pd.DataFrame(result, columns=('store', 'sido', 'gungu', 'store_address'))
    # bbq_table.to_csv('c:/Users/lg/IdeaProjects/Bigdata/web_data/bbq.csv', encoding='cp949', mode='w', index=True)
    # del result[:]
    #
    # print('NENE ADDRESS CRAWLING START')
    # getNeneAddress(result)
    # nene_table = pd.DataFrame(result, columns=('store', 'sido', 'gungu', 'store_address'))
    # nene_table.to_csv('c:/Users/lg/IdeaProjects/Bigdata/web_data/nene.csv', encoding='cp949', mode='w', index=True)
    # del result[:]
    # #
    # print('KYOCHON ADDRESS CRAWLING START')
    # for sido1 in range(1, 18):
    #     getKyochonAddress(sido1, result)
    # kyochon_table = pd.DataFrame(result, columns=('store', 'sido', 'gungu', 'store_address'))
    # kyochon_table.to_csv('c:/Users/lg/IdeaProjects/Bigdata/web_data/kyochon.csv', encoding='cp949', mode='w', index=True)
    # del result[:]

    print('PERICANA ADDRESS CRAWLING START')
    getPelicanaAddress(result)
    pericana_table = pd.DataFrame(result, columns=('store', 'sido', 'gungu', 'store_address'))
    pericana_table.to_csv('c:/Users/lg/IdeaProjects/Bigdata/web_data/pericana.csv', encoding='cp949', mode='w', index=True)
    del result[:]

    print('CHIEOGAJIP ADDRESS CRAWLING START')
    CheogajipAddress(result)
    cheogajip_table = pd.DataFrame(result, columns=('store', 'sido', 'gungu', 'store_address'))
    cheogajip_table.to_csv('c:/Users/lg/IdeaProjects/Bigdata/web_data/cheogajip.csv', encoding='cp949', mode='w', index=True)
    del result[:]

    print('GOOBNE ADDRESS CRAWLING START')
    GoobneAddress(result)
    goobne_table = pd.DataFrame(result, columns=('store', 'sido', 'gungo', 'store_address'))
    goobne_table.to_csv('c:/Users/lg/IdeaProjects/Bigdata/web_data/goobne.csv', encoding='cp949', mode='w', index=True)

    print('FINISHED')


if __name__ == '__main__':
    main()