# 概要（共有するときはAPIキーを空白にしておくこと）
このスクリプトは、

- arXiv APIを用いてgr-qcの論文を最新のものから20本検索
- Geminiを用いてsummaryを日本語で要約
- 論文情報と要約の内容をSlackに投稿
  
を行う。
投稿するSlackのチャンネルはあらかじめ用意されていることを想定。

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

## APIの参考 (arXiv_paper_info.py)
- おまけでつけた arXiv_paper_info.py は arXiv API の使い方を練習するファイル
- [arXiv APIについて](https://info.arxiv.org/help/api/user-manual.html)

