import sys
import spacy
from spacy.pipeline import EntityRuler
from typing import Final

PATTERNS: Final[list[dict[str, str]]] = [
    {"label": "PERSON", "pattern": "ジェイド"}
]
COLORS: Final[dict[str, str]] = {
    blue: '#ccccff',
    yellow: '#ffffcc',
    red: '#ffcccc',
    aqua: '#ccffff',
    green: '#ccffcc'
}

nlp = spacy.load('ja_ginza')
ruler = EntityRuler(nlp, overwrite_ents=True)
ruler.add_patterns(PATTERNS)
nlp.add_pipe(ruler)

filepath: str = sys.argv[1]

with open(filepath) as f:
    s = f.read()

doc: str = nlp(s)

spacy.displacy.serve(
    doc,
    style='ent',
    page=False,
    host='localhost',
    options={
        'colors': {
            'ANIMAL_PART': COLORS['red'],
            'CLOTHING': COLORS['aqua'],
            'PERSON':COLORS['blue'],
            'COLOR_OTHER': COLORS['yellow'], 'NATURE_COLOR': COLORS['yellow'],
            'TIME': COLORS['green'], 'PERIOD_TIME': COLORS['green'], 'PERIOD_YEAR': COLORS['green'], 'PERIOD_DAY': COLORS['green']
        }
    }
)
