# -*- coding: utf-8 -*-
import pandas as pd

from pathList import PathList
from dataProcessing import define_object, get_user_follow_df, get_user_influence_df
from sqlalchemy import create_engine

# pandas의 to_sql을 사용하기 위해서는 engine을 create해야 한다. -> 단순 db 연동이라고 생각하면 됨.
db_uri = "mysql+pymysql://root:1234@127.0.0.1:3306/db_instagram"
engine = create_engine(db_uri)

dirpathlist = PathList('C:\\Users\\LG\\Desktop\\todayQuest\\all_flow\\data', 'dir').get_path_list()
for dirpath in dirpathlist:
    
    all_df = pd.DataFrame(columns=['contents_url', 'like_count', 'post', 'comment_count', 'post_id',
                                   'user_id', 'timeStamp', 'extracted_tags'])
    all_follow_df = pd.DataFrame(columns=['user_id', 'followers', 'following'])
    all_influence_df = pd.DataFrame(columns=['user_id', 'influence', 'norm_influence'])
    
    # 폴더내 존재하는 json파일 경로를 가져온다.
    filepathlist = PathList(dirpath).get_path_list('.json')
    # 이 후 폴더내 존자하는 json 파일을 저장한 후 한 데이터 프레임으로 저장한다.
    for filepath in filepathlist:
        result = define_object(filepath)
        result_follow_df = get_user_follow_df(result, 'user_id')
        result_influence_df = get_user_influence_df(result_follow_df, 'followers', 'following')
        all_df = all_df.append(result)
        all_follow_df =all_follow_df.append(result_follow_df)
        all_influence_df = all_influence_df.append(result_influence_df)
    
    # all_df = all_df.drop("post", axis=1) # post를 지울수도 있음.
    all_df.post = all_df.post.astype(str) # post는 리스트 형태인데 오류가 나서 string형으로 변경해주었다.
    
    # 폴더별 모든 json 파일에 대한 데이터프레임 DB에 저장.
    all_df.to_sql(con=engine, name='posts', if_exists='append', index=False, chunksize=10000)
    all_follow_df.to_sql(con=engine, name='follow_infomation', if_exists='append', index=False, chunksize=10000)
    all_influence_df.to_sql(con=engine, name='norm_influence', if_exists='append', index=False, chunksize=10000)