import sys
import re
import ginza
import spacy
from spacy import displacy
nlp = spacy.load('ja_ginza')

txt: str = sys.argv[1]
txt2: str = txt.replace('\n', '').replace('　', '')
doc = nlp(txt2)

def to_dependency_data(doc) -> dict[str, str] :
    words: list[str, str] = []
    arcs: list = []
    bunsetu_head_list = ginza.bunsetu_head_list(doc)
    for i, chunk in enumerate(ginza.bunsetu_spans(doc)):
        words.append({
            'text': chunk.text, 'tag': chunk.label_
        })
        for token in chunk.lefts:
            arcs.append({
                'start': bunsetu_head_list.index(token.i),
                'end': i,
                'label': token.dep_,
                'dir': 'left'
            })
        for token in chunk.rights:
            arcs.append({
                'start': i,
                'end': bunsetu_head_list.index(token.i),
                'label': token.dep_,
                'dir': 'right'
            })
    return {'words': words, 'arcs': arcs}
    
displacy.serve(
    to_dependency_data(doc),
    style='dep',
    # jupyter=True,
    host='localhost',
    manual=True
)

# for sent in doc.sents:
#     for span in ginza.bunsetu_spans(sent):
#         for token in span.lefts:
#             text = text + '\n' + (str(ginza.bunsetu_span(token))+' → '+str(span))
# with open(filepath + '.dat', 'w', encoding='UTF_8',
#             newline='\n') as f:
#     f.write(text)