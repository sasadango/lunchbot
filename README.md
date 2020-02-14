# 御苑ランチボット

## Overview
Cloud RunとCloud Storageを使用したSlackボット  

## Description
`gyoen-lunchbot`：ボット本体  
`use-api`：ぐるなびAPIを叩くやつ

## Requirment
GCPアカウント  
Docker  
ぐるなびAPIキー

## Usage
### GCPサービスの準備
プロジェクトの作成  
Cloud Build, Cloud Run, Cloud Storageサービスを利用可能にする

### ぐるなびAPIからレストラン情報を取得
`use-api/api-grunabi.py` の `apikey`にぐるなびAPIキーをセット  
`$ python api-grunabi.py`  
吐き出されたjsonファイルをCloud Storageにアップロード  

### イメージビルド＆デプロイ
#### コンテナイメージをビルド
`gyoen-lunchbot` に移動し、以下のコマンドを叩く
```
$ gcloud builds submit --tag gcr.io/[PROJECT-ID]/gyoen
```
`PROJECT-ID` 取得方法
```
$ gcloud config get-value project
```
これで Container Registry にイメージが保存される

#### Cloud Runにデプロイする
```
$ gcloud beta run deploy --image gcr.io/[PROJECT-ID]/gyoen
```
- ターゲットプラットフォーム
- リージョン
- サービス名  

以上を入力すると、エンドポイントが作成される  


### ローカル環境でテストしたい場合  
cloud storageにあるデータにアクセスする必要があります  
`gyoen-lunchbot/tmp/key` にサービスアカウントキーを配置しておきます

     PORT=8080 && docker run \
       -p 8080:${PORT} \
       -e PORT=${PORT} \
       -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/key/[FILE_NAME].json \
       -v $GOOGLE_APPLICATION_CREDENTIALS:/tmp/key/[FILE_NAME].json:ro \
       gcr.io/[PROJECT_ID]/[IMAGE]

`--environment`（`-e`）フラグを使用して、コンテナ内に `GOOGLE_ACCOUNT_CREDENTIALS` 変数を設定します。  

`--volume`（`-v`）フラグを使用して、認証情報のファイルをコンテナに挿入します。
この操作を行う前に、マシンに `GOOGLE_APPLICATION_CREDENTIALS` 環境変数が設定されている必要があります。 

## Reference
[Cloud Run](https://cloud.google.com/run?hl=ja)

[コンテナ イメージをローカルでテストする](https://cloud.google.com/run/docs/testing/local?hl=ja)

[ぐるなびAPI](https://api.gnavi.co.jp/api/)

[cloud runとslackbotで作るおすすめランチスポットボット](https://qiita.com/wcsakurai/items/27fa9cebf22ca7009661)
