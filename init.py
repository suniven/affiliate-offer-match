import pandas as pd
from tqdm import main
import os


def init():
    if not os.path.exists('./search_result.csv'):
        df = pd.DataFrame(columns=[
            'url', 'landing_page', 'keyword', 'offer_url', 'offer_title', 'offer_payout', 'offer_create_time',
            'offer_update_time', 'offer_category', 'offer_geo', 'offer_network', 'offer_description',
            'offer_landing_page'
        ])
        df.to_csv('./search_results.csv', index=False)


if __name__ == '__main__':
    init()