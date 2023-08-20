"""fixしたIDを検索"""
import done
from typing import Final

def test_fix() -> None:
    lines: Final[list[str]] = ['test', 'fix 1']

    matchs: list[str] = []

    for line in lines:
        matchs.append(done.match_id(line))

    assert matchs[0] == ''
    assert matchs[1] == '1'
