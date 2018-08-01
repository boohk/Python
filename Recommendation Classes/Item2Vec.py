# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 17:10:53 2018

@author: User
"""
import logging
import time

from gensim.models import Word2Vec
from gensim.models.doc2vec import Doc2Vec


class User2Vec:

    def __init__(self, tagged_documents, config):
        self.tagged_documents = tagged_documents
        self.config = config

    def train(self):

        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        model = Doc2Vec(**self.config)
        model.build_vocab(self.tagged_documents)

        # epoch 설정 후 학습
        start = time.time()
        for epoch in range(model.epochs):
            model.train(self.tagged_documents, total_examples=len(self.tagged_documents), epochs=model.epochs)
            model.alpha -= 0.002  # decrease the learning rate
            model.min_alpha = model.alpha  # fix the learning rate, no decay

        end = time.time()
        print("During Time: {}".format(end - start))
        return model

    # updated_tagged_documents #솔찍히 필요 없을듯 -_-
    def update(self, model):
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        model.build_vocab(self.tagged_documents, update=True)
        # epoch 설정 후 학습
        start = time.time()
        for epoch in range(model.epochs):
            model.train()
            model.alpha -= 0.002  # decrease the learning rate
            model.min_alpha = model.alpha  # fix the learning rate, no decay

        end = time.time()
        print("During Time: {}".format(end - start))
        return model

    @staticmethod
    def save(model, save_path):
        import time
        date_created = int(time.time())
        print(date_created)
        file_name = "{}.user2vec.model".format(date_created)
        save_path += file_name
        print(save_path)
        model.save(save_path)
        print(save_path + "에 저장 완료")

    # {사용자 번호: {유사 사용자 1 : 유사도, 유사 사용자 2 : 유사도, , etc}}
    # {'8156815234': {'3056895722': 0.6550565958023071, '8145042343': 0.5274348258972168}
    @staticmethod
    def get_most_similar_users(model, user_id):
        users_list = model.docvecs.most_similar(str(user_id), topn=20)
        users_dict = dict(users_list)
        similar_users_dict = {user_id: users_dict}
        return similar_users_dict


class Post2Vec:

    def __init__(self, tagged_documents, config):
        self.tagged_documents = tagged_documents
        self.config = config

    @property
    def train(self):
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        model = Doc2Vec(**self.config)
        model.build_vocab(self.tagged_documents)

        # epoch 설정 후 학습
        start = time.time()
        for epoch in range(model.epochs):
            model.train(self.tagged_documents, total_examples=len(self.tagged_documents), epochs=model.epochs)
            model.alpha -= 0.002  # decrease the learning rate
            model.min_alpha = model.alpha  # fix the learning rate, no decay

        end = time.time()
        print("During Time: {}".format(end - start))
        return model

    # updated_tagged_documents #솔찍히 필요 없을듯 -_-
    def update(self, model):
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        model.build_vocab(self.tagged_documents, update=True)
        # epoch 설정 후 학습
        start = time.time()
        for epoch in range(model.epochs):
            model.train()
            model.alpha -= 0.002  # decrease the learning rate
            model.min_alpha = model.alpha  # fix the learning rate, no decay

        end = time.time()
        print("During Time: {}".format(end - start))
        return model

    @staticmethod
    def save(model, save_path):
        import time
        date_created = int(time.time())
        print(date_created)
        file_name = "{}.post2Vec.model".format(date_created)
        save_path += file_name
        print(save_path)
        model.save(save_path)
        print(save_path + "에 저장 완료")

    # {게시물 번호: {유사 게시물 1 : 유사도, 유사 게시물 2 : 유사도, , etc}}
    # {'8156815234': {'3056895722': 0.6550565958023071, '8145042343': 0.5274348258972168}
    @staticmethod
    def get_most_similar_posts(model, post_id):
        posts_list = model.docvecs.most_similar(str(post_id), topn=20)
        posts_dict = dict(posts_list)
        similar_posts_dict = {post_id: posts_dict}
        return similar_posts_dict


class Tag2Vec:

    def __init__(self, sentences, config):
        self.sentences = sentences
        self.config = config

    def train(self):
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

        start = time.time()
        model = Word2Vec(**self.config)
        model.build_vocab(self.sentences)
        model.train(self.sentences, total_examples=len(self.sentences), epochs=model.iter)
        end = time.time()
        print("During Time: {}".format(end - start))
        return model

    # Word2Vec 학습모델 생성
    def update(self, model):
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        # model = Word2Vec.load(model_load_path)
        start = time.time()
        model.build_vocab(self.sentences, update=True)
        model.train()
        end = time.time()
        print("During Time: {}".format(end - start))
        return model

    @staticmethod
    def save(model, save_path):
        import time
        date_created = int(time.time())
        file_name = "{}.tag2Vec.model".format(date_created)
        save_path += file_name
        model.save(save_path)
        print(save_path + "에 저장 완료")

    @staticmethod
    def get_most_similar_words(model, tag):
        tags_list = model.wv.most_similar(tag, topn=20)
        tags_dict = dict(tags_list)
        similar_tags_dict = {tag: tags_dict}
        return similar_tags_dict

    @staticmethod
    def get_related_to_tags(model, p_tag1, p_tag2, n_tag1):
        tags_list = model.wv.most_similar(positive=[p_tag1, p_tag2], negative=[n_tag1], topn=20)
        tags_dict = dict(tags_list)
        similar_tags_dict = {'n_tag2': tags_dict}
        return similar_tags_dict
    # model.wv.vocab <- 중복 제거된 단어장을 얻을 수 있다. 반환시 list로 반환하면 편하다. 원래는 dict


# 저장 모델 불러오기. 공통적으로 사용된다.
def load_model(model_path):
    if model_path.find('user2vec') > 0 or model_path.find('post2Vec') > 0:
        model = Doc2Vec.load(model_path)
        return model
    elif model_path.find('tag2vec') > 0:
        model = Word2Vec.load(model_path)
        return model
    else:
        print("Check your path! The current path is {}".format(model_path))
