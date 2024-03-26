# %% [markdown]
# # Format 3000,5000,5000 exclusive data to word lists
# format 3000,5000,5000_exclusve in the following formats:
#
# * all data text british: word, type, definition, example, phonetics, cefr
# * all data text usa: word, type, definition, example, phonetics, cefr
# * all data + pronunciation: same as above with clickable HTML
# * 2 column: word, type, definiton
#
# All of the above grouped by cefr

import argparse

from utils.dataset import EnglishData
from utils.utils import replace_word_in_example_with_underscore, FixLatexLine

parser = argparse.ArgumentParser()
parser.add_argument("dataset", default="oxford_3000", choices=["oxford_3000", "oxford_5000", "oxford_5000_exclusive"])
parser.add_argument("--generate_pdf", action="store_true", default=False)
args = parser.parse_args()

DATASET = args.dataset
IS_GENERATE_PDF = args.generate_pdf

load_data = EnglishData(DATASET).load_english

# %% [markdown]
# ## HTML+PDF all columns alphabetical

# %%
# Complete to HTML
data = load_data()

style = data.style.format(
    escape="html",
    )
style = style.hide(axis='index')

html = style.to_html()
filename = DATASET + '_alphabetical'
with open(f'output/{filename}.html', 'w') as f:
    f.write('<meta charset="UTF-8">'+html)


# %%
# Complete to HTML
data = load_data()
data["example"] = data.apply(lambda row: replace_word_in_example_with_underscore(row.word, row.example) , axis=1)

style = data.style.format(
    escape="html",
    )
style = style.hide(axis='index')

html = style.to_html()
filename = DATASET + '_underscore_alphabetical'
with open(f'output/{filename}.html', 'w') as f:
    f.write('<meta charset="UTF-8">'+html)


# %% [markdown]
# ## HTML+PDF all columns grouped by CEFR

# %%
data = load_data()
data["example"] = data.apply(lambda row: replace_word_in_example_with_underscore(row.word, row.example) , axis=1)
print(data["example"][0])
cefrs = ['A1', 'A2', 'B1', 'B2', 'C1']
data_by_cefr = list(map(lambda c : data[data['cefr'] == c], cefrs))

# Complete to HTML
html_out = ''
for data in data_by_cefr:
    if data.empty:
        continue
    cefr = data['cefr'].iloc[0]
    html_out += f'<h2>{cefr}</h2>'
    data = data.drop(['cefr'], axis=1)
    print()
    data = data.rename(columns={'word' : f'word ({cefr})'})

    style = data.style.format(
        escape="html",
        )
    style = style.hide(axis='index')
    html_out += style.to_html()


filename = DATASET+'_underscore_by_cefr'
with open(f'output/{filename}.html', 'w', encoding='utf-8') as f:
    f.write('<meta charset="UTF-8">'+html_out)


# %%
data = load_data()
cefrs = ['A1', 'A2', 'B1', 'B2', 'C1']
data_by_cefr = list(map(lambda c : data[data['cefr'] == c], cefrs))

# Complete to HTML
html_out = ''
for data in data_by_cefr:
    if data.empty:
        continue
    cefr = data['cefr'].iloc[0]
    html_out += f'<h2>{cefr}</h2>'
    data = data.drop(['cefr'], axis=1)
    print()
    data = data.rename(columns={'word' : f'word ({cefr})'})

    style = data.style.format(
        escape="html",
        )
    style = style.hide(axis='index')
    html_out += style.to_html()


filename = DATASET+'_by_cefr'
with open(f'output/{filename}.html', 'w', encoding='utf-8') as f:
    f.write('<meta charset="UTF-8">'+html_out)

# %% [markdown]
# ## HTML+PDF all columns grouped by CEFR shuffle

# %%
# Complete to HTML
html_out = ''
for data in data_by_cefr:
    if data.empty:
        continue
    data = load_data()
    cefr = data['cefr'].iloc[0]
    html_out += f'<h2>{cefr}</h2>'
    data = data.drop(['cefr'], axis=1)
    print()
    data = data.rename(columns={'word' : f'word ({cefr})'})
    data = data.sample(frac=1)

    style = data.style.format(
        escape="html",
        )
    style = style.hide(axis='index')
    html_out += style.to_html()


filename = DATASET+'_by_cefr_shuffle'
with open(f'output/{filename}.html', 'w', encoding='utf-8') as f:
    f.write('<meta charset="UTF-8">'+html_out)

# to pdf


# %%
# Complete to HTML
html_out = ''
for data in data_by_cefr:
    if data.empty:
        continue
    data = load_data()
    cefr = data['cefr'].iloc[0]
    html_out += f'<h2>{cefr}</h2>'
    data = data.drop(['cefr'], axis=1)
    print()
    data = data.rename(columns={'word' : f'word ({cefr})'})
    data = data.sample(frac=1)

    style = data.style.format(
        escape="html",
        )
    style = style.hide(axis='index')
    html_out += style.to_html()


filename = DATASET+'_by_cefr_shuffle'
with open(f'output/{filename}.html', 'w', encoding='utf-8') as f:
    f.write('<meta charset="UTF-8">'+html_out)

# to pdf


# %% [markdown]
# ## 2 Column LateX word,type and definition alphabetical


# %%
# 2 Column word + definition
data = load_data()
data = data[["word", "definition"]]

style = data.style.format(
    escape="latex",
    )
style = style.hide(axis='index')
style = style.hide(axis='columns')

column_format = 'p{1.2in}p{2.3in}p{1.2in}p{2.3in}'
fix_latex_line = FixLatexLine(column_format).fix_latex_line

latex = style.to_latex(
    environment='supertabular',
    column_format=column_format
)

latex_lines = latex.splitlines()
latex = '\n'.join((map(fix_latex_line, latex_lines)))

filename = DATASET + '_table_alphabetical'
with open(f'./build/{filename}.tex', 'w') as f:
    f.write(latex)

# %% [markdown]
# ## 2 Column LateX word,type and definition by CEFR

# %%
data = load_data()
cefrs = ['A1', 'A2', 'B1', 'B2', 'C1']
data_by_cefr = list(map(lambda c : data[data['cefr'] == c], cefrs))

# %%
data_by_cefr[1].head()

# %%
for data, cefr in zip(data_by_cefr, cefrs):
    if data.empty:
        continue
    data = data[["word", "definition", "type", "cefr"]]
    data["word"] = data.apply(lambda row: f"{row.word.strip()} ({row.type.strip()})" , axis=1)
    data = data[["word", "definition"]]

    style = data.style.format(
        escape="latex",
        )
    style = style.hide(axis='index')
    style = style.hide(axis='columns')

    column_format = 'p{1.2in}p{2.3in}p{1.2in}p{2.3in}'
    fix_latex_line = FixLatexLine(column_format).fix_latex_line
    latex = style.to_latex(
        environment='supertabular',
        column_format=column_format
    )

    latex_lines = latex.splitlines()

    latex = '\n'.join((map(fix_latex_line, latex_lines)))

    filename = f'{DATASET}_{cefr}'
    with open(f'build/{filename}.tex', 'w') as f:
        f.write(latex)

# %% [markdown]
# ## 2 Column LateX word,type and definition by CEFR shuffle

# %%
for data, cefr in zip(data_by_cefr, cefrs):
    if data.empty:
        continue
    data = data[["word", "definition", "type", "cefr"]]
    data["word"] = data.apply(lambda row: f"{row.word.strip()} ({row.type.strip()})" , axis=1)
    data = data[["word", "definition"]]

    data = data.sample(frac = 1)

    style = data.style.format(
        escape="latex",
        )
    style = style.hide(axis='index')
    style = style.hide(axis='columns')

    column_format = 'p{1.2in}p{2.3in}p{1.2in}p{2.3in}'
    fix_latex_line = FixLatexLine(column_format).fix_latex_line
    latex = style.to_latex(
        environment='supertabular',
        column_format=column_format
    )

    latex_lines = latex.splitlines()
    latex = '\n'.join((map(fix_latex_line, latex_lines)))

    filename = f'{DATASET}_shuffle_{cefr}'
    with open(f'build/{filename}.tex', 'w') as f:
        f.write(latex)

if IS_GENERATE_PDF:
    # pandoc with wkhtml or
    # wkhtmltopdf --user-style-sheet format/table.css output/oxford_3000_alphabetical.html output/oxford_3000_alphabetical.pdf
    import os
    filename = DATASET+'_by_cefr_shuffle'
    cmd = f"""pandoc -f html -t pdf output/{filename}.html -t html5 -o output/{filename}.pdf --metadata pagetitle="{filename}" -V margin-top=2 -V margin-bottom=2 -V margin-left=2 -V margin-right=2 -c format/table.css  --title '{filename}'"""
    os.system(cmd)

    filename = DATASET+'_by_cefr_shuffle'
    cmd = f"""pandoc -f html -t pdf output/{filename}.html -t html5 -o output/{filename}.pdf --metadata pagetitle="{filename}" -V margin-top=2 -V margin-bottom=2 -V margin-left=2 -V margin-right=2 -c format/table.css  --title '{filename}'"""
    os.system(cmd)

    filename = DATASET+'_by_cefr'
    cmd = f"""pandoc -f html -t pdf output/{filename}.html -t html5 -o output/{filename}.pdf --metadata pagetitle="{filename}" -V margin-top=2 -V margin-bottom=2 -V margin-left=2 -V margin-right=2 -c format/table.css  --title '{filename}'"""
    os.system(cmd)

    filename = DATASET+'_underscore_by_cefr'
    cmd = f"""pandoc -f html -t pdf output/{filename}.html -t html5 -o output/{filename}.pdf --metadata pagetitle="{filename}" -V margin-top=2 -V margin-bottom=2 -V margin-left=2 -V margin-right=2 -c format/table.css  --title '{filename}'"""
    os.system(cmd)

    filename = DATASET + '_underscore_alphabetical'
    cmd = f'pandoc -f html -t pdf output/{filename}.html -t html5 -o output/{filename}.pdf --metadata pagetitle="{filename}" -V margin-top=2 -V margin-bottom=2 -V margin-left=2 -V margin-right=2 -c format/table.css '
    os.system(cmd)

    filename = DATASET + '_alphabetical'
    cmd = f'pandoc -f html -t pdf output/{filename}.html -t html5 -o output/{filename}.pdf --metadata pagetitle="{filename}" -V margin-top=2 -V margin-bottom=2 -V margin-left=2 -V margin-right=2 -c format/table.css '
    os.system(cmd)

    # latexmk to convert format tex files. Must be run from format as wd
    # Run terminal cd format latexmk oxford*.tex to finish build pdfs
    cmd_build = f"latexmk -pdf -cd format/{DATASET}*.tex -outdir=../output" 
    os.system(cmd_build)
