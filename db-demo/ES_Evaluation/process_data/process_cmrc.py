"""
process cmrc dataset into more formatted csv file
"""
import json

import pandas as pd
from tqdm import tqdm


def process_qa(qa, item_info, paragraph_id, paragraph_context, question_src):
    """
    process one question and answer
    with previous information(including the context, i.e. the document) into a dict
    """
    item_id = item_info['item_id']
    item_title = item_info['item_title']
    result = {
        'question': qa['question'],
        'answer': qa['answers'][0]['text'],
        'question_id': qa['id'],
        'paragraph_context': paragraph_context,
        'paragraph_id': paragraph_id,
        'item_id': item_id,
        'item_title': item_title,
        'src': question_src
    }
    return result


def process_paragraph(item_id, item_title, item_paragraph, question_src):
    """
    process a paragraph
    """
    paragraph_id = item_paragraph['id']
    paragraph_context = item_paragraph['context']
    qa_result_list = list()
    for qa in item_paragraph['qas']:
        qa_result_list.append(
            process_qa(qa, {'item_id': item_id, 'item_title': item_title},
                       paragraph_id, paragraph_context, question_src))
    return qa_result_list


def process_single_item(item, question_src):
    """

    Args:
        item: an item in data array, including an id and a title

    Returns:

    """
    item_id = item['id']
    item_title = item['title']
    item_info = list()
    for paragraph in item['paragraphs']:
        item_info += process_paragraph(item_id, item_title, paragraph, question_src)
    return item_info


def extract_doc_qa(data_pack: dict, question_src: str):
    """
    Args:
        data_pack: one item of a document in cmrc dataset
        question_src: source of the question

    Returns:
        a list of dicts containing one question, one answer, one doc, one id
    """
    doc_qa_list = list()
    for item in tqdm(data_pack):
        doc_qa_list += process_single_item(item, question_src)

    return doc_qa_list


if __name__ == '__main__':
    src_list = ['cmrc2018_train', 'cmrc2018_dev', 'cmrc2018_trial']
    data_list = list()
    for src in src_list:
        file_path = './cmrc_raw/' + src + '.json'
        with open(file_path, encoding='utf8') as f:
            data = json.load(f)
            data_list += extract_doc_qa(data['data'], src)
    df = pd.DataFrame(data_list)
    df.to_csv('./cmrc_reformatted/cmrc_reformatted.csv', sep='\t')
