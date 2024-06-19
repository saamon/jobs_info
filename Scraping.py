# scrapingライブラリ
import requests
from bs4 import BeautifulSoup
import os
import json

# config.jsonファイルを読み込む
with open('config.json', 'r') as f:
    config = json.load(f)


# 引数にurlを受け取り、アルバイト情報を取得する
def get_job_info(url):
    # Webページを取得
    res = requests.get(url, headers={'User-Agent': ''})
    soup = BeautifulSoup(res.text, 'html.parser')

    # アルバイト情報を取得
    jobs = []
    for job in soup.select('div.list-group a.list-group-item'):
        title = job.select_one('h5.list-group-heading').text
        description = job.select_one('p').text
        pay = job.select('p')[1].text
        categories = [span.text for span in job.select('p.right span.label-info')]

        jobs.append({
            'title': title,
            'description': description,
            'pay': pay,
            'categories': categories,
        })

    return jobs


# 引数にアルバイト情報とWebhook URLを受け取りDiscordに送信する
def send_to_discord(jobs, webhook_url):
    all_success = True
    for job in jobs:
        data = {
            'content': (
                f"Title: {job['title']}\n"
                f"Description: {job['description']}\n"
                f"Pay: {job['pay']}\n"
                f"Categories: {', '.join(job['categories'])}"
            )
        }
        response = requests.post(webhook_url, json=data)
        # もし送信に失敗した場合はエラーメッセージを表示
        if response.status_code != 204:
            print('メッセージ送信に失敗しました')
            all_success = False
    if all_success:
        print('全てのメッセージを送信しました')


# jsonファイルからwebhook_urlとtarget_urlを取得
webhook_url = config['webhook_url']
url = config['target_url']
jobs = get_job_info(url)
send_to_discord(jobs, webhook_url)
