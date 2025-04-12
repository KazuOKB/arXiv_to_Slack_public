# 概要
- このスクリプトは、
    - arxiv apiを用いてgr-qcの論文を最新のものから20本検索
    - Geminiを用いてsummaryを日本語で要約
    - 論文情報と要約の内容をSlackに投稿
を行います。
- 投稿するSlackのチャンネルはあらかじめ用意されていることを想定しています。

# APIの参考

- 参考サイト
    - [arXiv APIについて](https://info.arxiv.org/help/api/user-manual.html)
    - [Slack APIについて]()
### appの作成
1. [ここ](https://api.slack.com/apps?new_app=1)から新しいappを作る
2. OAuth & Permissionsから以下のScopesを設定 & slackのWorkspaceにinstall
    - ここから
    ![img1](./docs/imgs/img1.png)
    - Scopeの設定項目


# Geminiへの要請 (arXiv_to_slackbot_gemini.py)
geminiに論文を要約させるためのprompt。現状以下のように設定しています：
```.txt
    制約条件:
    ```与えられた論文の要点を3点のみでまとめ、以下のフォーマットで日本語で出力してください。
    ・要点1
    ・要点2
    ・要点3
    ```
```

