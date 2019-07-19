#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request

from main import main

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World!"


@app.route("/api/get/companies", methods=["GET", "POST"])
def get_companies():
    """
    企業名を取得する
    :param:
    id : str
        ログイン用ID
    password : str
        ログイン用パスワード

    :return:
    company_list : list

    """
    if request.method == "GET":
        uid = request.args.get('uid')
        password = request.args.get('password')

        crawl = main.Crawl(uid, password)
        company_list = crawl.get_company_list()

        return company_list


@app.route("/api/get/jobs", methods=["GET", "POST"])
def get_jobs():
    """
    案件を取得する
    :param:
    id : str
        ログイン用ID
    password : str
        ログイン用パスワード
    company_num : int
        企業番号

    :return:
    job_list : list
    """
    if request.method == "GET":
        uid = request.args.get('uid')
        password = request.args.get('password')
        company_num = request.args.get('company_num')

        crawl = main.Crawl(uid, password)
        job_list = crawl.get_job_list(company_num)

        return job_list


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)