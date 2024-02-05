# %%
import pandas as pd
import os
import re

# %%
DATASET = 'spanish_5000'

# %%
df2 = pd.read_pickle(f"./data/spanish2.pkl")
df2.head()

# %%
# "word": word, "type": type, "english": english, "frequency_rank": frequency_rank, "example_spanish": example_spanish, "example_english": example_english
def load_data2():
    data = df2[["word", "type", "english", "example_spanish", "example_english", "frequency_rank"]]
    return data

# %%
# Replaces given word in field with '_'
def replace_word_in_field_with_underscore(word, field):
    field_split = field.split(' ')
    def _replace(e):
        if word not in e:
           return e
        if not re.match(f"^{word}.*?$", e):
            return e
        return e.replace(word, '_')
    field_split_replaced = list(map(lambda e: _replace(e), field_split))
    return ' '.join(field_split_replaced)

# %% [markdown]
# ## HTML+PDF all columns

# %%
# HTML, Underscore, Shuffled and Alphabetical

def format_html_all_columns(is_shuffle=True, is_alphabetical=False, with_underscore=True):
    data = load_data2()
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
    f.write(html)

filename = DATASET+'_underscore_shuffled'
html = format_html_all_columns(is_shuffle=True, is_alphabetical=False, with_underscore=True)
with open(f'output/{filename}.html', 'w') as f:
    f.write(html)

filename = DATASET+'_shuffled'
html = format_html_all_columns(is_shuffle=True, is_alphabetical=False, with_underscore=False)
with open(f'output/{filename}.html', 'w') as f:
    f.write(html)

filename = DATASET+'_alphabetical'
html = format_html_all_columns(is_shuffle=False, is_alphabetical=True, with_underscore=False)
with open(f'output/{filename}.html', 'w') as f:
    f.write(html)

filenames = [DATASET+'_alphabetical', DATASET+'_shuffled', DATASET+'_underscore_shuffled', DATASET + '_underscore_alphabetical']
for filename in filenames:
    cmd = f'pandoc -f html -t pdf output/{filename}.html -t html5 -o output/{filename}.pdf --metadata pagetitle="{filename}" -V margin-top=1cm -V margin-bottom=1cm -V margin-left=1cm -V margin-right=1cm -c format/table.css --pdf-engine-opt=--enable-local-file-access'
    os.system(cmd)

# ## HTML+PDF all columns grouped by CEFR

# By Ranking / pseudo-cefr. Shuffled

# Complete to HTML
def format_html_columns_by_cefr(is_shuffle=True, is_alphabetical=False, with_underscore=True):
    data = load_data2()
    if with_underscore:
        data["example_spanish"] = data.apply(lambda row: replace_word_in_field_with_underscore(row.word, row.example_spanish) , axis=1)
    data.head()

    data_by_cefr = [
        data.iloc[:1000],
        data.iloc[1000:2000],
        data.iloc[2000:3000],
        data.iloc[3000:4000],
        data.iloc[4000:],
        ]

    data_by_cefr[1].head()
    cefrs = ['A1', 'A2', 'B1', 'B2', 'C1']

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
    f.write(html)

filename = DATASET+'_underscore_by_cefr_alphabetical'
html = format_html_columns_by_cefr(is_shuffle=False, is_alphabetical=True, with_underscore=True)
with open(f'output/{filename}.html', 'w', encoding='utf-8') as f:
    f.write(html)


for filename in [DATASET+'_underscore_by_cefr_shuffled', DATASET+'_underscore_by_cefr_alphabetical']:
    cmd = f"""pandoc -f html -t pdf output/{filename}.html -t html5 -o output/{filename}.pdf --metadata pagetitle="{filename}" -V margin-top=2 -V margin-bottom=2 -V margin-left=2 -V margin-right=2 -c format/table.css --pdf-engine-opt=--enable-local-file-access --title '{filename}'"""
    os.system(cmd)


# %%
# 2 column 5000 not by rank
# shuffle and alphabetical
import re
# Fix supertabular and add \textit to type
column_format = 'p{1.2in}p{2.3in}p{1.2in}p{2.3in}'
def fix_latex_line(line):
    if re.match(r"^\\begin{supertabular}", line):
        # Add column_format to supertabular}
        return '\\begin{supertabular}'+'{'+column_format+'}'
    if re.match(r"^\\.*{tabular}", line):
        # Remove {tabular}
        return ''
    if re.match(r"^\w+\s.*\(\w+\s?\w+?\)", line):
        # Italics
        return re.sub(r"(^\w+\s.*)(\(\w+\s?\w+?\))", r"\1\\textit{\2}", line)
    return line

def format_latex_columns(is_alphabetical=False, is_shuffle=True):
    # columns = ["word", "type", "english", "frequency_rank"]
    data = load_data2()
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

# %%
# two column, cefr by rank
import re
# Fix supertabular and add \textit to type
column_format = 'p{1.2in}p{2.3in}p{1.2in}p{2.3in}'
def fix_latex_line(line):
    if re.match(r"^\\begin{supertabular}", line):
        # Add column_format to supertabular}
        return '\\begin{supertabular}'+'{'+column_format+'}'
    if re.match(r"^\\.*{tabular}", line):
        # Remove {tabular}
        return ''
    if re.match(r"^\w+\s.*\(\w+\s?\w+?\)", line):
        # Italics
        return re.sub(r"(^\w+\s.*)(\(\w+\s?\w+?\))", r"\1\\textit{\2}", line)
    return line

def format_latex_columns_by_cefr(is_alphabetical=True, is_shuffle=False):
    data = load_data2()
    data_by_cefr = [
        data.iloc[:1000], #A1
        data.iloc[1000:2000], #A2
        data.iloc[2000:3000], #B1
        data.iloc[3000:4000], #B2
        data.iloc[4000:], #C1
        ]

    cefrs = ['A1', 'A2', 'B1', 'B2', 'C1']
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

        #data_slice = data_slice.sort_values('word')
        #data_slice = data_slice.rename(columns={'word' : f'word ({cefr})'})

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
import re
# Fix supertabular and add \textit to type
#column_format = 'p{1.2in}p{2.3in}p{1.2in}p{2.3in}'
# 0.787401575 inches margin total
# A4 width 8.3 inch
#column_format = 'p{1.0in}p{3.0in}p{3.0in}' # total 8.3in - 0.7874in - column_width
#column_format = 'p{0.8in}p{1.1in}p{2.55in}p{2.55in}' # total 8.3in - 0.7874in - column_width
column_format = 'p{0.9in}p{1.0in}p{2.8in}p{2.30in}' # total 8.3in - 0.7874in - column_width
#column_format = 'ccc'
def fix_latex_line(line):
    if re.match(r"^\\begin{supertabular}", line):
        # Add column_format to supertabular}
        return '\\begin{supertabular}'+'{'+column_format+'}'
    if re.match(r"^\\.*{tabular}", line):
        # Remove {tabular}
        return ''
    if re.match(r"^\w+\s.*\(\w+\s?\w+?\)", line):
        # Italics
        return re.sub(r"(^\w+\s.*)(\(\w+\s?\w+?\))", r"\1\\textit{\2}", line)
    return line

def format_latex_columns_by_cefr_with_example(is_alphabetical=True, is_shuffle=False):

    data = load_data2()
    data["example_spanish"] = data.apply(lambda row: replace_word_in_field_with_underscore(row.word, row.example_spanish) , axis=1)
    data_by_cefr = [
        data.iloc[:1000], #A1
        data.iloc[1000:2000], #A2
        data.iloc[2000:3000], #B1
        data.iloc[3000:4000], #B2
        data.iloc[4000:], #C1
        ]

    cefrs = ['A1', 'A2', 'B1', 'B2', 'C1']
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

# ## 2 Column LateX word,type and definition by CEFR shuffle

# %%
# Run terminal cd format latexmk oxford*.tex to finish build pdfs
cmd_build = f"latexmk -pdf -cd format/{DATASET}*.tex -outdir=../output"
os.system(cmd_build)