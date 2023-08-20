"""
sumyでドキュメント要約を行うサンプルプログラム
"""
# spaCy
import spacy
from typing import Final
# sumy
from sumy.parsers.plaintext import PlaintextParser
# 以下、要約アルゴリズム
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.reduction import ReductionSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from sumy.summarizers.kl import KLSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer


# 前処理と言えば前処理　 -----------------------------

# GiNZA/spaCyの初期化
nlp = spacy.load('ja_ginza')

# sumy の sumy.nlp.tokenizers.Tokenizerに似せた、オリジナルのTokenizerを定義
#   https://github.com/miso-belica/sumy/blob/master/docs/how-to-add-new-language
class myTokenizer:
    @staticmethod
    def to_sentences(text) -> list[str] :
        return [str(s) for s in nlp(text).sents] # spaCyは、「sents」で文のジェネレータを戻す

    @staticmethod
    def to_words(sentence) -> list[str] :
        l = next(nlp(sentence).sents).lemma_  # spaCyは、「lemma_」で文のレンマ化した文字列を戻す
        return l.split(' ')  # spacy/GiNZAの仕様により、半角スペース区切りでトークン化されるようなのでそれを前提にリストにする

# ドキュメントの読み込み
doc_str: str = open('unno.txt').read().replace(' ', '').replace('　', '')  # 今回は、スペースは最初の時点でストップワードとして除外しておく。

# 何行に要約するかの値を算出
# (※これはsumy利用のポイントではなく、筆者がお試しするのにこうしておくのが便利だと思った味付け。
# この味付けは不要、単に3行に要約したければ、sentences_count=3 とすれば良い）
num: int = len(doc_str.split('。'))  # 句点の数を文の数とみなす。
N: Final[int] = 3
sentences_count: int = N if num < 100 else int(num/10) # 長めの文章なら10分の1に、そうでなければN行に要約

# パーサーの設定（入力ドキュメントを読み込ませて、Tokenizerでコーパスを生成する...など)
parser = PlaintextParser.from_string(doc_str, myTokenizer())


# 以下、アルゴリズムを指定して要約する -----------------------------

def summarize(summarizer) -> None: # 出力関数(手抜き)
    result = summarizer(document=parser.document, sentences_count=sentences_count)
    print('\n',summarizer)
    for s in result: print(s)


##
summarize(LexRankSummarizer())

##
summarize(LsaSummarizer())

## 
summarize(ReductionSummarizer())

##
summarize(LuhnSummarizer())

##
summarize(SumBasicSummarizer())

##
summarize(KLSummarizer())

##　
# summarize(EdmundsonSummarizer())
##  bonus_wordsが必要と怒られるので、この呼び出し方ではダメなので省略

