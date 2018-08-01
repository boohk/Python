from gensim.models import Word2Vec


class RelatedTag:
    def __init__(self, model_path=None, model=None):
        self.model_path = model_path
        self.model = model

    # def infer_related_tag(self, model, tag):
    #
    #
    #
    #     tag_and_sim_dict = dict(model.most_similar(tag, topn=20))
    #     sorted_tag_and_sim = sorted(tag_and_sim_dict.items(), reverse=False)
    #     sorted_tag_and_sim_dict = dict(sorted_tag_and_sim)
    #     return sorted_tag_and_sim_dict

    @staticmethod
    def extract_related_tag(model, tag):
        tag_and_sim_dict = dict(model.most_similar(tag, topn=20))
        sorted_tag_and_sim = sorted(tag_and_sim_dict.items(), reverse=False)
        sorted_tag_and_sim_dict = dict(sorted_tag_and_sim)
        return sorted_tag_and_sim_dict
