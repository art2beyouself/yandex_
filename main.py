from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
from datetime import datetime


import pandas as pd
import locale
locale.setlocale(locale.LC_ALL, '')
'ru_RU.utf8'
import time


list_date = []
list_raitin = []

list_date2 = []
list_raitin2 = []


key = "date"
key2 = "reiting"

dates = {}
reitin = {}

def seleniums(base_url, times, name):
    print(base_url)
    print(time)

    x = times.partition("/")[0]
    y = times.partition("/")[2]

    print(x)
    print(y)


    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-data-dir=selenium")
    # options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)

    # base_url = "https://yandex.kz/maps/org/epilium_clinic/191265823168/"

    # Wait untill input text box is visible
    if "yandex" in base_url:
        if 'reviews' not in base_url: base_url = base_url.partition('?')[0] + 'reviews'

    browser.get(base_url)
    time.sleep(2)

    if "2gis" in base_url:
        try:
            element = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[2]/div[1]/div/div/div[1]/div[3]/div/a')
        except:
            element = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[2]/div[1]/div/div/div[1]/div[3]/div/a')
        for i in range(0, 20):
            ActionChains(browser).send_keys_to_element(element, Keys.CONTROL, Keys.END).perform()
            time.sleep(0.5)
        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")

        start = 'inline-image _loaded business-rating-badge-view__star _full _size_m'
        # перебираем первые 5 звезд
        reiting = 0
        for container in soup.find_all("div", {"class": "_11gvyqv"}):
            for sta in container.find_all("div", {"class": "_1fkin5c"}):
                # перебираем все даты
                for a in container.find_all("div", {"class": "_4mwq3d"}):
                    dateString = a.get_text()
                    if ", отредактирован" in dateString:
                        dateString = dateString.replace(", отредактирован", "")
                    try:
                        dateFormatter = "%d %B %Y"
                        data = (datetime.strptime(dateString, dateFormatter).date())
                    except ValueError as errors:
                        dateString = dateString + ' 2023'
                        data = (datetime.strptime(dateString, dateFormatter).date())
                    # перебираем рейтинг
                    for id in sta.find_all("span"):
                        reiting += 1

                    list_date2.append(data)
                    list_raitin2.append(reiting)

                    reiting = 0

        dates.setdefault(key, list_date2)
        reitin.setdefault(key2, list_raitin2)
        d = dates | reitin
        df = pd.DataFrame(d)
        df["date"] = pd.to_datetime(df["date"], format='%Y-%m-%d')
        filtered = df.loc[(df["date"] >= x) & (df["date"] <= y)]
        data = (filtered['reiting'].value_counts(sort=False).to_dict())

        try:
            data["⭐ ⭐ ⭐ ⭐ ⭐"] = data[5]
            del data[5]
        except:
            pass

        try:
            data["⭐ ⭐ ⭐ ⭐"] = data[4]
            del data[4]
        except:
            pass

        try:
            data["⭐ ⭐ ⭐"] = data[3]
            del data[3]
        except:
            pass

        try:
            data["⭐ ⭐"] = data[2]
            del data[2]
        except:
            pass

        try:
            data["⭐"] = data[1]
            del data[1]
        except:
            pass

        list_date2.clear()
        list_raitin2.clear()
        print(data)
        resultList =  list(map(list, data.items()))

        answer = []
        answer.append(name)
        try:
            one = str(resultList[0]).replace(",", " -").replace("'", "").replace("[", "").replace("]", "")
            answer.append(one)
        except:
            pass

        try:
            two = str(resultList[1]).replace(",", " -").replace("'", "").replace("[", "").replace("]", "")
            answer.append(two)
        except:
            pass

        try:
            three = str(resultList[2]).replace(",", " -").replace("'", "").replace("[", "").replace("]", "")
            answer.append(three)
        except:
            pass

        try:
            fore = str(resultList[3]).replace(",", " -").replace("'", "").replace("[", "").replace("]", "")
            answer.append(fore)
        except:
            pass

        try:
            five = str(resultList[4]).replace(",", " -").replace("'", "").replace("[", "").replace("]", "")
            answer.append(five)
        except:
            pass

        doness = '\n'.join(answer)


        return doness




    if "yandex" in base_url:

        element = browser.find_element(By.LINK_TEXT, 'Отзывы')
        for i in range(0, 20):
            ActionChains(browser).send_keys_to_element(element, Keys.CONTROL, Keys.END).perform()
            time.sleep(0.2)

        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")

        start = 'inline-image _loaded business-rating-badge-view__star _full _size_m'
        # перебираем первые 5 звезд
        reiting = 0
        for container in soup.find_all("div", {"class": "business-review-view"}):
            for sta in container.find_all("div", {"class": "business-rating-badge-view__stars"}):
                # перебираем все даты
                for a in container.find_all("span", {"class": "business-review-view__date"}):
                    try:
                        dateString = a.get_text()
                        dateFormatter = "%d %B %Y"
                        data = (datetime.strptime(dateString, dateFormatter).date())
                    except ValueError as errors:
                        dateString = dateString + ' 2023'
                        data = (datetime.strptime(dateString, dateFormatter).date())
                    # перебираем рейтинг
                    for i in sta.find_all("span", {"class": start}):
                        reiting += 1

                    list_date.append(data)
                    list_raitin.append(reiting)
                    reiting = 0

        dates.setdefault(key, list_date)
        reitin.setdefault(key2, list_raitin)
        d = dates | reitin
        df = pd.DataFrame(d)
        df["date"] = pd.to_datetime(df["date"], format='%Y-%m-%d')
        filtered = df.loc[(df["date"] >= x) & (df["date"] <= y)]
        data = (filtered['reiting'].value_counts(sort=False).to_dict())

        try:
            data["⭐ ⭐ ⭐ ⭐ ⭐"] = data[5]
            del data[5]
        except:
            pass

        try:
            data["⭐ ⭐ ⭐ ⭐"] = data[4]
            del data[4]
        except:
            pass

        try:
            data["⭐ ⭐ ⭐"] = data[3]
            del data[3]
        except:
            pass

        try:
            data["⭐ ⭐"] = data[2]
            del data[2]
        except:
            pass

        try:
            data["⭐"] = data[1]
            del data[1]
        except:
            pass


        list_date.clear()
        list_raitin.clear()

        resultList = list(map(list, data.items()))

        answer = []
        answer.append(name)
        try:
            one = str(resultList[0]).replace(",", " -").replace("'", "").replace("[", "").replace("]", "")
            answer.append(one)
        except:
            pass

        try:
            two = str(resultList[1]).replace(",", " -").replace("'", "").replace("[", "").replace("]", "")
            answer.append(two)
        except:
            pass

        try:
            three = str(resultList[2]).replace(",", " -").replace("'", "").replace("[", "").replace("]", "")
            answer.append(three)
        except:
            pass

        try:
            fore = str(resultList[3]).replace(",", " -").replace("'", "").replace("[", "").replace("]", "")
            answer.append(fore)
        except:
            pass

        try:
            five = str(resultList[4]).replace(",", " -").replace("'", "").replace("[", "").replace("]", "")
            answer.append(five)
        except:
            pass

        doness = '\n'.join(answer)

        return doness

    # json_dates = json.dumps(dates)
    # json_reiting = json.dumps(reitin)
    #
    # print(json_dates)
    # print(json_reiting)

        print("Работа завершена")