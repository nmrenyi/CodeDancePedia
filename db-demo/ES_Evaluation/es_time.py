"""
Elastic Search Time Evaluation
"""
import os
from time import time

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import numpy as np
import pandas as pd
from tqdm import tqdm


def print_search_response(response):
    """
    print response for debug
    """
    # for hit in response:
    #     print('score:', hit.meta.score, '\tid:', hit.id, '\tcontent:', hit.content)


def get_question_time_list(search, question, epoch):
    """

    Args:
        search: search object for elastic search
        question: str for question
        epoch: repeat ask times

    Returns:
        a list of elapsed time for asking this question
        length of this list equals to epoch
    """
    time_list = list()
    for _ in range(epoch):
        start_search = time()
        response = search.query("match", content=question).filter("term", status=0).execute()
        print_search_response(response)
        end_search = time()
        time_list.append(end_search - start_search)
    return time_list


def get_question_info(search, question_list, epoch):
    """

    Args:
        search: search object for elastic search
        question_list: a list of questions to be asked
        epoch: repeat ask times

    Returns:
        a list of average time cost on each question
        a list of variance on time cost on each question

    """
    time_avg_list = list()
    time_var_list = list()
    for question in tqdm(question_list):
        time_list = get_question_time_list(search, question, epoch)
        time_avg_list.append(np.mean(time_list))
        time_var_list.append(np.var(time_list))
    return time_avg_list, time_var_list


def main():
    """
    main function for Elastic Search Time Evaluation
    """
    client = Elasticsearch(['152.136.231.113:32004'])
    search = Search(using=client, index="mydocument")
    # initial search to get connected, avoid forehead cost in evaluation
    search.query("match", content='麦克米兰计划是如何产生的').filter("term", status=0).execute()

    df_path = './DuReader_reformatted/DuReader_for_dbCombinedPara500-150-sample10000.csv'
    df = pd.read_csv(df_path, sep='\t', index_col=0).dropna()  # drop 2 nan question and 8 nan title
    epoch = 1
    time_avg_list, time_var_list = get_question_info(search, df['question'].tolist(), epoch=epoch)
    print('total avg time average:', np.mean(time_avg_list))
    print('total avg time variance:', np.mean(time_var_list))

    df['time_avg'] = time_avg_list
    df['time_var'] = time_var_list
    new_df_path = os.path.splitext(df_path)[0] + '-epoch-' + str(epoch) + '.csv'
    df.to_csv(new_df_path, sep='\t')
    print('file successfully saved to ', new_df_path)


if __name__ == '__main__':
    main()
