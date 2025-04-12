# 概要
- このスクリプトは、
    - arXiv APIを用いてgr-qcの論文を最新のものから20本検索
    - Geminiを用いてsummaryを日本語で要約
    - 論文情報と要約の内容をSlackに投稿
を行います。
- 投稿するSlackのチャンネルはあらかじめ用意されていることを想定しています。

## Geminiへの要請 (arXiv_to_slackbot_gemini.py)
geminiに論文を要約させるためのprompt。現状以下のように設定しています：
```.txt
    制約条件:
    ```与えられた論文の要点を3点のみでまとめ、以下のフォーマットで日本語で出力してください。
    ・要点1
    ・要点2
    ・要点3
    ```
```

## Slack API Token のScopeについて
OAuth & Permissions にて "chat:write" と "channels:join" を追加

## APIの参考
- [arXiv APIについて](https://info.arxiv.org/help/api/user-manual.html)
