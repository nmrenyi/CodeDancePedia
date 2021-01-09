"""
Get Answer Position in DuReader Evaluation
"""
import os
import json
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from tqdm import tqdm


def get_pred_list(search, q):
    """

    Args:
        search: search object for Elastic Search
        q:question (str)

    Returns:
        ElasticSearch hit doc contents

    """
    response = search.query("multi_match", query=q, fields=['title', 'content']) \
        .filter("term", status=0) \
        .execute()
    return [hit.content for hit in response]


def get_ans_pos(search, q_list, truth_str_list):
    """

    Args:
        search: search object for Elastic Search
        q_list: question list, list of str
        truth_str_list: ground truth list, list of str

    Returns:
        result: list of answer position
        total_rela_cnt: list total relevant doc cnt
        retrieved_rela_cnt: list of total retrieved relevant cnt

    """
    result = []
    total_rela_cnt = []
    retieved_rela_cnt = []
    for i, q in tqdm(enumerate(q_list), total=len(q_list)):
        truth_list = json.loads(truth_str_list[i])
        total_rela_cnt.append(len(truth_list))
        pred_list = get_pred_list(search, q)
        performance = []
        for j, pred in enumerate(pred_list):
            if pred in truth_list:
                performance.append(j + 1)
        result.append(performance)
        retieved_rela_cnt.append(len(performance))
    return result, total_rela_cnt, retieved_rela_cnt


def main():
    """
    main function for Elastic Search Precision and Recall Evaluation
    """
    client = Elasticsearch(['152.136.231.113:32004'])
    search = Search(using=client, index="mydocument")
    df_path = './DuReader_reformatted/DuReader_for_db-sample10000.csv'
    df = pd.read_csv(df_path, sep='\t', index_col=0).dropna()
    answer_position_list, total_rela_cnt, retieved_rela_cnt = \
        get_ans_pos(search, df['question'].tolist(), df['ground_truth'].tolist())
    df['ans_pos'] = answer_position_list
    df['total_relevant_cnt'] = total_rela_cnt
    df['retrieved_rela_cnt'] = retieved_rela_cnt
    order = ['question', 'total_relevant_cnt', 'retrieved_rela_cnt',
             'ans_pos', 'src', 'ground_truth']
    df = df[order]
    new_df_path = os.path.splitext(df_path)[0] + '-anspos' + '.csv'
    df.to_csv(new_df_path, sep='\t')
    print('file successfully saved to ', new_df_path)


if __name__ == '__main__':
    main()
