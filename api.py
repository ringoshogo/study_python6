import requests
import urllib
import os
import csv

# 環境変数
from os.path import join, dirname
from dotenv import load_dotenv

# リクエスト
import requests

# 環境変数の設定
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# アプリケーションID
APP_ID=os.environ.get("APP_ID")

ICHBA_BASE_URL="https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
PRD_BASE_URL="https://app.rakuten.co.jp/services/api/Product/Search/20170426"
RNK_BASE_URL="https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628"

def get_api(url, payload=None):
    result = requests.get(url, params=payload)
    return result.json()

def get_item_list():
    
    """
    商品一覧と商品価格を取得する
    """
    payload = {
        'applicationId': APP_ID,
        'hits': 30,
        'keyword': "鬼滅"
    }
    res = get_api(ICHBA_BASE_URL, payload)
    
    results1 = []
    # 商品一覧と商品価格を取得する
    for i in res['Items']:
        item = i['Item']
        result = {}
        result['item_name'] = item['itemName']
        result['item_price'] = item['itemPrice']
        results1.append(result)

    return results1

def get_min_and_max_value():

    """
    最安値と最高値を取得する
    """
    payload = {
        'applicationId': APP_ID,
        'hits': 30,
        'keyword': "鬼滅",
    }
    res = get_api(PRD_BASE_URL, payload)
    
    results2 = []
    # 商品一覧と商品価格を取得する
    for i in res['Products']:
        item = i['Product']
        result = {}
        result['max_price'] = item['maxPrice']
        result['min_price'] = item['minPrice']
        results2.append(result)

def get_rank():
    """
    ジャンルのランキングを作成する
    """
    payload = {
        'applicationId': APP_ID,
        'hits': 30,
        'keyword': "鬼滅",
        'sort': '-seller'
    }
    res = get_api(RNK_BASE_URL, payload)
    
    results3 = [['ランキング', '製品名', '価格', '販売開始日時', '販売終了日時', 'レビュー件数', 'レビュー平均']]
    for i in res['Items']:
        item = i['Item']
        result = []
        result.append(item['rank'])
        result.append(item['itemName'])
        result.append(item['itemPrice'])
        result.append(item['startTime'])
        result.append(item['endTime'])
        result.append(item['reviewCount'])
        result.append(item['reviewAverage'])
        results3.append(result)

    # newline デフォルトでは 改行となっているため、何もしないように変更する必要あり
    with open('./ranking.csv', 'w', encoding='utf-8_sig', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(results3)

def main():
    get_item_list()
    get_min_and_max_value()
    get_rank()

# main()

if __name__ == "__main__":
    main()
