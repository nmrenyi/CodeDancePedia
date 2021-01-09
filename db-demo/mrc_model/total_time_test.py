# coding=utf-8

'''Time-cost testing script, by dac'''

import time
import argparse
from rpc_client import get_answer_from_server

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--times', type=int, default=10,
        help='Testing times of sending documents. Default: 10')
    parser.add_argument('--docnum', type=int, default=10,
        help='Number of documents. Default: 10')
    parser.add_argument('--host', type=str, default='152.136.231.113:31001',
        help='Host to connect. Default: TencentCloud')
    parser.add_argument('--doclen', type=int, default=1000,
        help='Maximum length of every document')
    args = parser.parse_args()

    times, doc_num, host, doc_len = args.times, args.docnum, args.host, args.doclen

    f = open('doc_example', 'r', encoding='utf-8')
    document = f.readlines()
    f.close()
    QUESTION = '竹醋液是什么'
    hit_meta = []
    for i in range(doc_num):
        hit_meta.append({'content':document[i%10][:doc_len], 'doc_id':0, 'es_score':0,
                        'title':'test', 'src':'test'})

    avg_len = sum([len(meta['content']) for meta in hit_meta]) / len(hit_meta)
    print('Average length of document: ', avg_len)

    time_start = time.time()
    for i in range(times):
        get_answer_from_server(question=QUESTION, hit_meta=hit_meta, address=host)
    time_end = time.time()
    print("Elasped time per prediction: ", (time_end-time_start)/times)
