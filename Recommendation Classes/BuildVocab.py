# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 17:10:53 2018

@author: User
"""
import time


# 게시글 작성 시간을 기준으로 필터링 한다.
def fitter_df(self, col_date_writen):
    now = time.time()
    month = 2624671916.0105
    condition = now - month
    filtered_df = self.df[col_date_writen] > condition
    return filtered_df


class TaggedDocuments:

    def __init__(self, df, col_name_idx, col_name_extracted_tags):
        self.df = df
        self.col_name_idx = col_name_idx
        self.col_name_extracted_tags = col_name_extracted_tags

    def define_data_set(self):
        tmp = self.df.groupby(self.col_name_idx)[self.col_name_extracted_tags].agg(lambda col: ' '.join(col))
        defined_data_set = dict()
        for item in tmp.items():
            value = item[1] if item[1] != 'null+nan+none' else ''
            defined_data_set[item[0]] = value
        return defined_data_set

    def get_custom_tagged_document(self):
        defined_data_set = self.define_data_set()
        from gensim.models.doc2vec import TaggedDocument
        custom_tagged_document = []
        for user in defined_data_set.keys():
            splited_tags = defined_data_set[user].split(" ")
            custom_tagged_document.append(TaggedDocument(splited_tags, [str(user)]))
        return custom_tagged_document

    @staticmethod
    def count_words(custom_tagged_document):
        import collections
        tagged_documents = []
        for tagged_document in custom_tagged_document:
            tagged_documents += tagged_document[0]
        tagged_documents_count = collections.Counter(tagged_documents)
        return tagged_documents_count

    @staticmethod
    def track_words(custom_tagged_document, word):
        tracked_documents = dict()
        extracted_document = dict()
        for tracked_document in custom_tagged_document:
            if word in tracked_document[0]:
                extracted_document[tracked_document[1]] = tracked_document[0]
        tracked_documents[word] = extracted_document
        return tracked_documents

    @staticmethod
    def save_custom_tagged_document(custom_tagged_document, save_path):
        import json
        with open(save_path, 'w', encoding="utf-8") as data_file:
            json.dump(custom_tagged_document, data_file, ensure_ascii=False, indent="\t")
            data_file.close()
    # sorted(taggedDocuments_count.items(), key=lambda value: value[1])


class SentencesReader(object):
    def __init__(self, df, col_name_extracted_tags):
        self.df = df
        self.col_name_extracted_tags = col_name_extracted_tags

    # 문장 리스트로 읽기
    def read_rows(self):
        custom_sentences = []
        for row in self.df[self.col_name_extracted_tags].iteritems():
            if not row[1] is None:
                custom_sentences.append([w for w in row[1].split(', ')])
        return custom_sentences

    @staticmethod
    def count_words(custom_sentences):
        import collections
        sentences = []
        for sentence in custom_sentences:
            sentences += sentence[0]
        sentences_count = collections.Counter(sentences)
        return sentences_count

    # sorted(taggedDocuments_count.items(), key=lambda value: value[1])
    @staticmethod
    def track_words(custom_sentences, word):
        tracked_sentences, extracted_sentences = dict(), dict()
        for tracked_sentence in custom_sentences:
            if word in tracked_sentence[0]:
                extracted_sentences[tracked_sentence[1]] = tracked_sentence[0]
        tracked_sentences[word] = extracted_sentences
        return tracked_sentences
