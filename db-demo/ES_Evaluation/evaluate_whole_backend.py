"""
Evaluate whole backend time script
"""
import os
from time import time
import requests
import pandas as pd
from tqdm import tqdm


def ask(url, question):
    """

    Args:
        url: url for asking
        question: question str

    Returns:
        response object

    """
    response = requests.get(url=url, params={'ask': question})
    return response


def get_time_avg(question_list, epoch):
    """

    Args:
        question_list: list for questions
        epoch: int, repeat time

    Returns:
        total_time_list: the time for each question
            including the network communication time
        back_end_time_list: the time for each question
            only the backend time

    """
    url = 'https://db-demo-codedance.app.secoder.net/docs/search'
    total_time_list = []
    back_end_time_list = []
    for question in tqdm(question_list, total=len(question_list)):
        total_time_sum = 0.0
        back_end_time_sum = 0.0
        for _ in range(epoch):
            start_time = time()
            response = ask(url, question)
            finish_time = time()
            total_time_sum += finish_time - start_time
            back_end_time_sum += response.json()['time']

        total_time_list.append(total_time_sum / epoch)
        back_end_time_list.append(back_end_time_sum / epoch)

    return total_time_list, back_end_time_list


def main():
    """
    main function for backend time evaluation
    """
    df_path = './DuReader_reformatted/DuReader_for_dbCombinedPara500-150-sample10000.csv'
    df = pd.read_csv(df_path, sep='\t', index_col=0).dropna()  # drop 2 nan question and 8 nan title
    epoch = 5  # about 6 hours
    total_time_list, back_end_time_list = get_time_avg(df['question'].tolist(), epoch)
    df['time_avg'] = total_time_list
    df['backend_time'] = back_end_time_list
    new_df_path = os.path.splitext(df_path)[0] + '-whole-epoch-' + str(epoch) + '.csv'
    df.to_csv(new_df_path, sep='\t')
    print('file successfully saved to ', new_df_path)


if __name__ == '__main__':
    main()
