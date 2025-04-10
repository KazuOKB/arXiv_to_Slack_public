# source path/to/venv/bin/activate

import os
import arxiv
import random
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import google.generativeai as genai
import absl.logging
import datetime
import time


# Initialize absl logging
absl.logging.set_verbosity(absl.logging.INFO)
absl.logging.use_absl_handler()

# # GenemiのAPIキー
genemi_api_key = "AIzaSyCzKzpJ-FKjXvCdGxCRRgiytnPB5g-wVgg"
# Slack APIトークン
SLACK_API_TOKEN = "xoxb-1044593597587-8276980833415-yBKi5w5ku0BggMRNHkFeRaj1"  # Bot Tokenをここに記載
# Slackに投稿するチャンネル名を指定する
SLACK_CHANNEL = "#test_for_bot"

def send_slack_message(token, channel, message):
    """
    Slackにメッセージを送信する関数。

    Parameters:
        token (str): SlackのBot Token。
        channel (str): メッセージを送信するチャンネル（例: '#general'）。
        message (str): 送信するメッセージ。
    """
    client = WebClient(token=token)

    try:
        response = client.chat_postMessage(
            channel=channel,
            text=message
        )
        print(f"メッセージが正常に送信されました")
    except SlackApiError as e:
        print(f"メッセージの送信に失敗しました")

def get_summary(arxiv_paper):
    genai.configure(api_key="AIzaSyCzKzpJ-FKjXvCdGxCRRgiytnPB5g-wVgg")
    model = genai.GenerativeModel("gemini-1.5-flash", system_instruction="""与えられた論文の要点を3点のみでまとめ、以下のフォーマットで日本語で出力してください。
    ・要点1
    ・要点2
    ・要点3            
    """)
    text = f"title: {arxiv_paper.title}\nbody: {arxiv_paper.summary}"
    response = model.generate_content(
        text,
        generation_config = genai.GenerationConfig(
            max_output_tokens=1000,
            temperature=0.7,
        )
    )
    # Initialize absl logging
    absl.logging.set_verbosity(absl.logging.INFO)
    absl.logging.use_absl_handler()
    return str(response.text)

def Translate_to_Japanese(title_in_english):
    genai.configure(api_key="AIzaSyCzKzpJ-FKjXvCdGxCRRgiytnPB5g-wVgg")
    model = genai.GenerativeModel("gemini-1.5-flash", system_instruction="""与えられたタイトルを以下のフォーマットで日本語で出力してください。
    タイトル名
    """)
    text = f"title: {title_in_english}"
    response = model.generate_content(
        text,
        generation_config = genai.GenerationConfig(
            max_output_tokens=1000,
            temperature=0.7,
        )
    )
    # Initialize absl logging
    absl.logging.set_verbosity(absl.logging.INFO)
    absl.logging.use_absl_handler()
    return str(response.text)

def arXiv_info():
    # 検索クエリを設定（gr-qcカテゴリの論文を対象）
    # arXivではカテゴリは "cat:" プレフィックスを使うので、ここでは gr-qc を指定
    query = 'cat:gr-qc'
    # arxiv APIで最新の論文情報を取得する
    search = arxiv.Search(
        query=query,  # 検索クエリ
        max_results=100,  # 最新の論文3本のみ取得
        sort_by=arxiv.SortCriterion.SubmittedDate,  # 論文を投稿された日付でソートする
        sort_order=arxiv.SortOrder.Descending,  # 新しい論文から順に取得する
    )

    # 取得結果をリストに変換
    results = list(search.results())

    # print(results)

    j = 1
    # 取得した論文リストから情報を表示
    for idx, paper in enumerate(results, start=1): #search.results() にすると新しい順
        if j == 15:
            time.sleep(90)
            j = 1
        
        #今日投稿された論分のみをslackに送信
        # day = str( datetime.date.today() )
        # day = str( datetime.date.today() - datetime.timedelta(days=1) )
        day = str( results[1].published.date() )
        # 2025/1/16に投稿された論文を取得するには　day='2025-01-16'
        if str(paper.published.date()) == day:
            j = j + 1
            arxiv_paper_info = []
            arxiv_number = paper.entry_id.split('/')[-1]
            paper_url = paper.entry_id  # 論文のURL
            paper_link = f"<{paper_url}|arXiv: {arxiv_number}>"  # URLをリンク形式にする
            paper_number = f"リンク: {paper_link}"
            paper_index = f"----- {paper_link}  -----"
            # paper_title = f"タイトル: {Translate_to_Japanese(paper.title)}"
            paper_title = f"タイトル: {paper.title}"
            authors = ', '.join(author.name for author in paper.authors)
            peper_authors = "著者: " + str(authors)
            # paper_abstract = "アブストラクト:" + str(paper.summary)
            paper_summary = "要点:\n" + str(get_summary(paper))

            arxiv_paper_info.append("```")
            arxiv_paper_info.append(paper_index)
            arxiv_paper_info.append(str(paper.published.date()))
            arxiv_paper_info.append("\n")
            arxiv_paper_info.append(paper_title)
            arxiv_paper_info.append("\n")
            arxiv_paper_info.append(peper_authors)
            # arxiv_paper_info.append("\n")
            # arxiv_paper_info.append(paper_abstract)
            arxiv_paper_info.append("\n")
            arxiv_paper_info.append(paper_summary)
            arxiv_paper_info.append("```")

            message = str(''.join(arxiv_paper_info))
            message = message.replace("\n\n", "\n")

            # print(''.join(arxiv_paper_info))
            send_slack_message(SLACK_API_TOKEN, SLACK_CHANNEL, message)

            # print(f"ifbunnonakadesu 論文タイトル: {message}")


if __name__ == "__main__":
    arXiv_info()
