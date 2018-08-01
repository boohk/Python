import math

import numpy as np
import pandas as pd


class UserItemMatrix:

    def __init__(self, dict_format):
        self.dict_format = dict_format

    # 행 인덱스를 구한다.
    def get_row_index(self):
        row_index_list = self.dict_format.keys()
        return row_index_list

    # 열 인덱스를 구한다.
    def get_column_index(self):
        row_index_list = self.dict_format.keys()
        column_index_list = []
        for index in row_index_list:
            column_index_list += self.dict_format.get(index)
        duplicated_column_index_list = list(set(column_index_list))
        return duplicated_column_index_list

    # 사용자-아이템 데이터 프레임 만들기 -> 0, 1로 표현
    def get_user_item_matrix_df(self):
        row_index_list = self.get_row_index()
        column_index_list = self.get_column_index()
        user_item_matrix = []
        for row_index in row_index_list:
            tmp_list = []
            for column_index in column_index_list:
                # 열 인덱스 값과 같으면 1 아니면 0
                tmp_list.append(1) if self.dict_format[row_index].count(column_index) else tmp_list.append(0)
            user_item_matrix.append(tmp_list)
        user_item_matrix_df = pd.DataFrame(user_item_matrix, columns=column_index_list, index=row_index_list)
        return user_item_matrix_df

    def get_user_item_matrix(self):
        user_item_matrix = self.get_user_item_matrix_df().values
        return user_item_matrix


class CosineSimilarity:

    def __init__(self, user_item_matrix_df):
        self.user_item_matrix_df = user_item_matrix_df

    # 모든 데이터에 대한 사용자별 코사인 유사도 계산 결과로 구성된 행렬을 반환한다.
    @property
    def get_cosine_similarity_matrix(self):
        # 두 벡터의 코사인 유사도를 계산하는 함수

        def get_cosine_similarity(first_row, second_row):
            vec1 = np.array(first_row)
            vec2 = np.array(second_row)
            numerator = np.dot(vec1.T, vec2)  # 두 벡터의 내적 값은 분자로
            sum_squared_vec_element1 = sum([v1 ** 2 for v1 in vec1])
            sum_squared_vec_element2 = sum([v2 ** 2 for v2 in vec2])
            denominator = math.sqrt(sum_squared_vec_element1) * math.sqrt(
                sum_squared_vec_element2)  # 각 벡터의 제곱값의 합의 루트의 곱은 분모로
            cosine_similarity = numerator / denominator
            return cosine_similarity

        user_item_matrix_array = np.array(self.user_item_matrix_df)
        cosine_similarity_matrix = []
        for i in range(len(user_item_matrix_array)):
            row_cosine_similarity = []
            for j in range(len(user_item_matrix_array)):
                first_row = user_item_matrix_array[i]
                second_row = user_item_matrix_array[j]
                row_cosine_similarity.append(
                    get_cosine_similarity(first_row, second_row)) if i != j else row_cosine_similarity.append(1)
            cosine_similarity_matrix.append(row_cosine_similarity)
        return cosine_similarity_matrix


class JaccardSimilarityDf:

    def __init__(self, user_item_matrix_df):
        self.user_item_matrix_df = user_item_matrix_df

    def get_jaccard_similarity_matrix(self):
        # a.intersection(b)은 a와 b의 교집합을 구하는 파이썬 내장함수이다. 이를 사용하기 위해서는 리스트형을 집합형(set)으로 변환해야한다.
        def get_jaccard_similarity(first_row, second_row):
            interaction = 0
            union = 0
            for x, y in zip(first_row, second_row):
                if x + y == 2:
                    interaction += 1
                if x + y == 2 or x + y != 0:
                    union += 1
            numerator = interaction
            denominator = union
            jaccard_similarity = numerator / denominator
            return jaccard_similarity

        user_item_matrix_array = np.array(self.user_item_matrix_df)
        jaccard_similarity_matrix = []
        for i in range(len(user_item_matrix_array)):
            row_jaccard_similarity = []
            for j in range(len(user_item_matrix_array)):
                first_row = user_item_matrix_array[i]
                second_row = user_item_matrix_array[j]
                row_jaccard_similarity.append(
                    get_jaccard_similarity(first_row, second_row)) if i != j else row_jaccard_similarity.append(1)
            jaccard_similarity_matrix.append(row_jaccard_similarity)
        return jaccard_similarity_matrix


class JaccardSimilarityDict:

    def __init__(self, user_item_dict):
        self.user_item_dict = user_item_dict

    def get_jaccard_similarity_matrix(self):
        # a.intersection(b)은 a와 b의 교집합을 구하는 파이썬 내장함수이다. 이를 사용하기 위해서는 리스트형을 집합형(set)으로 변환해야 한다.
        def get_jaccard_similarity(first_row, second_row):
            s_first_row = set(first_row)
            s_second_row = set(second_row)
            numerator = s_first_row.intersection(s_second_row)
            denominator = s_first_row.union(s_second_row)
            jaccard_similarity = len(numerator) / len(denominator)
            return jaccard_similarity

        jaccard_similarity_matrix = []
        for i in self.user_item_dict:
            row_jaccard_similarity = []
            for j in self.user_item_dict:
                first_row = self.user_item_dict[i]
                second_row = self.user_item_dict[j]
                row_jaccard_similarity.append(get_jaccard_similarity(first_row, second_row))
            jaccard_similarity_matrix.append(row_jaccard_similarity)
        return jaccard_similarity_matrix

    def get_similarity_users_dict(self):
        jaccard_similarity_matrix = self.get_jaccard_similarity_matrix()
        # 인덱스를 기준으로 매트릭스를 딕셔너리로 재구성
        jaccard_similarity_dict = jaccard_similarity_matrix.to_dict('index')
        for k in jaccard_similarity_dict.keys():
            tmp_dict = dict()
            for item in jaccard_similarity_dict.get(k).items():
                if k == item[0]:
                    pass
                else:
                    tmp_dict[item[0]] = item[1]
            # 내림차순으로 정렬한 결과를 넣는다.
            tmp_dict = dict(sorted(tmp_dict.items(), key=lambda t: t[1], reverse=True))
            jaccard_similarity_dict[k] = tmp_dict
        return jaccard_similarity_dict


# print(setFormat(0.70710678118654757))


# 혹시 모르니...
def change_df_to_dict(df, col_name_user_id, col_name_contents):
    df_to_dict = df.set_index(col_name_user_id)[col_name_contents].str.split(' ').to_dict()
    return df_to_dict


# 소수 4번째 자리에서 반올림하는 함수
def setFormat(value):
    value = round(value, 3)
    return value

load_path = 'C:\\Users\\User\Documents\MEGA\Python Project\ExperimentationVoraRecommendationSystem\DataHandling\data\definedData\combineResults2.json'
df = pd.read_json(load_path, encoding='utf-8')
new = change_df_to_dict(df, 'user_id', 'extracted_tags')
n_uim = UserItemMatrix(new)
UserItem_matrix = n_uim.get_user_item_matrix()

if __name__ == '__main__':
    print(UserItem_matrix)
