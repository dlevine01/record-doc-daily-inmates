import pandas as pd
from pathlib import Path

DATE_FORMAT = '%Y_%m_%d'

def combine_data() -> pd.DataFrame:
    data_dir = Path('./Daily data')

    data = pd.concat([
        pd.read_json(
            file
        )
        .assign(
            as_of_date = pd.to_datetime(
                file.stem,
                format=DATE_FORMAT
            )
        )
        for file
        in data_dir.iterdir()
    ])

    return data

if __name__ == "__main__":
    combine_data()