import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.manifold import TSNE


class WordsClustering:

    # 폰트 설정
    mpl.rcParams['axes.unicode_minus'] = False
    font_name = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
    mpl.rc('font', family=font_name)

    def __init__(self, model):
        self.model = model

    def get_plot(self, topn):
        vocab = list(self.model.wv.vocab)
        X = self.model[vocab]
        tsne = TSNE(n_components=2)
        # X_tsne = tsne.fit_transform(X[:50, :])
        X_tsne = tsne.fit_transform(X[:topn, :])
        # df = pd.DataFrame(X_tsne, index=vocab[:50], columns=['x', 'y'])
        df = pd.DataFrame(X_tsne, index=vocab[:topn], columns=['x', 'y'])
        fig = plt.figure()
        fig.set_size_inches(200, 150)
        ax = fig.add_subplot(1, 1, 1)
        ax.scatter(df['x'], df['y'])

        for word, pos in df.iterrows():
            ax.annotate(word, pos, fontsize=30)
        return plt.show()
