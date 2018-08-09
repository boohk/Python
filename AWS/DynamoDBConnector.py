# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 18:17:04 2018

@author: User
"""

import boto3
import pprint
import pandas as pd
import time

# with open('./config/config.json', 'r') as file:
#     config = json.loads(file.read())

dynamodb = boto3.resource(
    'dynamodb',
    region_name='ap-northeast-2',
    # aws_access_key_id=config['ID'],
    # aws_secret_access_key=config['KEY']
)


# 1. Table 제거
if __name__ == '__main__':
    table = dynamodb.Table('relatedTags')
    response = table.delete()
    printer = pprint.PrettyPrinter(indent=2)
    printer.pprint(response)


# 2. DynamoDB 내 Table 생성하기
# 키 정리할 때, 기준 키만 설정하면 된다. 핵 좋아!
if __name__ == '__main__':
    table = dynamodb.create_table(
        TableName='relatedTags',
        KeySchema=[
            {
                'AttributeName': 'idx',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'idx',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 50,
            'WriteCapacityUnits': 50
        }
    )

# 3. DynamoDB 내 생성된 특정 Table 정보 확인 및 아이템 가져오기
if __name__ == '__main__':
    table = dynamodb.Table('relatedTags')
    print(1, table.creation_date_time)

    response = table.get_item(
        Key={
            'idx': 1
        }
    )
    item = response['Item']
    print(2, item)

# 4. 아이템 업데이트 하기
if __name__ == '__main__':
    table = dynamodb.Table('relatedTags')
    table.update_item(
        Key={
            'idx': 2
        },
        UpdateExpression='SET createdTime = :val1',
        ExpressionAttributeValues={
            ':val1': "2018-08-08T05:07:13.515Z"
        }
    )

# 5. 아이템 삭제하기
if __name__ == '__main__':
    table = dynamodb.Table('relatedTags')
    table.delete_item(
        Key={
            'idx': 1
        }
    )

# 6. 항목 생성하기
if __name__ == '__main__':
    table = dynamodb.Table('relatedTags')
    table.put_item(
        Item={
            'idx': 1,
            'cretedTime': "2018-08-09T05:07:13.515Z",
            'relatedTag': {
                "1": [
                    177,
                    60,
                    1231,
                    1298423,
                    8831092,
                    20931
                ],
                "2": [
                    54,
                    782,
                    229,
                    7821,
                    49632,
                    85214
                ],
                "3": [
                    285,
                    2,
                    987,
                    128,
                    6356,
                    6684
                ]
            },
        }
    )
        
# 7. Json 파일을 이용해 항목 데이터로 생성하기
if __name__ == '__main__':
    def load_json_to_dict(load_path):
        import json
        with open(load_path, 'r', encoding="utf-8") as data_file:
            data = data_file.read()
        data_file.close()
        d = json.loads(data)
        return d
    
    table = dynamodb.Table('relatedTags')
    load_path = "D:\\vora_recommendation\\data_add_time_dynamo1.json"
    data = load_json_to_dict(load_path)
    table = dynamodb.Table('relatedTags')
    
    dataIdx = data['idx']
    dataCreatedTime = data['createdTime']
    dataRelatedTags = data['relatedTags']
    
    response = table.put_item(
        Item={
            'idx': dataIdx,
            'createdTime': dataCreatedTime,
            'relatedTags': dataRelatedTags
        })
    printer = pprint.PrettyPrinter(indent=2)
    printer.pprint(response)
    time.sleep(.500)
