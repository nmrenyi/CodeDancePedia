"""
process dureader dataset into more formatted csv file
"""
import json
from time import time
import pandas as pd
from tqdm import tqdm

if __name__ == '__main__':
    start_time = time()
    docs_info = list()
    srcs = ['search.train', 'zhidao.train', 'search.dev',
            'zhidao.dev', 'search.test', 'zhidao.test', ]
    for src in srcs:
        print('processing', src, '...')
        file_path = '../DuReader_raw/' + src + '.preprocessed.json'
        start_load_time = time()
        with open(file_path, encoding='utf8') as f:
            file_info = f.readlines()
            finish_load_time = time()
            print('load', src, 'time cost', finish_load_time - start_load_time, 's')
            for line in tqdm(file_info):
                item = json.loads(line)
                q_text = item['question']
                q_type = item['question_type']
                q_id = item['question_id']
                q_fact_or_opinion = item['fact_or_opinion']
                doc_titles = [x['title'] for x in item['documents']]
                doc_paragraphs = [json.dumps(x['paragraphs'], ensure_ascii=False)
                                  for x in item['documents']]

                try:
                    doc_selected = [1 if x['is_selected'] else 0 for x in item['documents']]
                except KeyError:
                    doc_selected = [''] * len(item['documents'])
                try:
                    doc_most_related_paras = [x['paragraphs'][x['most_related_para']]
                                              for x in item['documents']]
                except KeyError:
                    doc_most_related_paras = [''] * len(item['documents'])

                try:
                    answers = json.dumps(item['answers'], ensure_ascii=False)
                except KeyError:
                    answers = ''
                for i, title in enumerate(doc_titles):
                    docs_info.append({
                        'question': q_text,
                        'question_id': q_id,
                        'question_type': q_type,
                        'question_fact_opinion': q_fact_or_opinion,
                        'doc_title': title,
                        'doc_selected': doc_selected[i],
                        'doc_paragraphs': doc_paragraphs[i],
                        'doc_most_related_paragraph': doc_most_related_paras[i],
                        'answers': answers,
                        'src': src
                    })

    df = pd.DataFrame(docs_info)
    save_path = '../DuReader_reformatted/DuReader_reformatted.csv'
    df.to_csv(save_path, sep='\t')
    end_time = time()
    print('file successfully saved to ', save_path)
    print('time cost ', end_time - start_time, 's')
