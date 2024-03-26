import pandas as pd

class EnglishData:
    def __init__(self, dataset: str):
        self.dataset = dataset

    def load_data(self):
        dataset = self.dataset
        df = pd.read_pickle(f"./data/english/{dataset}.pkl")
        df.head()
        data = df[["word", "type", "cefr", "phon_br", "phon_n_am", "definition", "example"]]
        data['cefr'] = data['cefr'].map(lambda x: x.strip().upper())
        data = data.rename(columns={'phon_br' : 'phonetics (UK)'})
        data = data.rename(columns={'phon_n_am' : 'phonetics (US)'})
        return data

class SpanishData:
    def __init__(self, dataset: str):
        self.dataset = dataset

    # "word": word, "type": type, "english": english, "frequency_rank": frequency_rank, "example_spanish": example_spanish, "example_english": example_english
    def load_data(self):
        dataset = self.dataset
        df2 = pd.read_pickle(f"./data/spanish/spanish2.pkl")
        data = df2[["word", "type", "english", "example_spanish", "example_english", "frequency_rank"]]
        if dataset == 'spanish_3000':
            data = data.iloc[:3000] # A1, A2, B1
        elif dataset == 'spanish_5000_exclusive':
            data = data.iloc[3000:] # B2, C1
        return data

    # By Ranking / pseudo-cefr. Shuffled
    def cefrs_data_by_dataset(self, data):
        DATASET = self.dataset
        if DATASET=='spanish_3000':
            cefrs = ['A1', 'A2', 'B1']
            data_by_cefr = [
                data.iloc[:1000],
                data.iloc[1000:2000],
                data.iloc[2000:],
                ]
        elif DATASET=='spanish_5000_exclusive':
            cefrs = ['B2', 'C1']
            data_by_cefr = [
                data.iloc[:1000],
                data.iloc[1000:],
                ]
        else:
            cefrs = ['A1', 'A2', 'B1', 'B2', 'C1']
            data_by_cefr = [
                data.iloc[:1000],
                data.iloc[1000:2000],
                data.iloc[2000:3000],
                data.iloc[3000:4000],
                data.iloc[4000:],
                ]
        return cefrs, data_by_cefr

    # Complete to HTML