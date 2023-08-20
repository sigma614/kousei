"""Trelloのカードを読み込んでコミットメッセージに表示"""

import json
import os
import subprocess
from typing import Final, Union

import requests
from dotenv import load_dotenv

load_dotenv(verbose=True)

LIST_API: Final[str] = 'https://api.trello.com/1/lists'
DOING_LIST: Final[str] = '60814b5e1b596b8e5151cca5'

CHARA_CODE: Final[str] = 'UTF_8'
LINE_CODE: Final[str] = '\n'

GIT_CMD: Final[list[str]] = ['git', 'config', 'commit.template']

TXT: Final[str] = """
# ==== Readme ====
# 作業内容をコメントアウトするか記入してください
# やることが完了したら、対応する「# fix ID」行をコメントアウトすると、カードが「やった」リストに送られます

# ==== :emoji: ====
# 📝memo ----------- 執筆
# ♻️recycle -------- カイゼン
# ✅white_check_mark lint
# 🐛bug ------------ バグ修正
# 📦package -------- ライブラリ"""  # 文末に表示する説明


def main() -> None:
    """Trelloのカードを読み込んでコミットメッセージに表示"""
    list: Union[list[dict[str, str]], None] = read_trello()
    if list is not None:
        output: str = output_txt(list)
        print(list)
        write_txt(output)


def read_trello() -> Union[list[dict[str, str]], None]:
    """Trelloの「やる」リストのカードを読み込む

    Returns:
        Union[list[dict[str, str]], None]: カード一覧（読み込み失敗したらNone）
    """
    trello_key: Union[str, None] = os.getenv('TRELLO_KEY')
    trello_token: Union[str, None] = os.getenv('TRELLO_TOKEN')

    if trello_key is not None and trello_token is not None:
        try:
            r: requests.Response = requests.get(
                f'{LIST_API}/{DOING_LIST}/cards?key={trello_key}'
                f'&token={trello_token}&fields=name')
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(e)
        else:
            return json.loads(r.text)
    else:
        return None


def output_txt(json: list[dict[str, str]]) -> str:
    """コミットメッセージのテンプレートにTrelloのカード一覧を追加

    Args:
        json (list[dict[str, str]]): Trelloのカード一覧

    Returns:
        str: テンプレート
    """

    output: str = ''
    for i in json:
        output += f"# ♻{i['name']}" + '\n'

    for i in json:
        output += f"# fix {i['id']}" + '\n'

    output += TXT
    return output


def write_txt(output: str) -> None:
    """テンプレートに書き込む

    Args:
        output (str): 書き込む内容
    """
    filename: str = subprocess.run(GIT_CMD, capture_output=True,
                                   text=True).stdout.strip()
    if filename != '':
        try:
            with open(filename, 'w', encoding=CHARA_CODE,
                      newline=LINE_CODE) as f:
                f.write(output)
        except OSError as e:
            print(e)


if __name__ == '__main__':
    main()
