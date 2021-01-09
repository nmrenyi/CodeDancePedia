# coding=utf-8

'''Support for multithreading'''

import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from rpc_client import get_answer_from_server
sns.set()

if __name__ == "__main__":
    plt.rcParams['savefig.dpi'] = 100
    plt.rcParams['figure.dpi'] = 100
    times, host = 10, '152.136.231.113:31001'

    f = open('doc_example', 'r', encoding='utf-8')
    document = f.readlines()
    f.close()
    QUESTION = '猫屎咖啡是什么'
    res_dict = {'Length':[50, 100, 150, 200, 250, 300, 350, 400, 450, 500]}
    for num in range(10):
        doc_num = num + 1
        res_dict[doc_num] = []
        for length in range(10):
            doc_len = (length + 1) * 50
            print(doc_num, " ", doc_len)
            hit_meta = []
            for i in range(doc_num):
                hit_meta.append({'content':document[i%10][:doc_len], 'doc_id':0, 'es_score':0})
            time_start = time.time()
            for i in range(times):
                get_answer_from_server(question=QUESTION, hit_meta=hit_meta, address=host)
            time_end = time.time()
            res_dict[doc_num].append((time_end-time_start)/times)
            time.sleep(0.5)
    plot_df = pd.DataFrame(res_dict)
    plot_df.set_index(['Length'], inplace=True)
    ax = sns.heatmap(plot_df, cmap="YlGnBu", annot=True, fmt=".4f",
                     annot_kws={'size':8}, linewidths=.1)
    label_y = ax.get_yticklabels()
    plt.setp(label_y, rotation=360)
    plt.xlabel('Number of docments')
    plt.title('Running time @ Docker')
    plt.savefig('plt', dpi=300)
