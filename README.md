# 概要（共有するときはAPIキーを空白にしておくこと）
このスクリプトは、

- arXiv APIを用いてgr-qcの論文を最新のものから20本検索
- Geminiを用いてsummaryを日本語で要約
- 論文情報と要約の内容をSlackに投稿
- cron デーモンを使って11 am (JST)に自動的に投稿
  
を行う。
投稿するSlackのチャンネルはあらかじめ用意されていることを想定している。
環境を整えるために environment.yml にAnacondaの仮想環境を用意した。

## Geminiへの要請 (arXiv_to_slackbot_gemini.py)
geminiに論文を要約させるためのprompt。現状以下のように設定している：
```.txt
    制約条件:
    ```与えられた論文の要点を3点のみでまとめ、以下のフォーマットで日本語で出力してください。
    ・要点1
    ・要点2
    ・要点3
    ```
```

## Slack API Token について
- Scope: OAuth & Permissions にて "chat:write" と "channels:join" を追加。
- Slack: 呼び出したいチャンネルにてTokenの追加（招待）。

## run_arxiv.sh について
手動で毎回投稿するのをやめるために、shell script を使って自動化する。
ファイルの中身は my_arXiv_Slackbot.py の実行コマンドをまとめており "./run_arxiv.sh" で実行。
11 am (JST)に投稿するようにするために cron デーモンを使用している。

- cron デーモンの設定の仕方

  ターミナルで"crontab -e"とするとvimが開く
  エディタ内で

  "0 11 * * * /some/directories/arXiv_to_Slack/run_arxiv.sh >> /some/directories/arXiv_to_Slack/logs/cron.log 2>&1"

  を追加。その後":wq"とすれば書き換えてcrontabが保存され終了する。



## APIの参考 (arXiv_paper_info.py)
- おまけでつけた arXiv_paper_info.py は arXiv API の使い方を練習するファイル
- [arXiv APIについて](https://info.arxiv.org/help/api/user-manual.html)

