import sys
import ginza
import spacy
from spacy import displacy

nlp = spacy.load('ja_ginza')
filepath: str = sys.argv[1]

with open(filepath) as f:
    s: str = f.read()

doc = nlp(s)
text: str = ''

for sent in doc.sents:
    for span in ginza.bunsetu_spans(sent):
        for token in span.lefts:
            text = text + '\n' + (str(ginza.bunsetu_span(token)) + ' → ' + str(span))

with open(filepath + '.dat', 'w', encoding='UTF_8',newline='\n') as f:
    f.write(text)