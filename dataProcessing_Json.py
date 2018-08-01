import json
import pandas as pd
from pandas.io.json import json_normalize  # package for flattening json in pandas df
import os
import re


# 디렉토리 내에 특정 파일의 목록을 가지고 오는 클래스
class FilePathList:
    def __init__(self, path, sign):
        self.path = path
        self.sign = sign

    # Call a list of files from directory path
    def get_path(self):
        file_path_list = []
        for (file_path, dir, files) in os.walk(self.path):
            for filename in files:
                full_filename = os.path.join(file_path, filename)
                ext = os.path.splitext(filename)[-1]
                if ext == self.sign:
                    file_path_list.append(full_filename)
        return file_path_list


# Json 파일을 df 형태로 전처리하는 클래스
class DataProcessing(object):
    def __init__(self, path):
        self.path = path

    def define_obejct(self):
        # Getting values using key on dictionary format
        def extract_items(dict_data, keys):
            new_dict = {}
            for i in dict_data.keys():
                if i in keys:
                    new_dict[i] = dict_data[i]
            return new_dict

        defined_obejct_df = pd.DataFrame()
        try:
            with open(self.path, encoding='UTF8') as f:
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
                        tag_list.append("null+nan+none")
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
                defined_obejct_df = defined_obejct_df.append(j2, ignore_index=True)
            print("행 {}, 열 {}로 구성된 데이터 프레임입니다.".format(defined_obejct_df.shape[0], defined_obejct_df.shape[1]))

        except:
            print("정규화할 데이터가 없네요! 확인하세요.")
            print("경로: {}".format(self.path))

        finally:
            return defined_obejct_df


# 데이터를 저장하는 함수
def save_data(save_path, dataFrame, format):
    formats = ['csv', 'xlsx', 'json']
    if format in formats:
        if format == formats[0]:
            dataFrame.to_csv(path_or_buf=save_path, sep='|', header=True, index=False, encoding='utf-8')
        elif format == formats[1]:
            writer = pd.ExcelWriter(save_path)
            dataFrame.to_excel(writer, 'sheet1', header=True, index=False, encoding='utf-8')
            writer.save()
        else:
            dataFrame.to_json(path_or_buf=save_path, orient='index')
    else:
        print("'csv', 'xlsx', 'json' 형태 중 하나만 선택하세요.")



def main():
    path = "C:\\Users\\User\Documents\MEGA\Python Project\\test_Recommnedation_system\\test_recommendation_system\Data\Original_data\dataset2"
    json_path_list = FilePathList(path, '.json').get_path()

    try:
        All_df = pd.DataFrame()
        wrong_data_path = []
        cnt = 0

        for path in json_path_list:
            cnt += 1
            print(cnt, path)
            each_df = DataProcessing(path).define_obejct()
            if each_df.empty:
                wrong_data_path.append(path)
            else:
                All_df = pd.concat([All_df, each_df], axis=0, ignore_index=True)
        print(All_df.shape)

    finally:
        print("데이터가 정제되지 않은 것도 있네요! 확인해보세요.")
        print("목록:", wrong_data_path)

    # 데이터 저장하기
    # save_root = 'C:\\Users\\User\Documents\MEGA\Python Project\\test_Recommnedation_system\\test_recommendation_system\Data\Defined_data\\correct_data_20180726'
    # save_format =  ['csv', 'xlsx', 'json']
    # for f in save_format:
    #     save_path = save_root+'.'+f
    #     save_data(save_path, All_df, f)

    # 데이터 정제가 되지 않은 데이터도 저장한다. (확인용)
    save_path = 'C:\\Users\\User\Documents\MEGA\Python Project\\test_Recommnedation_system\\test_recommendation_system\Data\Defined_data\\wrong_data_20180727.json'
    wrong_data_path_df = pd.DataFrame(wrong_data_path, columns=['wrong_path'])
    save_data(save_path, wrong_data_path_df, 'json')
    # test = pd.read_json('C:\\Users\\User\Documents\MEGA\Python Project\\test_Recommnedation_system\\test_recommendation_system\data\data1.json', encoding='utf-8')



#테스트
# if __name__ == '__main__':
    # main()





















