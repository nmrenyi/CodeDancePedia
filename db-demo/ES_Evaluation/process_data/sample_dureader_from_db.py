"""
sample dureader from db
"""
import os
import json
import pandas as pd
from tqdm import tqdm


df_path = '../DuReader_reformatted/DuReader_for_db.csv'
# df_path = '../DuReader_reformatted/DuReader_demo.csv'

df = pd.read_csv(df_path, sep='\t', index_col=0)
sample_len = 100
sampled_df = df.sample(n=sample_len, axis=0, random_state=123)

sampled_q_list = sampled_df['question'].tolist()
ground_truth_list = []

for q in tqdm(sampled_q_list):
    ground_truth = df[df['question'] == q]['doc_paragraph'].tolist()
    ground_truth_list.append(json.dumps(ground_truth, ensure_ascii=False))

sampled_df.drop(columns=['doc_paragraph'], inplace=True)
sampled_df['ground_truth'] = ground_truth_list

new_df_path = os.path.splitext(df_path)[0] + '-sample' + str(sample_len) + '.csv'
sampled_df.to_csv(new_df_path, sep='\t')
print('file successfully saved to ', new_df_path)
