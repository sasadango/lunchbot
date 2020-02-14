import random
import json

from flask import Flask

from google.cloud import storage


app = Flask(__name__)

template = """
<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8"/>
<meta property="og:title" content="さーて、今日のランチはー！" />
<meta property="og:type" content="article" />
<meta property="og:description" content="「 {} 」{} {} {}" />
<mete property="og:url" content="{}" />
<meta property="og:image" content="{}" />

</head>
</html>
"""


def select_restaurant(gnavi_json):
    total = gnavi_json["total_hit_count"]
    return random.randrange(total - 1)


def extract_content(gnavi_json, index):
    restaurant = gnavi_json["rest"][index]
    name = restaurant["name"]
    category = restaurant["category"]
    url = restaurant["url"]
    image = restaurant["image_url"]["shop_image1"]
    pr = restaurant["pr"]["pr_short"]

    return template.format(name, category, url, pr, url, image)


def download_blob(bucket_name, filename):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(filename)
    content = blob.download_as_string().decode('utf-8')
    return content


@app.route('/')
def now():
    bucket_name = 'gnavi-data'
    filename = 'restaurant.json'

    gnavi_data = download_blob(bucket_name, filename)
    gnavi_json = json.loads(gnavi_data)
    index = select_restaurant(gnavi_json)

    return extract_content(gnavi_json, index)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
