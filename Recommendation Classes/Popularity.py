# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 14:12:03 2018
활동량이 가장 많은 인기 사용자 추천을 위해 추천할 사용자의 팔로워 수와 게시물 증가량를 계산한다.
@author: Boo, Hyunkyung
"""
import pandas as pd


class ContentsReactivity:
    """
    게시물 반응도는 좋아요 수(N)와 댓글 수(M)에 따른 반응도(P)로 라플라스 교정법 기반의 엔트로피 공식과 속성에 대한 상대적 가중치를 결합해 고안한 반응도 공식이다.
    이 때, 상대적 가중치로 게시물을 구성하는 좋아요, 댓글로 구분하여 각각의 중요도를 반영한다. 좋아요에 대한 가중치는 0.8, 댓글에 대한 가중치는 0.2로 설정한다
    """

    def __init__(self, content_id, like_count, comment_count):
        """

        Args:
            content_id: 게시물 id
            like_count: 게시물에 표현된 좋아요 수
            comment_count: 게시물에 달린 코멘트 수
        """
        self.content_id = content_id
        self.like_count = like_count
        self.comment_count = comment_count

    @property
    def calculate_contents_reactivity(self):
        """
        Returns: contents_reactivity (게시물 반응도)

        """
        molecular = ((self.like_count + 1) * 0.8 + (self.comment_count + 1) * 0.2)
        denominator = (self.like_count + self.comment_count + 2)
        contents_reactivity = molecular / denominator
        return contents_reactivity


class UserPopularity:
    """
    게시물 증가량과 정규화된 팔로워수에 각 0.5를 곱하여 사용자 인기도를 계산한다.
    """

    def __init__(self, user_id):
        """

        Args:
            user_id: 사용자 id
        """
        self.user_id = user_id

    @staticmethod
    def calculate_contents_gain(data):
        """
        게시물 증가량(Contents Gain, CG)의 수식은 다음과 같으며 게시물별 반응도를 모든 게시물에 적용해 표현한 값으로
        모든 게시물에 대한 타 사용자가 표현한 '게시물 반응도'를 계산한다.

        Args:
            data: 사용자 게시물 반응도의 평균

        Returns: 사용자 게시물 증가량

        """
        try:
            if type(data) == list:
                user_contents_gain_mean = 0 if len(data) == 0 else sum(data) / len(data)
            else:
                user_contents_gain_mean = data['contents_reactivity'].mean()

            return user_contents_gain_mean

        except TypeError:
            print("This data is wrong type, Check data type again")

    @staticmethod
    def normalize_follower_counting(user_follower_count, max_follower_count, min_follower_count):
        """

        Args:
            user_follower_count: 사용자의 팔로워 수
            max_follower_count: 전체 사용자 팔로워수의 최댓값
            min_follower_count: 전체 사용자 팔로워수의 최솟값

        Returns: 사용자의 정규화된 팔로워 수

        """
        normalized_follower_counting = (user_follower_count - max_follower_count) / (
                max_follower_count - min_follower_count)
        return normalized_follower_counting

    @staticmethod
    def calculate_user_popularity(user_contents_gain_mean, normalized_follower_counting):
        """

        Args:
            user_contents_gain_mean: 사용자의 게시물 증가량
            normalized_follower_counting: 사용자의 정규화된 팔로워 수

        Returns: 사용자 인기도

        """
        user_popularity = (user_contents_gain_mean * 0.5) + (normalized_follower_counting * 0.5)
        return user_popularity


# if __name__ == '__main__':
#     post111 = ContentsReactivity(111, 11, 10).calculate_contents_reactivity()
#     post112 = ContentsReactivity(112, 12, 10).calculate_contents_reactivity()
#     post113 = ContentsReactivity(113, 13, 10).calculate_contents_reactivity()
#     post114 = ContentsReactivity(114, 14, 10).calculate_contents_reactivity()
#     all_posts = [post111, post112, post113, post114]
#
#     user = UserPopularity(1)
#     user_cg = user.calculate_contents_gain(all_posts)
#     user_nfc = user.normalize_follower_counting(10, 50, 0)
#     user_p = user.calculate_user_popularity(user_cg, user_nfc)
#
#     # 사용자 인기도
#     print(user_p)


def create_contents_reactivity_df(df, col_name_content_id, col_name_like_count, col_name_comment_count):
    """

    Args:
        df:
        col_name_content_id:
        col_name_like_count:
        col_name_comment_count:
    """
    contents_reactivity_list = []
    for content_id, like_count, comment_count in zip(df[col_name_content_id], df[col_name_like_count],
                                                     df[col_name_comment_count]):
        content_reactivity = ContentsReactivity(content_id, like_count, comment_count).calculate_contents_reactivity
        contents_reactivity_list.append(content_reactivity)
    df['contents_reactivity'] = contents_reactivity_list


def change_to_dict_format(key_list, value_list):
    """

    Args:
        key_list:
        value_list:

    Returns:

    """
    tmp_dict = dict()
    for key, value in zip(key_list, value_list):
        tmp_dict[key] = value
    return tmp_dict


def create_contents_gain_dict(df, col_name_user_id, col_name_contents_reactivity):
    """

    Args:
        df:
        col_name_user_id:
        col_name_contents_reactivity:

    Returns:

    """
    user_id_list = []
    user_contents_gain_list = []
    unique_user_id_list = list(df[col_name_user_id].drop_duplicates())
    for user_id in unique_user_id_list:
        user_contents_reactivity = df.groupby(user_id)[col_name_contents_reactivity]
        user_contents_gain = UserPopularity(user_id).calculate_contents_gain(user_contents_reactivity)
        # 한줄로도 표현 가능하다.
        # user_contents_gain = df.groupby(user_id)[col_name_contents_reactivity].mean()
        user_id_list.append(user_id)
        user_contents_gain_list.append(user_contents_gain)

    contents_gain_dict = change_to_dict_format(user_id_list, user_contents_gain_list)
    # contents_gain_dict = dict()
    # contents_gain_dict['user_id'] = user_id_list
    # contents_gain_dict['contents_gain'] = contents_gain_list
    return contents_gain_dict


def create_normalized_follower_counting_dict(df, col_name_user_id, col_name_follower_counting):
    """

    Args:
        df:
        col_name_user_id:
        col_name_follower_counting:

    Returns:

    """
    # unique_user_id_list = list(df[col_name_user_id].drop_duplicates())
    tmp_df = df.sort_values('col_name_follower_counting', ascending=False).drop_duplicates(
        col_name_user_id).sort_index()
    normalized_follower_counting_list = []
    for user_id, user_follower_counting in zip(tmp_df['col_name_user_id'], tmp_df['col_name_follower_counting']):
        user_normalize_follower_counting = UserPopularity(user_id).normalize_follower_counting(user_follower_counting,
                                                                                               tmp_df[
                                                                                                   col_name_follower_counting].max(),
                                                                                               tmp_df[
                                                                                                   col_name_follower_counting].min())
        normalized_follower_counting_list.append(user_normalize_follower_counting)

    normalized_follower_counting_dict = change_to_dict_format(list(tmp_df['col_name_user_id']),
                                                              normalized_follower_counting_list)
    return normalized_follower_counting_dict


def create_user_popularity_to_dict(df, col_name_user_id, normalized_follower_counting_dict, contents_gain_dict):
    """

    Args:
        df:
        col_name_user_id:
        normalized_follower_counting_dict:
        contents_gain_dict:

    Returns:

    """
    unique_user_id_list = list(df[col_name_user_id].drop_duplicates())
    user_popularity_list = []
    for user_id in unique_user_id_list:
        normalized_follower_counting = normalized_follower_counting_dict.get(user_id)
        user_contents_gain_mean = contents_gain_dict.get(user_id)
        user_popularity = UserPopularity(user_id).calculate_user_popularity(user_contents_gain_mean,
                                                                            normalized_follower_counting)
        user_popularity_list.append(user_popularity)

    user_popularity_dict = change_to_dict_format(unique_user_id_list, user_popularity_list)
    return user_popularity_dict


def merge_dicts(normalized_follower_counting_dict, contents_gain_dict, user_popularity_dict):
    user_info = {**normalized_follower_counting_dict, **contents_gain_dict, **user_popularity_dict}
    print("user_info 의 키 값은 {}이다.".format(user_info.keys()))
    return user_info


def save_back_up_file(dict_data, save_path):
    columns_list = dict_data.keys()
    user_info_df = pd.DataFrame.from_dict(dict_data, columns=columns_list)

    # 결과는 JSON 형태로 저장
    user_info_df.to_json(path_or_buf=save_path, orient='columns')
