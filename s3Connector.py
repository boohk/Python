import boto3
import botocore
import dataProcessing

# 1. 버킷 생성/삭제
if __name__ == "__main__":
    # 버킷 사용 위한 기본 설정
    s3 = boto3.resource('s3')
    s3client = boto3.client('s3')

    s3.create_bucket(Bucket="my-insta-bucket-boo",
                     CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-2'})()  # 버킷 생성
    s3.Bucket("my-insta-bucket-boo").delete()  # 버킷 제거
    s3.create_bucket(Bucket="my-insta-bucket-boo",
                     CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-2'})()  # 버킷 생성

# 2. 버킷 정보 확인
if __name__ == '__main__':
    s3 = boto3.resource('s3')
    s3client = boto3.client('s3')

    for bucket in s3.buckets.all():
        # 계정내 생성된 버킷 정보 가져오기
        print('{name}\t{created}'.format(name=bucket.name, created=bucket.creation_date))

# 3. 특정 버킷에 객체 업로드
if __name__ == '__main__':
    s3 = boto3.resource('s3')
    s3client = boto3.client('s3')

    myBucket = s3.Bucket("my-insta-bucket-boo")  # 특정 버킷 연동
    print(myBucket.name)  # 버킷 이름

    path = 'C:\\Users\\User\Documents\MEGA\Python Project\\test_Recommnedation_system\\test_recommendation_system\Data\Original_data\dataset2'
    obj_path_list = dataProcessing.FilePathList(path, '.json').get_path()

    for file_path in obj_path_list:
        folder = 'Original_data/'  # 버킷 내 폴더 생성
        obj = file_path.split('\\')[-1]  # 저장할 객체 이름
        s3.Object(myBucket.name, folder + obj).upload_file(file_path)  # 파일 업로드

    for obj in bucket.objects.all():
        print(obj.key, obj.last_modified)

# 4. 버킷 내 저장된 객체 정보 확인
if __name__ == '__main__':
    s3 = boto3.resource('s3')
    s3client = boto3.client('s3')

    myBucket = s3.Bucket("my-insta-bucket-boo")  # 특정 버킷 연동

    # 버킷에 저장된 객체 이름과 마지막 수정일을 확인한다.
    for obj in myBucket.objects.all():
        print(obj.key, obj.last_modified)

    # 특정 객체의 모든 정보를 읽는다
    obj = s3.Object(myBucket.name, 'Original_data/삼겹살맛집.json').get()
    print(obj)

    # 객체 내용만 읽는다
    obj_body = s3.Object(myBucket.name, 'Original_data/삼겹살맛집.json').get()['Body'].read().decode('utf-8')
    print(obj_body)

# 4. 객체 다운로드
if __name__ == '__main__':
    s3 = boto3.resource('s3')
    s3client = boto3.client('s3')
    myBucket = s3.Bucket("my-insta-bucket-boo")  # 특정 버킷 연동

    try:
        s3.Bucket(myBucket).download_file('Original_data/삼겹살맛집.json', 'D:\삼겹살맛집.json')  # 객체 다운로드
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
