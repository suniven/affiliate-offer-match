import pandas as pd
from tqdm import main
import os


def init():
    if not os.path.exists('./search_result.csv'):
        df = pd.DataFrame(columns=[
            'keyword', 'url', 'title', 'payout', 'offer_create_time', 'offer_update_time', 'category', 'geo', 'network',
            'description', 'landing_page'
        ])
        df.to_csv('./search_results.csv')


if __name__ == '__main__':
    init()