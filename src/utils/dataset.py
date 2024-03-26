import pandas as pd

def load_english(dataset='oxford_3000'):
    df = pd.read_pickle(f"./data/english/{dataset}.pkl")
    df.head()
    data = df[["word", "type", "cefr", "phon_br", "phon_n_am", "definition", "example"]]
    data['cefr'] = data['cefr'].map(lambda x: x.strip().upper())
    data = data.rename(columns={'phon_br' : 'phonetics (UK)'})
    data = data.rename(columns={'phon_n_am' : 'phonetics (US)'})
    return data

# "word": word, "type": type, "english": english, "frequency_rank": frequency_rank
def load_spanish():
    df = pd.read_pickle(f"./data/spanish/spanish.pkl")
    data = df[["word", "type", "english", "frequency_rank"]]
    return data

# "word": word, "type": type, "english": english, "frequency_rank": frequency_rank, "example_spanish": example_spanish, "example_english": example_english
def load_spanish2():
    df2 = pd.read_pickle(f"./data/spanish/spanish2.pkl")
    data = df2[["word", "type", "english", "example_spanish", "example_english", "frequency_rank"]]
    return data