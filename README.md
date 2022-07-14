# Words vocabulary + pronounciation + definition

This project aims to provide easy-to-read and printable vocabulary list of the
most common words of the English/Dutch/French/... language with their meaning.

The word lists contain the following points of data
* Spelling (text)
* Meaning (text)
* Example (text)
* Lexical spelling (text) (optional)
* Pronounciation (audio) (optional)

This project contains scripts to extract data and formatting. 

## Languages so far:
* English: see README.md in [`./english/`](./english)

## Data
Extracted data is hosted seperately on mediafire and can be
found in formats `.pkl`, `.csv`, `.json`

Formatted lists in `/output` are formatted alphabetically, by CEFR rating, random and viewable in
`.pdf` and `.html` format.

## Folder structure for each language
```
├── audio
│   └── *.mp3
├── data
│   ├── data.pkl
│   ├── data.csv
│   ├── data.json
├── output
│   ├── output.html
│   └── output.pdf
├── format.ipynb
└── scrape.ipynb
```