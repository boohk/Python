# -*- coding: utf-8 -*-
import json
import re

import numpy as np
import pandas as pd
from pandas.io.json import json_normalize  # package for flattening json in pandas df


# Json 파일을 df 형태로 전처리하는 함수
def define_object(path):
    # Getting values using key on dictionary format
    def extract_items(dict_data, keys_list):
        new_dict = {}
        for i in dict_data.keys():
            if i in keys_list:
                new_dict[i] = dict_data[i]
        return new_dict

    defined_object_df = pd.DataFrame()
    try:
        with open(path, encoding='UTF8') as f:
            # 1. load .Json
            data = json.load(f)
            # 2. Extract data (What will we use?)
            keys = ['count', 'edges']
            j1 = extract_items(data, keys)

            # 3. Normalize Json format
            j2 = json_normalize(j1['edges'])
            # 4. Drop columns that don't be needed and then rename columns
            original = set(j2.columns)
            fixed = {'node.display_url', 'node.edge_liked_by.count', 'node.edge_media_to_caption.edges',
                     'node.edge_media_to_comment.count', 'node.id', 'node.owner.id', 'node.taken_at_timestamp'}
            j2.drop(list(original - fixed), axis=1, inplace=True)

            # Clear sets that don't use anymore
            original.clear()
            fixed.clear()

            # rename columns
            j2.columns = ['contents_url', 'like_count', 'post', 'comment_count', 'post_id', 'user_id', 'timeStamp']

            # 5. Extracting tags form text (use regex)
            tag_list = []
            for row in j2['post']:
                if not bool(row):
                    tag_list.append(None)
                else:
                    re_row = row[0]['node']['text']
                    if re_row.find("#") > -1:
                        p = re.compile('#([^#\s]+)')
                        tag_from_row = p.findall(re_row)
                        tag_from_row = [x.strip('#') for x in tag_from_row]
                        row = ' '.join(tag_from_row)
                        tag_list.append(row)
                    else:
                        tag_list.append(None)

            # 6. Create new columns and insert tag list into created columns
            j2['extracted_tags'] = tag_list
            defined_object_df = defined_object_df.append(j2, ignore_index=True)
        print("행 {}, 열 {}로 구성된 데이터 프레임입니다.".format(defined_object_df.shape[0], defined_object_df.shape[1]))

    except:
        print("정규화할 데이터가 없네요! 확인하세요.")
        print("경로: {}".format(path))

    finally:
        return defined_object_df

# 팔로워, 팔로잉 수가 없어서 랜덤으로 만들어주었다.
def get_user_follow_df(df, column_name_user_id):
    deduplicated_users = list(set(list(df[column_name_user_id])))  # duplicated_user
    user_follow_df = pd.DataFrame()
    user_follow_df['user_id'] = deduplicated_users
    user_follow_df['followers'] = np.random.randint(100, size=len(deduplicated_users))  # followers_list
    user_follow_df['following'] = np.random.randint(100, size=len(deduplicated_users))  # followings_list

    return user_follow_df


# 임의로 생성된 팔로워와 팔로잉 수를 이용해 사용자 영향도를 생성하였고, -1.1은 아예 추천에 제외될 것이다.
def get_user_influence_df(df, column_name_followers_list, column_name_followings_list):
    # 사용자별 영향력 정규화
    def normalize_influence(df):
        numerator = (df - df.mean())
        denominator = (df.max() - df.min())
        df_norm = -1.1 if denominator == 0 else numerator / denominator
        return df_norm

    influence_list = []
    for followers, followings in zip(df[column_name_followers_list], df[column_name_followings_list]):
        influence_list.append(followers - followings)
    
    user_influence_df = pd.DataFrame()
    user_influence_df['user_id'] = df['user_id']
    user_influence_df['influence'] = influence_list
    user_influence_df['norm_influence'] = normalize_influence(user_influence_df['influence'])
    del df # delete useless df
    return user_influence_df


"""
예제. 파일 정제하기.
test_path = "D:\\vora_recommendation\\RecommendationEngine\\DataProcessing\\Data\\Original_data\\dataset2\\핫.json"
result = DataProcessing.define_object(test_path)
result_follow_df = DataProcessing.get_user_follow_df(result, 'user_id')
result_influence_df = DataProcessing.get_user_influence_df(result_follow_df, 'followers', 'following')

"""