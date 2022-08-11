from offer_search.offervault import offervault_search
from offer_search.odigger import odigger_search
import pandas as pd
import datetime


def search(keyword_list):
    for keyword in keyword_list:
        results = offervault_search(keyword)
        save_name = './results/result_' + datetime.datetime.now().strftime('%Y-%m-%d') + '.txt'
        if results:
            with open(save_name, 'a', encoding='utf-8') as f:
                for result in results:
                    f.write("{0}\t{1}\n".format(keyword, result))
        results = odigger_search(keyword)
        if results:
            with open(save_name, 'a', encoding='utf-8') as f:
                for result in results:
                    f.write("{0}\t{1}\n".format(keyword, result))


if __name__ == '__main__':
    df = pd.read_csv('./keyword.csv', engine='python')
    keyword_list = df.iloc[:, 0].values
