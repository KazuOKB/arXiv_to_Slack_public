#!/bin/sh
# ─────────────────────────────────────────────
# このスクリプトを実行すると、仮想環境apiを起動して
# 同じディレクトリ内の Python スクリプトを一度だけ動かします。
# ─────────────────────────────────────────────

# (1) このシェルスクリプト自身のあるディレクトリに移動
cd "$(dirname "$0")"

# (2) conda run で環境"api"のPythonを呼び出しスクリプトを実行
# activate/source は一切せずに、conda run だけ使う
/opt/anaconda3/bin/conda run -n api python3 my_arXiv_slackbot.py