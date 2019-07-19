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


class Crawl:
    BASE_URL = "https://hrmos.co/agent/corporates/"

    def __init__(self, uid, password):
        self.uid = uid
        self.password = password

    def get_driver(self):
        options = Options()

        options.binary_location = '/app/.apt/usr/bin/google-chrome'
        options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=options)

        # 　ローカルの場合
        # options.add_argument('--headless')
        # driver = webdriver.Chrome(executable_path="/Users/kiryu/webdriver/chromedriver", options=options)

        url = "https://hrmos.co/agent/login"
        driver.get(url)
        time.sleep(2)
        return driver

    # ID/PASS入力,Login
    def login(self, driver):
        uid = driver.find_element_by_name("email")
        uid.send_keys(self.uid)
        password = driver.find_element_by_name("password")
        password.send_keys(self.password)
        login_button = driver.find_element_by_name("submit")
        login_button.click()

    def get_company_list(self):
        """
        企業の取得
        :param
        :return: list
            key:company_name, company_link, company_num
        """
        driver = self.get_driver()

        try:
            self.login(driver)
            time.sleep(1)
            page_source = driver.page_source.encode('utf-8')
            soup = BeautifulSoup(page_source, "html.parser")

            company_items = soup.find_all("hrm-nav-list-detail-item")
            companies_list = []
            for item in company_items:
                try:
                    company_item = {}
                    company_item["company_link"] = item.a.get("href").strip()
                    company_item["company_name"] = item.find("span", class_="normal").text
                    company_item["company_num"] = re.search(r'\/[0-9]*\/', company_item["company_link"]).group().replace("/", "")
                    companies_list.append(company_item)
                except:
                    continue

            company_list = json.dumps(companies_list, ensure_ascii=False,
                                        indent=2)  # 作った配列をjson形式にして出力する
            return company_list

        except:
            traceback.print_exc()
        finally:
            # エラーが起きても起きなくてもブラウザを閉じる
            driver.quit()

    def get_job_list(self, company_num):
        """
        求人一覧を取得
        :param company_num:
        :return: job_list
        """
        url = self.BASE_URL + str(company_num) + "/jobs"

        driver = self.get_driver()

        try:
            self.login(driver)
            time.sleep(2)
            # 遷移する
            driver.get(url)
            time.sleep(2)
            page_source = driver.page_source.encode('utf-8')
            soup = BeautifulSoup(page_source, "html.parser")

            job_items = soup.find_all("a", class_="ng-tns-c13-0")
            print(job_items)
            job_list = []
            for item in job_items:
                try:
                    job_item = {}
                    job_item["job_link"] = item.get("href")
                    job_item["job_name"] = item.find("span", class_="normal").text
                    job_item["job_num"] = re.search(r'[0-9]*$', job_item["job_link"]).group()
                    job_list.append(job_item)
                except:
                    continue

            jobs_list = json.dumps(job_list, ensure_ascii=False,
                                        indent=2)  # 作った配列をjson形式にして出力する
            return jobs_list

        except:
            traceback.print_exc()
        finally:
            # エラーが起きても起きなくてもブラウザを閉じる
            driver.quit()
