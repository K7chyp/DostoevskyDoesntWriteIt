from re import sub
from pymystem3 import Mystem
from tqdm import tqdm
from joblib import Parallel
from joblib import delayed
from tqdm import tqdm
import warnings

warnings.simplefilter("ignore")


RUSSIAN_STOPWORDS = {
    word.replace("\n", ""): True for word in open("RusStopWords.txt", "r")
}
BATCH_SIZE = 1000


class Preprocessing:
    def __init__(self, df):
        self.df = df.copy()
        self.string_preprocessing()
        self.text_lemmatizing()

    def string_preprocessing(self):
        m = Mystem()
        self.df.text = self.df.text.apply(
            lambda string: sub(r"\b\d+\b", "", sub(r"[^\w\s]", " ", str(string)))
        )
        self.df.text = self.df.text.apply(
            lambda string: "".join(word.lower() for word in string).split()
        )
        self.df.text = self.df.text.apply(
            lambda string: " ".join(
                word for word in string if word not in RUSSIAN_STOPWORDS
            ).split()
        )

    def lemmatize(self, text):
        m = Mystem()
        merged_text = "|".join(text)

        doc = []
        res = []

        for t in m.lemmatize(merged_text):
            if t != "|":
                doc.append(t)
            else:
                res.append(doc)
                doc = []

        return res

    def text_lemmatizing(self):
        self.df.text = self.df.text.apply(
            lambda texts: [
                texts[i : i + BATCH_SIZE] for i in range(0, len(texts), BATCH_SIZE)
            ]
        )
        self.df.text = self.df.text.apply(
            lambda text_batch: Parallel(n_jobs=-1)(
                delayed(self.lemmatize)(part_of_batch)
                for part_of_batch in tqdm(text_batch)
            )
        )
        self.df.text = self.df.text.apply(
            lambda text: [
                item[0] for sublist in [item for item in text] for item in sublist
            ]
        )
