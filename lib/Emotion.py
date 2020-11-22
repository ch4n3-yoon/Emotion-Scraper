# coding: utf-8

import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

headers = {
    'Referer': 'https://demo.pingpong.us/sentiment-analyzer/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': '_ga=GA1.2.257438808.1602743624; uncode_privacy[consent_types]=%5B%5D; uncodeAI.screen=2560; uncodeAI.images=2880; uncodeAI.css=2560x1080@16.1; _gid=GA1.2.409086791.1603943134; _gat_gtag_UA_142588611_4=1; _gat_gtag_UA_125669591_1=1; tk_ai=woo%3AEXGV4Dr%2BC5Gp6jJPC6ku6V8H'
}


def get_emotion(query) -> float:
    query = query.encode().decode('utf-8')
    url = 'https://demo.pingpong.us/api/sentiment.php'
    resp = requests.get(url, params={'queries': query}, verify=False, headers=headers)
    try:
        resp_json = resp.json()
    except json.decoder.JSONDecodeError:
        print('[ ERROR ] Json Decode Error')
        print(resp.text)

        return 0.0

    # For debugging
    # print(resp_json)

    try:
        posneg = resp_json[0][1]
    except IndexError:
        print(f'[ ERROR ] Invalid Query ({query})')
        print('└─[ MESSAGE ] Check that query is empty')

        return 0.0

    model_score = float(posneg.get('model_score'))
    # score = posneg.get('message')

    return model_score


if __name__ == '__main__':
    print(get_emotion('테스트 테스트 테스트'))
