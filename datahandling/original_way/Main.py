# -*- coding: utf-8 -*-
"""
원래대로라면 raw 데이터를 정제하고 정제된 데이터를 json 형식(백업용)으로 저장하고,
다시 pandas로 읽은 후 한 번에 Mysql에 저장했을 것이다. 그럴 때 사용하는 파이썬 코드이다.

"""


import pandas as pd
import pymysql

load_path = 'D:\\vora_recommendation\RecommendationEngine\DataProcessing\Data\Defined_data\experiment_remove_None_data_1533627625.json'
df = pd.read_json(load_path, orient='index')
df = df.reset_index(drop=True)

# 1. DB 커넥션 설정
# MySQL Connection 연결
conn = pymysql.connect(host='localhost', user='root', password='1234', db='db_instagram', charset='utf8mb4')

# Connection의 Cursor 생성
curs = conn.cursor()

# 2. MySQL에 raw_data 삽입하기
sql_insert = "INSERT INTO instagram(user_id, timestamp, post_id, extracted_tags, contents_url, like_count, comment_count) VALUES (%s, %s, %s, %s, %s, %s, %s)"

try:
    cnt = 0
    for row in df.iterrows():
        user_id = row[1]['user_id']
        timestamp = row[1]['timeStamp']
        post_id = row[1]['post_id']
        extracted_tags = row[1]['extracted_tags']
        contents_url = row[1]['contents_url']
        like_count = row[1]['like_count']
        comment_count = row[1]['comment_count']
        # Assign values from each row
        values = (user_id, str(timestamp), post_id, extracted_tags, contents_url, like_count, comment_count)
        # Execute sql Query
        curs.execute(sql_insert, values)
        
    # 1000개마다 커밋해준다. 하나 하나 커밋하면 속도가 너무 느려지기 때문이다. 
    cnt = cnt + 1
    if cnt == 1000:
        conn.commit()
    cnt = 0
    if cnt != 1000:
        print(cnt)
    conn.commit()
    
except Exception as e:
    print(e)

finally:
    curs.close()