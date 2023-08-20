"""テンプレート出力テスト"""
import template
from typing import Final


def test_template() -> None:
    TXT: Final[list[dict[str, str]]] = [{'id': '1', 'name': 'test'}]
    output: str = template.output_txt(TXT)
    assert output == """# ♻test
# fix 1

# ==== Readme ====
# 作業内容をコメントアウトするか記入してください
# やることが完了したら、対応する「# fix ID」行をコメントアウトすると、カードが「やった」リストに送られます

# ==== :emoji: ====
# 📝memo ----------- 執筆
# ♻️recycle -------- カイゼン
# ✅white_check_mark lint
# 🐛bug ------------ バグ修正
# 📦package -------- ライブラリ"""
