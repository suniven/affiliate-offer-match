from offer_search.offervault import offervault_search
from offer_search.odigger import odigger_search
from offer_search.affplus import affplus_search
import pandas as pd
import datetime


def search(keyword_list):
    for keyword in keyword_list:
        offervault_search_results = offervault_search(keyword)
        save_name = './results/result_' + datetime.datetime.now().strftime('%Y-%m-%d') + '.txt'
        if offervault_search_results:
            with open(save_name, 'a', encoding='utf-8') as f:
                for result in offervault_search_results:
                    f.write("{0}\t{1}\n".format(keyword, result))
        odigger_search_results = odigger_search(keyword)
        if odigger_search_results:
            with open(save_name, 'a', encoding='utf-8') as f:
                for result in odigger_search_results:
                    f.write("{0}\t{1}\n".format(keyword, result))
        affplus_search_results = affplus_search(keyword)
        if affplus_search_results:
            with open(save_name, 'a', encoding='utf-8') as f:
                for result in affplus_search_results:
                    f.write("{0}\t{1}\n".format(keyword, result))


if __name__ == '__main__':
    df = pd.read_csv('./keyword.csv', engine='python')
    keyword_list = df.iloc[:, 0].values
    search(keyword_list)
