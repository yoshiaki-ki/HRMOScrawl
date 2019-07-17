#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request

from main import crawl

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World!"


@app.route("/api/get/all", methods=["GET", "POST"])
def get_all_jobs():
    """
    企業、案件を全て取得する
    :param:
    id : str
        ログイン用ID
    password : str
        ログイン用パスワード

    :return:
    job_list : list
    """
    if request.method == "GET":
        uid = request.args.get('uid')
        password = request.args.get('password')
        result = crawl.get_all(uid, password)

        return result

    else:
        try:
            pass

        except:
            pass


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
    pass


#
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
    pass


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)