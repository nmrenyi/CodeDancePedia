"""
Elastic Search Precision and Recall Evaluation
By RenYi
"""
import os

import numpy as np
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from tqdm import trange


def calc_precision(document, returned_docs, top_k):
    """

    Args:
        document: the ground truth doc
        returned_docs: returned docs from elastic search

    Returns:
        precision (float) of this search
    """

    if document in returned_docs[0:top_k]:
        return 1 / top_k
    # document is not in returned docs or len(returned_docs) == 0
    return 0


def calc_recall(document, returned_docs, top_k):
    """

    Args:
        document: the related document (str)
                    there is only one related document in cmrc for each question
        returned_docs:  returned docs from elastic search

    Returns:
        recall (float) of this search

    """

    if document in returned_docs[0:top_k]:
        return 1
    return 0


def get_precision_recall(search, question_list, document_list, top_k):
    """

    Args:
        search: search object in elastic search
        question_list: questions
        document_list: the specific document for the question

    Returns:
        precision_list: precision for the questions
        recall_list: recall for the questions
    """
    precision_list = list()
    recall_list = list()
    length = len(question_list)
    for i in trange(length):
        question = question_list[i]
        document = document_list[i]
        response = search.query("multi_match", query=question, fields=['title', 'content']) \
                         .filter("term", status=0) \
                         .execute()
        # response = search.query("match", content=question) \
        #                  .filter("term", status=0) \
        #                  .execute()
        returned_docs = [hit.content for hit in response]
        precision_list.append(calc_precision(document, returned_docs, top_k))
        recall_list.append(calc_recall(document, returned_docs, top_k))

    return precision_list, recall_list


def main():
    """
    main function for Elastic Search Precision and Recall Evaluation
    """
    client = Elasticsearch(['152.136.231.113:32000'])
    search = Search(using=client, index="mydocument")
    top_k = 1
    df_path = './cmrc_reformatted/cmrc_reformatted.csv'
    df = pd.read_csv(df_path, sep='\t', index_col=0).dropna()  # drop 2 nan question and 8 nan title
    precision_list, recall_list = get_precision_recall(search, df['question'].tolist(),
                                                       df['paragraph_context'].tolist()
                                                       , top_k)
    # print('precision list', precision_list)
    # print('recall list', recall_list)
    print('average precision:', np.mean(precision_list))
    print('average recall:   ', np.mean(recall_list))
    df['precision'] = precision_list
    df['recall'] = recall_list
    new_df_path = os.path.splitext(df_path)[0] + '-precision-recall@' + str(top_k) + '.csv'
    df.to_csv(new_df_path, sep='\t')
    print('file successfully saved to ', new_df_path)


if __name__ == '__main__':
    main()
