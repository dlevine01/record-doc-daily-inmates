import pandas as pd

import combine_data

def summarize_data() -> pd.DataFrame:
    data = combine_data.combine_data()

    inmates_in_custody = (
        data
        .groupby('as_of_date')
        ['inmateid']
        .nunique()
        .rename('total_inmates_in_custody')
    )

    bradh_inmates_in_custody = (
        data
        [data['bradh'].eq('Y')]
        .groupby('as_of_date')
        ['inmateid']
        .nunique()
        .rename('bradh_inmates_in_custody')
    )
    
    summary_data = (
        inmates_in_custody
        .to_frame()
        .join(
            bradh_inmates_in_custody,
            on='as_of_date',
            how='left'
        )
        .reset_index()
    )

    return summary_data

def save_summary_data(summary_data):
    
    (
        summary_data
        .melt(
            id_vars='as_of_date',
            var_name='category',
            value_name='count'
        )
        .to_json(
            'Summary data/summary_data.json', 
            orient='records', 
            date_format='iso'
        )
    )

if __name__ == "__main__":
    summary_data = summarize_data()
    save_summary_data(summary_data)