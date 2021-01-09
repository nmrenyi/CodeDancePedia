"""
prepare dureader dataset for db processing convenience
"""
import json
import pandas as pd
from tqdm import tqdm

SINGLE_PARAGRAPH = False
K = 500
L = 150

def add_to_db(result_list, question, title, doc, src):
    """
    add doc item into result list
    """
    result_list.append({
        'question': question,
        'doc_title': title,
        'doc_paragraph': doc,
        'src': src,
    })


def main():
    """
    main function for process dureader for db
    """
    df = pd.read_csv('../DuReader_reformatted/DuReader_reformatted.csv', sep='\t', index_col=0)
    result_list = list()
    paragraph_total_len = 0
    paragraph_cnt = 0
    if SINGLE_PARAGRAPH:
        for _, row in tqdm(df.iterrows(), total=len(df)):
            paragraph_list = (json.loads(row['doc_paragraphs']))
            for paragraph in paragraph_list:
                add_to_db(result_list, row['question'], row['doc_title'], paragraph, row['src'])
                paragraph_total_len += len(paragraph)
                paragraph_cnt += 1
    else:
        for _, row in tqdm(df.iterrows(), total=len(df)):
            doc = json.loads(row['doc_paragraphs'])
            doc_context = ''.join(doc)
            if len(doc_context) < K:  # doc not too long, add directly
                add_to_db(result_list, row['question'], row['doc_title'], doc_context, row['src'])
                paragraph_cnt += 1
                paragraph_total_len += len(doc_context)
            else:  # doc too long, split into paragraphs
                unit_doc = ''
                for para in doc:
                    if len(unit_doc) + len(para) > L:  # meet minimum length requirement
                        unit_doc += para
                        add_to_db(result_list, row['question'],
                            row['doc_title'], unit_doc, row['src'])
                        paragraph_cnt += 1
                        paragraph_total_len += len(unit_doc)
                        unit_doc = ''
                    else:
                        unit_doc += para
                if unit_doc:  # len(unit_doc) != 0
                    add_to_db(result_list, row['question'], row['doc_title'], unit_doc, row['src'])
                    paragraph_cnt += 1
                    paragraph_total_len += len(unit_doc)

    result_df = pd.DataFrame(result_list)
    file_out_path = '../DuReader_reformatted/DuReader_for_db' +\
                    ('SinglePara' if SINGLE_PARAGRAPH else 'CombinedPara' + str(K) + '-' +str(L)) +\
                    '.csv '
    result_df.to_csv(file_out_path, sep='\t')
    print('file successfully saved to ', file_out_path)
    print('paragraph avg len: ', paragraph_total_len / paragraph_cnt)


if __name__ == '__main__':
    main()
