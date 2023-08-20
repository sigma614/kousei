"""ルビタグ変換"""

import re
import sys
import jaconv
from typing import Final, Pattern

CHARA_FROM: Final[str] = 'SHIFT_JIS'
CHARA_TO: Final[str] = 'UTF_8'
LINE_CODE: Final[str] = '\n'

LATEX_FROMS: Final[dict[str, str]] = {
    'htn': '！？',
    'bkr': '！！',
    'bkr2': 'Bkr',
    'nami': '～～',
    'zenaki': r'(.+)　'
}
LATEX_TOS: Final[dict[str, str]] = {
    'htn': '\\\htn',
    'bkr': '\\\Bkr',
    'bkr2': 'bkr',
    'nami': '\\\nami{}',
    'zenaki': '\\1\\\zenaki{}'
}

HTN_FROM: Final[Pattern[str]] = re.compile('！？')
HTN_TO: Final[str] = '\\\htn'

BKR_FROM: Final[Pattern[str]] = re.compile(r'！！')
BKR_TO: Final[str] = '\\\Bkr'

BKR2_FROM: Final[Pattern[str]] = re.compile(r'Bkr')
BKR2_TO: Final[str] = 'bkr'

ZENAKI_FROM: Final[Pattern[str]] = re.compile(
    r'(.+)　')
ZENAKI_TO: Final[str] = '\\1\\\zenaki{}'

def main() -> None:
    """ファイル名を指定し、ルビ用タグを変換して出力"""
    filename: str = sys.argv[1]
    txt: str = read_file(filename)
    output: str = trans_txt(txt)
    if output != '':
        write_file(filename, output)
    print(output)


def read_file(filename: str) -> str:
    """ファイルの内容を取得

    Args:
        filename (str): ファイル名

    Returns:
        str: 内容
    """
    txt: str = ''
    if filename != '':
        try:
            with open(filename, 'r', encoding=CHARA_FROM,
                      newline=LINE_CODE) as f:
                txt = f.read()
        except OSError as e:
            print(e)
    return txt


def trans_txt(txt: str) -> str:
    """各サイトのルビ用タグを変換

    Args:
        txt (str): 変換する文章
        site (str): 対象サイト

    Returns:
        str: 変換後の文章
    """
    txt = HTN_FROM.sub(HTN_TO, txt)
    txt = BKR_FROM.sub(BKR_TO, txt)
    txt = BKR2_FROM.sub(BKR2_TO, txt)
    txt = jaconv.h2z(txt.capitalize(),digit=True,ascii=True)
    txt = ZENAKI_FROM.sub(ZENAKI_TO, txt)
    return txt


def write_file(filename: str, output: str) -> None:
    """ファイルに書き込む

    Args:
        filename (str): ファイル名
        output (str): 書き込む内容
    """
    if filename != '' and output != '':
        try:
            with open(filename, 'w', encoding=CHARA_TO,
                      newline=LINE_CODE) as f:
                f.write(output)
        except OSError as e:
            print(e)


if __name__ == '__main__':
    main()
