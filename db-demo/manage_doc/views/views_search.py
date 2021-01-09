"""
Search API
By RenYi, Liu Chang
"""
import json
import threading
import xml
from time import time

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from mrc_model.rpc_client import get_answer_from_server
from manage_doc.documents import ElasticSearchDocument
from back_end.settings import FILTER_TOO_LONG_DOC, MAX_ALLOWED_DOC_LEN, \
    MEDIUM_ANS, HIGH_ANS, ALLOW_MODEL_FAILURE
from ip_manager.ip_manager import ip_manager

from utils import get_user


def get_es_result(question: str, mode='multi_match'):
    """
    ask question to Elastic Search and get documents back

    Arguments:
        question: str, the question asked by user
        mode: str, match the documents with title and content (multi_match)
            or just match the content. (default multi_match)
    Return:
        es_result: Elastic Search returned douments iterable
        es_time: the time cost for Elastic Search
    """
    es_start = time()
    if mode == 'multi_match':
        es_result = ElasticSearchDocument.search() \
            .query("multi_match", query=question, fields=['title', 'content']) \
            .filter("term", status=0) \
            .execute()
    else:
        es_result = ElasticSearchDocument.search() \
            .query("match", content=question) \
            .filter("term", status=0) \
            .execute()
    es_finish = time()
    return es_result, es_finish - es_start


def refactor_es_hit(es_result):
    """
    refactor Elastic Search hit iterable into a list of dict,
    easy for transitting to JSON
    Arguments:
        es_result: the ES hit iterable
    Return:
        hit_meta: list of dict containing the hit info
    """
    hit_meta = []
    for hit in es_result:
        if FILTER_TOO_LONG_DOC:
            if len(hit.content) > MAX_ALLOWED_DOC_LEN:
                continue
        try:
            hit_src = hit.src
        except AttributeError:  # no src attribute
            hit_src = 8  # explained in src_dict
        hit_meta.append({'content': hit.content, 'doc_id': hit.id,
                         'es_score': hit.meta.score, 'title': hit.title, 'src': hit_src})
    return hit_meta


def get_model_result(question, hit_meta):
    """
    call model to get the answer for the question and from hit meta
    Arguments:
        question: str, the question asked by user
        hit_meta: the list of dict generated from ES hit iterable
    Return:
        model_response: list of dict containing the answer for the question
                (for more details, look into the get_answer_from_server docstring)
        model_time: the time cost for the model, in second
    """
    hosts = ip_manager.get_address(item='MODEL')
    model_start = time()
    model_response = get_answer_from_server(question,
                                            hit_meta, address=hosts)
    model_finish = time()
    return model_response, model_finish - model_start


def generate_response(model_response):
    """
    generate the list for response
    Arguments:
        model_response: list of dict containing the answer for the question
    Return:
         response_arr: list of dict with information needed by front end
    """
    response_arr = []  # JSON arr for responding to frontend
    src_dict = {-1: 'default', 0: 'user upload', 1: 'CMRC', 2: 'Baidu Search (trainset)',
                3: 'Baidu Zhidao (trainset)', 4: 'Baidu Search (devset)',
                5: 'Baidu Zhidao (devset)', 6: 'Baidu Search (testset)',
                7: 'Baidu Zhidao (testset)', 8: 'user upload before'}  # before means
    # before es listening to src
    for i, item in enumerate(model_response):
        if item['credit'] != 0 and item['model_score'] > 0:
            if item['model_score'] > 100:
                item['model_score'] = 100
            else:
                item['model_score'] = int(item['model_score'])
            if item['model_score'] >= HIGH_ANS:
                credit = 2
            elif item['model_score'] >= MEDIUM_ANS:
                credit = 1
            else:
                credit = 0
            try:
                item_src = src_dict[item['src']]
            except KeyError:
                item_src = 'user upload'
            response_arr.append({
                'id': i + 1,
                'content': item['content'],
                'title': item['title'],
                'answer': item['model_answer'],
                'grade': item['model_score'],
                'doc_id': item['doc_id'],
                'credit': credit,  # high, mid, low confidence, corresponding to 2, 1, 0
                'src': item_src
            })
    return response_arr


def search(request):
    """
    Query Interface
        1. get search question
        2. call model
        3. save user history
    """
    back_end_search_start = time()
    assert request.method == 'GET'
    question = request.GET.get('ask', default='范廷颂是什么时候被任为主教的？')

    es_result, es_time = get_es_result(question, mode='multi_match')

    hit_meta = refactor_es_hit(es_result)

    print('ES return time cost:', es_time, 's')
    print('ES total hits:', len(hit_meta))
    print('ES search question', question)

    if not hit_meta:  # len(hit_meta) == 0
        print('ES returned 0 docs, cancel model call')
        return JsonResponse({'code': 400, 'time': time() - back_end_search_start, 'data': []},
                            status=400, charset='utf-8', json_dumps_params={'ensure_ascii': False})
    try:
        model_response, model_time = get_model_result(question, hit_meta)
    except xml.parsers.expat.ExpatError as e:
        if not ALLOW_MODEL_FAILURE:
            raise e
        print('Model Call Failed, Return with code 400')
        return JsonResponse({'code': 400, 'time': time() - back_end_search_start, 'data': []},
                            status=400, charset='utf-8', json_dumps_params={'ensure_ascii': False})
    response_arr = generate_response(model_response)

    print('model return time cost:', model_time, 's')
    # print('Model Response', model_response)

    user_id = request.GET.get('user_id')
    save_history_start = time()

    # saving history in another thread, without blocking the main thread
    t = threading.Thread(target=save_history,
                         args=(user_id, model_response, back_end_search_start, question))
    t.start()

    back_end_search_finish = time()
    print('save history time cost:', back_end_search_finish - save_history_start, 's')
    print('whole backend time cost:', back_end_search_finish - back_end_search_start, 's')

    return JsonResponse({
        'code': 200,
        # search time rounded to 3 decimal bit (in second)
        'time': round(back_end_search_finish - back_end_search_start, 3),
        'data': response_arr
    }, status=200, charset='utf-8', json_dumps_params={'ensure_ascii': False})


def save_history(user_id, model_response, back_end_search_start, question):
    """
    Save user history
        1. check user id valid
        2. get user history json string
        3. json.loads into a python dict
        4. modify this dict
        5. json.dumps into a json string
        6. save this user into database

    Args:
        user_id: specify a user
        model_response: answers from model
        back_end_search_start: time when user begins search
        question: question that user asks

    Return:
        successful or not

    """
    user = get_user(user_id)
    # 出错了
    if not user:
        return False
    history_str = user.query_json
    # it means history_str is null
    if not history_str:
        history_str = '{"data": []}'

    json_dict = json.loads(history_str)
    # print(json_dict)
    append_dict = dict()
    append_dict['question'] = question
    append_dict['time'] = back_end_search_start
    append_dict['response'] = list()

    for item in model_response:
        append_dict['response'].append({
            'answer': item['model_answer'],
            'grade': item['model_score'],
            'content': item['content'],
            'doc_id': item['doc_id']
        })

    if len(json_dict['data']) < 100:
        json_dict['data'].append(append_dict)
    else:
        json_dict['data'].append(append_dict)
        json_dict['data'] = json_dict['data'][1:101]

    user.query_json = json.dumps(json_dict, ensure_ascii=False)
    try:
        user.full_clean()
        user.save()
    except ValidationError:
        return False
    return True
