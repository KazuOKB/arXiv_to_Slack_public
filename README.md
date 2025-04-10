# 概要
- このスクリプトは、
    - arxiv apiを用いて論文を検索
    - summaryをgptで要約
    - 論文情報と要約の内容をslackに投稿
を行います。
- slackのチャンネルはそれぞれ、arxiv apiで検索する条件ごとに作られていることを想定しています。

# setting
設定ファイルはjsonファイルで作成しています。各変数は以下です：
- "slack_token_environ_name"
    - slackのトークンを登録した環境変数名
- "open_ai_key_environ_name"
    - open aiのシークレットキーを登録した環境変数名
- "channel_query_dict"
    - 投稿するslackのチャンネルをキー、valueはチャンネルに対応するarxiv apiのquery
    - arxiv apiのquery関しては以下を参照
        - [公式Manual](https://qiita.com/KMD/items/bd59f2db778dd4bf6ed2)
        - [日本語](https://qiita.com/KMD/items/bd59f2db778dd4bf6ed2)
- "max_results"
    - 検索を何個まで行うかの最大数
- "query_time"
    - "now", "yyyy/mm/dd HH:MM", "all"
    - "yyyy/mm/dd HH:MM": 検索したい論文のupdate年月日時を指定する
    - "now": クエリした年月日を対象とする 
        - このスクリプトは最新の論文の要約をslackに投稿しようとして作ったので、このような仕様になっている
        - したがって、基本 "now" で使う想定
    - "all": "max_results" のすべてを使用する場合
        - 現状全チャンネルに対して同じ検索方法となっていることに注意
        - チャンネルごとに検索方法を変えたほうがいいかもしれない
- "gpt_model"
    - 要約に使うgpt model
- "system_text_path"
    - 要約をさせるための指示
    - txtファイル(gpt_system.txt)に別で書いている
- "summarize_mode"
    - 要約にgptを使うかどうか
    - "normal": 論文のabstをそのまま出力
        - gptを使うとお金がかかるのでテスト用として準備
        - このmodeの場合はgptの登録は不要（なはず）
    - "gpt": gptで要約

# gpt_system.txt
gptに論文を要約させるためのprompt。現状以下のように設定しています：
```.txt
    ```以下の制約条件と、入力された文章をもとに最高の要約を出力してください。

    制約条件:
    ・文章は簡潔にわかりやすく。
    ・箇条書きで3行で出力。
    ・1行あたりの文字数は80文字程度。
    ・重要なキーワードは取り逃がさない。
    ・要約した文章は日本語へ翻訳。

    期待する出力フォーマット:
    1.
    2.
    3.
    ```
```
- これは[この記事](https://dev.classmethod.jp/articles/summarize-the-paper-using-chatgpt/)を借用しました。
# 使用方法
## slackでの準備
- 参考サイト
    - [公式のgit](https://github.com/slackapi/python-slack-sdk)

### appの作成
1. [ここ](https://api.slack.com/apps?new_app=1)から新しいappを作る
2. OAuth & Permissionsから以下のScopesを設定 & slackのWorkspaceにinstall
    - ここから
    ![img1](./docs/imgs/img1.png)
    - Scopeの設定項目
