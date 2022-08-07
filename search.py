from offer_search.offervault import offervault_search
from init import init
import pandas as pd


def search():
    search_results = pd.read_csv('./search_results.csv', encoding='utf-8', engine='python')
    offers_df = offervault_search('teenfinder')
    if not offers_df.empty:
        search_results = pd.concat([search_results, offers_df], ignore_index=True)
        search_results = search_results.drop_duplicates()
    search_results.to_csv('./search_results.csv', index=False)


if __name__ == '__main__':
    init()
    search()
