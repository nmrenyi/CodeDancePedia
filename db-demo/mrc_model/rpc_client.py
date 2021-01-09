# coding=utf-8

'''Model API, by DAC'''

from xmlrpc.client import ServerProxy
import json
import re

def get_answer_from_server(question: str, hit_meta: list, address: str):
    '''
    question is the question str of asked question

    hit_meta is the list of dict
    the dict has the following fields:
        'content': doc content(str)
        'doc_id': document id(int)
        'es_score': document elastic search score


    the return value is a list of dict. Besides the fields above,
    it has the following extra fields:

    'model_answer': model answer from the document w.r.t the question
    'model_score': model answer score
    'start_index': the start position of model answer in a document
    'end_index': the end position of model answer in a document
    'credit': int type, credit label of the document. Specifiaclly,
        '3' means assured answer (Unique);
        '2' means referrible answer;
        '1' means useless answer

    the list is sorted descendently by the model_score
    '''
    server = ServerProxy("http://" + address)
    for i, dic in enumerate(hit_meta):
        hit_meta[i]['content'] = re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+", u"", dic['content'])
        hit_meta[i]['title'] = re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+", u"", dic['title'])

    return server.get_string(json.dumps([question, hit_meta], ensure_ascii=False))

def test_rpc(address="152.136.231.113", port="31001"):
    '''
    Record RPC connecting time
    '''
    server = ServerProxy("http://" + address + ":" + port)
    return server.timecost_test()

# Usage:
# time_start = time.time()
# print(test_rpc())
# time_end = time.time()
# print("Elasped time: ", time_end-time_start)
