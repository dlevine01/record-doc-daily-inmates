import requests
import os
import datetime
import json

OPEN_DATA_APP_TOKEN = os.getenv('OPEN_DATA_APP_TOKEN')

headers = {
    'X-App-Token': OPEN_DATA_APP_TOKEN
}

params = {
    '$limit':10000000
}

# get data

data_url = 'https://data.cityofnewyork.us/resource/7479-ugqb.json'

metadata_url = 'https://data.cityofnewyork.us/api/views/metadata/v1/7479-ugqb'

data_r = requests.get(data_url, headers=headers, params=params)

data_r.raise_for_status()

data = data_r.json()

# get metadata
metadata_r = requests.get(metadata_url)

OUT_DATE_FORMAT = '%Y_%m_%d'

data_updated_date_str = metadata_r.json().get('dataUpdatedAt')
data_updated_datetime = datetime.datetime.strptime(data_updated_date_str, '%Y-%m-%dT%H:%M:%S+0000')
data_updated_formatted = datetime.datetime.strftime(data_updated_datetime, OUT_DATE_FORMAT)

# save

with open(data_updated_formatted + '.json', 'w') as out_file:
    json.dump(data, out_file)
