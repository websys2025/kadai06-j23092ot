import requests
import pandas as pd

API_URL = "https://api.jartic-open-traffic.org/geoserver"
params = {
    "service": "WFS", #地理データを取得してくるサービス
    "version": "2.0.0", #バージョン情報
    "request": "GetFeature", #交通量情報のデータ
    "typeNames": "t_travospublic_measure_5m",  # 5分間交通量データ
    "srsName": "EPSG:4326", #緯度経度
    "outputFormat": "application/json",
    "exceptions": "application/json",
    "cql_filter": "道路種別='3' AND 時間コード=202506150900 AND BBOX(ジオメトリ,139.65,35.65,139.75,35.75,'EPSG:4326')"
}


response = requests.get(API_URL, params=params)
data = response.json()

rows = []
for feature in data["features"]:
    props = feature["properties"]
    if "geometry" in feature and feature["geometry"]:
        coords = feature["geometry"]["coordinates"][0]
        props["longitude"], props["latitude"] = coords
    rows.append(props)
df = pd.DataFrame(rows)

print(df.head())
