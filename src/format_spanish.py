import argparse

from utils.dataset import SpanishData
from utils.utils import replace_word_in_field_with_underscore, FixLatexLine

parser = argparse.ArgumentParser()
parser.add_argument("dataset", default="spanish_3000", choices=["spanish_3000", "spanish_5000"])
parser.add_argument("--generate_pdf", action="store_true", default=False)
args = parser.parse_args()

DATASET = args.dataset
IS_GENERATE_PDF = args.generate_pdf

load_data = SpanishData(DATASET).load_data
cefrs_data_by_dataset = SpanishData(DATASET).cefrs_data_by_dataset

# HTML, Underscore, Shuffled and Alphabetical
def format_html_all_columns(is_shuffle=True, is_alphabetical=False, with_underscore=True):
    data = load_data()
    if with_underscore:
        data["example_spanish"] = data.apply(lambda row: replace_word_in_field_with_underscore(row.word, row.example_spanish) , axis=1)
    assert is_alphabetical != is_shuffle
    if is_alphabetical:
        data.sort_values('word') # alphabetical
    if is_shuffle:
        data = data.sample(frac=1) # shuffle

    data = data.drop(['frequency_rank'], axis=1)
    data = data.rename(columns={'example_english' : 'example (English)'})
    data = data.rename(columns={'example_spanish' : 'example (Spanish)'})

    style = data.style.format(
        escape="html",
        )
    style = style.hide(axis='index')

    return style.to_html()

filename = DATASET + '_underscore_alphabetical'
html = format_html_all_columns(is_shuffle=False, is_alphabetical=True, with_underscore=True)
with open(f'output/{filename}.html', 'w') as f:
    f.write('<meta charset="UTF-8">'+html)

filename = DATASET+'_underscore_shuffled'
html = format_html_all_columns(is_shuffle=True, is_alphabetical=False, with_underscore=True)
with open(f'output/{filename}.html', 'w') as f:
    f.write('<meta charset="UTF-8">'+html)

filename = DATASET+'_shuffled'
html = format_html_all_columns(is_shuffle=True, is_alphabetical=False, with_underscore=False)
with open(f'output/{filename}.html', 'w') as f:
    f.write('<meta charset="UTF-8">'+html)

filename = DATASET+'_alphabetical'
html = format_html_all_columns(is_shuffle=False, is_alphabetical=True, with_underscore=False)
with open(f'output/{filename}.html', 'w') as f:
    f.write('<meta charset="UTF-8">'+html)

filenames = [DATASET+'_alphabetical', DATASET+'_shuffled', DATASET+'_underscore_shuffled', DATASET + '_underscore_alphabetical']

# ## HTML+PDF all columns grouped by CEFR

# Complete to HTML
def format_html_columns_by_cefr(is_shuffle=True, is_alphabetical=False, with_underscore=True):
    data = load_data()
    if with_underscore:
        data["example_spanish"] = data.apply(lambda row: replace_word_in_field_with_underscore(row.word, row.example_spanish) , axis=1)
    data.head()

    cefrs, data_by_cefr = cefrs_data_by_dataset(data)

    data_by_cefr[1].head()

    html_out = ''
    for i, data_slice in enumerate(data_by_cefr):
        if data_slice.empty:
            continue
        #cefr = data_slice['cefr'].iloc[0]
        cefr = cefrs[i]
        html_out += f'<h2>{cefr}</h2>'
        data_slice = data_slice.drop(['frequency_rank'], axis=1)

        if is_alphabetical:
            data_slice = data_slice.sort_values('word')
        if is_shuffle:
            data_slice = data_slice.sample(frac=1) # shuffle

        data_slice = data_slice.rename(columns={'word' : f'word ({cefr})'})
        data_slice = data_slice.rename(columns={'example_english' : 'example (English)'})
        data_slice = data_slice.rename(columns={'example_spanish' : 'example (Spanish)'})

        style = data_slice.style.format(
            escape="html",
            )
        style = style.hide(axis='index')
        html_out += style.to_html()
    return html_out

filename = DATASET+'_underscore_by_cefr_shuffled'
html = format_html_columns_by_cefr(is_shuffle=True, is_alphabetical=False, with_underscore=True)
with open(f'output/{filename}.html', 'w', encoding='utf-8') as f:
    f.write('<meta charset="UTF-8">'+html)

filename = DATASET+'_underscore_by_cefr_alphabetical'
html = format_html_columns_by_cefr(is_shuffle=False, is_alphabetical=True, with_underscore=True)
with open(f'output/{filename}.html', 'w', encoding='utf-8') as f:
    f.write('<meta charset="UTF-8">'+html)


# 2 column 5000 not by rank
# shuffle and alphabetical
# Fix supertabular and add \textit to type
column_format = 'p{1.2in}p{2.3in}p{1.2in}p{2.3in}'
fix_latex_line = FixLatexLine(column_format).fix_latex_line

def format_latex_columns(is_alphabetical=False, is_shuffle=True):
    # columns = ["word", "type", "english", "frequency_rank"]
    data = load_data()
    data["example_spanish"] = data.apply(lambda row: replace_word_in_field_with_underscore(row.word, row.example_spanish) , axis=1)
    if is_shuffle:
        data = data.sample(frac=1) # shuffle
    if is_alphabetical:
        data = data.sort_values('word') # alphabetical
    data["word"] = data.apply(lambda row: f"{row.word.strip()} ({row.type.strip()})" , axis=1)
    #data = data[["word", "spanish", "english", "example_spanish", "example_english"]]
    data = data[["word", "english"]]

    style = data.style.format(
        escape="latex",
        )
    style = style.hide(axis='index')
    style = style.hide(axis='columns')

    latex = style.to_latex(
        environment='supertabular',
        column_format=column_format
    )

    latex_lines = latex.splitlines()

    latex = '\n'.join((map(fix_latex_line, latex_lines)))
    return latex

latex = format_latex_columns(is_alphabetical=True, is_shuffle=False)
with open(f'build/{DATASET}_two_column_alphabetical.tex', 'w') as f:
    f.write(latex)

latex = format_latex_columns(is_alphabetical=True, is_shuffle=False)
with open(f'build/{DATASET}_two_column_shuffle.tex', 'w') as f:
    f.write(latex)

# two column, cefr by rank
# Fix supertabular and add \textit to type
column_format = 'p{1.2in}p{2.3in}p{1.2in}p{2.3in}'
fix_latex_line = FixLatexLine(column_format).fix_latex_line

def format_latex_columns_by_cefr(is_alphabetical=True, is_shuffle=False):
    data = load_data()

    cefrs, data_by_cefr = cefrs_data_by_dataset(data)

    for i, data_slice in enumerate(data_by_cefr):
        if data_slice.empty:
            continue
        cefr = cefrs[i]
        data_slice = data_slice[["word", "english", "type"]]

        if is_shuffle:
            filename = f'{DATASET}_two_column_shuffle_{cefr}'
            data_slice = data_slice.sample(frac=1) # shuffle
        if is_alphabetical:
            filename = f'{DATASET}_two_column_alphabetical_{cefr}'
            data_slice = data_slice.sort_values('word')

        data_slice["word"] = data_slice.apply(lambda row: f"{row.word.strip()} ({row.type.strip()})" , axis=1)
        data_slice = data_slice[["word", "english"]]

        style = data_slice.style.format(
            escape="latex",
            )
        style = style.hide(axis='index')
        style = style.hide(axis='columns')

        latex = style.to_latex(
            environment='supertabular',
            column_format=column_format
        )

        latex_lines = latex.splitlines()

        latex = '\n'.join((map(fix_latex_line, latex_lines)))

        with open(f'build/{filename}.tex', 'w') as f:
            f.write(latex)

format_latex_columns_by_cefr(is_alphabetical=False, is_shuffle=True)
format_latex_columns_by_cefr(is_alphabetical=True, is_shuffle=False)

# %%
# 4 column with examples alphabetical
# Fix supertabular and add \textit to type
#column_format = 'p{1.2in}p{2.3in}p{1.2in}p{2.3in}'
# 0.787401575 inches margin total
# A4 width 8.3 inch
#column_format = 'p{1.0in}p{3.0in}p{3.0in}' # total 8.3in - 0.7874in - column_width
#column_format = 'p{0.8in}p{1.1in}p{2.55in}p{2.55in}' # total 8.3in - 0.7874in - column_width
column_format = 'p{0.9in}p{1.0in}p{2.8in}p{2.30in}' # total 8.3in - 0.7874in - column_width
fix_latex_line = FixLatexLine(column_format).fix_latex_line

def format_latex_columns_by_cefr_with_example(is_alphabetical=True, is_shuffle=False):
    data = load_data()
    data["example_spanish"] = data.apply(lambda row: replace_word_in_field_with_underscore(row.word, row.example_spanish) , axis=1)

    cefrs, data_by_cefr = cefrs_data_by_dataset(data)

    for i, data_slice in enumerate(data_by_cefr):
        if data_slice.empty:
            continue
        cefr = cefrs[i]
        data_slice = data_slice[["word", "english", "example_spanish", "example_english", "type"]]

        if is_alphabetical:
            data_slice = data_slice.sort_values('word')
            filename = f'{DATASET}_two_column_alphabetical_{cefr}_with_example'
        if is_shuffle:
            data_slice = data_slice.sample(frac=1) # shuffle
            filename = f'{DATASET}_two_column_shuffle_{cefr}_with_example'

        data_slice["word"] = data_slice.apply(lambda row: f"{row.word.strip()} ({row.type.strip()})" , axis=1)
        data_slice = data_slice[["word", "english", "example_spanish", "example_english"]]

        style = data_slice.style.format(
            escape="latex",
            )
        style = style.hide(axis='index')
        style = style.hide(axis='columns')

        latex = style.to_latex(
            environment='supertabular',
            column_format=column_format
        )

        latex_lines = latex.splitlines()

        latex = '\n'.join((map(fix_latex_line, latex_lines)))

        with open(f'build/{filename}.tex', 'w') as f:
            f.write(latex)

format_latex_columns_by_cefr_with_example(is_alphabetical=True, is_shuffle=False)
format_latex_columns_by_cefr_with_example(is_alphabetical=False, is_shuffle=True)
