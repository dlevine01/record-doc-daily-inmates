import requests
import os
import datetime
import json
import logging
import sys
from logging.handlers import RotatingFileHandler

OUT_DATE_FORMAT = '%Y_%m_%d'


def configure_logging() -> None:
    log_dir = os.path.join(os.getcwd(), 'Logs')
    os.makedirs(log_dir, exist_ok=True)

    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    handlers = [logging.StreamHandler(sys.stdout)]
    handlers.append(
        RotatingFileHandler(
            os.path.join(log_dir, 'get_data.log'),
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding='utf-8',
        )
    )

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=handlers,
    )

    for handler in handlers:
        handler.setFormatter(log_formatter)


def main() -> None:
    open_data_app_token = os.getenv('OPEN_DATA_APP_TOKEN')
    if not open_data_app_token:
        logging.warning(
            'OPEN_DATA_APP_TOKEN is not set. Requests may be rate-limited or rejected.'
        )

    headers = {'X-App-Token': open_data_app_token} if open_data_app_token else {}
    params = {'$limit': 10000000}

    data_url = 'https://data.cityofnewyork.us/resource/7479-ugqb.json'
    metadata_url = 'https://data.cityofnewyork.us/api/views/metadata/v1/7479-ugqb'

    logging.info('Fetching data from %s', data_url)
    data_r = requests.get(data_url, headers=headers, params=params)
    data_r.raise_for_status()
    data = data_r.json()
    logging.info('Fetched %s records', len(data) if isinstance(data, list) else 1)

    logging.info('Fetching metadata from %s', metadata_url)
    metadata_r = requests.get(metadata_url)
    metadata_r.raise_for_status()

    data_updated_date_str = metadata_r.json().get('dataUpdatedAt')
    data_updated_datetime = datetime.datetime.strptime(
        data_updated_date_str, '%Y-%m-%dT%H:%M:%S+0000'
    )
    data_updated_formatted = data_updated_datetime.strftime(OUT_DATE_FORMAT)

    output_dir = 'Daily data'
    output_path = os.path.join(output_dir, f'{data_updated_formatted}.json')
    os.makedirs(output_dir, exist_ok=True)

    logging.info('Saving data to %s', output_path)
    with open(output_path, 'w', encoding='utf-8') as out_file:
        json.dump(data, out_file)

    logging.info('Saved data successfully.')


if __name__ == '__main__':
    configure_logging()
    try:
        main()
    except Exception:
        logging.exception('Failed to fetch or save data')
        raise
