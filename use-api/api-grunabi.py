import requests
import json

# ぐるなびAPI Key
apikey = ""

pages = 10

# API format
api = "https://api.gnavi.co.jp/RestSearchAPI/v3/?keyid={key}&latitude=35.688623&longitude=139.710696&lunch=1&hit_per_page=100&offset_page={page}"

# レストラン情報を取得する
for page in range(1, pages):
    # APIのURLを取得
    url = api.format(key=apikey, page=page)

    # ぐるなびAPIにリクエストを送信して結果を取得する
    r = requests.get(url)

    # 結果はJSON形式なのでデコード
    data = json.loads(r.text)

    # 結果を画面に表示
    json_file = open('restaurant_{}.json'.format(page), 'w')

    json.dump(data, json_file, indent=2)

    if (data["total_hit_count"] <= data["hit_per_page"]):
        break
