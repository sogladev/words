import re

# Replaces given word in field with '_'
def replace_word_in_field_with_underscore(word: str, example):
    example_split = example.split(' ')
    def _replace(e):
        if word not in e:
           return e
        if not re.match(f"^{word}.*?$", e, re.IGNORECASE):
            return e
        return e.replace(word, '_')
    example_split_replaced = list(map(lambda e: _replace(e), example_split))
    return ' '.join(example_split_replaced)

# Fix supertabular and add \textit to type
class FixLatexLine:
    def __init__(self, column_format):
        self.column_format = column_format

    def fix_latex_line(self, line):
        if re.match(r"^\\begin{supertabular}", line):
            # Add column_format to supertabular}
            return '\\begin{supertabular}'+'{'+self.column_format+'}' 
        if re.match(r"^\\.*{tabular}", line):
            # Remove {tabular}
            return ''
        if re.match(r"^\w+\s.*\(\w+\s?\w+?\)", line):
            # Italics
            return re.sub(r"(^\w+\s.*)(\(\w+\s?\w+?\))", r"\1\\textit{\2}", line)
        return line
