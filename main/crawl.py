# -*- Coding: UTF-8 -*-
import json
# スクレイピング必要分
from bs4 import BeautifulSoup
import re
# seleniumでブラウザ操作
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import traceback
from selenium import webdriver

# ID,PASSを入力する
def input_id_pass(driver, id_email, pass_password):
    email = driver.find_element_by_name("email")
    email.send_keys(id_email)
    password = driver.find_element_by_name("password")
    password.send_keys(pass_password)


# ログインボタンのクリック
def click_login(driver):
    login_button = driver.find_element_by_name("submit")
    login_button.click()


# 企業の取得
def get_company(driver):
    page_source = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(page_source, "html.parser")

    company_items = soup.find_all("hrm-nav-list-detail-item")

    company_list = []
    for item in company_items:
        try:
            company_item = {}
            company_item["company_link"] = item.a.get("href").strip()
            company_item["company_name"] = item.find("span", class_="normal").text

            company_list.append(company_item)

        except:
            continue

    return company_list


# 企業求人一覧ページのURLを取得
def get_company_url(company_num):
    base_url = "https://hrmos.co/agent/corporates/"
    url = base_url + str(company_num) + "/jobs"

    return url


# 企業求人一覧を取得
def get_job_list(driver):
    job_list = []

    page_source = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(page_source, "html.parser")

    job_items = soup.find_all("a", class_="ng-tns-c13-0")

    for item in job_items:
        job_item = {}
        job_item["job_link"] = item.get("href")
        job_item["job_name"] = item.find("span", class_="normal").text
        job_list.append(job_item)

    return job_list


# 数字（企業No）のみを取り出す
def extract_company_num(company_link):
    company_num = re.search(r'\/[0-9]*\/' , company_link)
    company_num = company_num.group().replace("/","")
    return company_num


# 数字（案件No）のみを取り出す
def extract_job_num(job_link):
    job_num = re.search(r'[0-9]*$', job_link)
    return job_num.group()


def get_all(uid, password):
    options = Options()
    # Heroku以外ではNone
    if chrome_binary_path:
        options.binary_location = chrome_binary_path
        options.add_argument('--headless')

        driver = Chrome(executable_path=driver_path, chrome_options=options)

    #　ローカルの場合
    # options.add_argument('--headless')
    # driver = webdriver.Chrome(executable_path="/Users/shingo/webdriver/chromedriver", options=options)

    try:
        driver.get("https://hrmos.co/agent/login")
        time.sleep(3)

        # ID/PASSを入力
        input_id_pass(driver, uid, password)

        time.sleep(1)

        # ログインボタンをクリック
        click_login(driver)

        time.sleep(3)

        # 企業を取得
        companies = get_company(driver)

        for company_obj in companies:
            company_num = extract_company_num(company_obj["company_link"])
            # 企業ページのURLを取得
            url = get_company_url(company_num)
            # 遷移する
            driver.get(url)
            time.sleep(3)

            job_list = get_job_list(driver)
            for job in job_list:
                job["company_name"] = company_obj["company_name"]
                job["company_num"] = company_num
                job["job_num"] = extract_job_num(job["job_link"])
            time.sleep(2)

        jsonstring = json.dumps(job_list, ensure_ascii=False,
                                indent=2)  # 作った配列をjson形式にして出力する

        return jsonstring

    except:
        traceback.print_exc()
    finally:
        # エラーが起きても起きなくてもブラウザを閉じる
        driver.quit()