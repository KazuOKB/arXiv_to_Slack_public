import os
import arxiv
import openai
import random
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

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
        print(f"メッセージが正常に送信されました: {response['ts']}")
    except SlackApiError as e:
        print(f"メッセージの送信に失敗しました: {e.response['error']}")

# 使用例
bot_token = "xoxb-1044593597587-8276980833415-yBKi5w5ku0BggMRNHkFeRaj1"  # Bot Tokenをここに記載
channel = "#test_for_bot"  # 送信先のチャンネル名
message = "こんにちは! slack_sdkを使ったメッセージ送信テストです。"
# send_slack_message(bot_token, channel, message)

def arXiv_info():
    # 検索クエリを設定（gr-qcカテゴリの論文を対象）
    # arXivではカテゴリは "cat:" プレフィックスを使うので、ここでは gr-qc を指定
    query = 'cat:gr-qc'
    # arxiv APIで最新の論文情報を取得する
    search = arxiv.Search(
        query=query,  # 検索クエリ
        max_results=50,  # 最新の論文3本のみ取得
        sort_by=arxiv.SortCriterion.SubmittedDate,  # 論文を投稿された日付でソートする
        sort_order=arxiv.SortOrder.Descending,  # 新しい論文から順に取得する
    )

    # 取得結果をリストに変換
    results = list(search.results())
    # 結果数が3件未満の場合はそのまま表示、そうでなければランダムに3本を選択
    num_papers = 3
    if len(results) < num_papers:
        selected_papers = results
    else:
        selected_papers = random.sample(results, k=num_papers)

    # 取得した論文リストから情報を表示
    for idx, paper in enumerate(selected_papers, start=1): #search.results() にすると新しい順
        arxiv_paper_info = []
        arxiv_number = paper.entry_id.split('/')[-1]
        paper_url = paper.entry_id  # 論文のURL
        paper_link = f"<{paper_url}|arXiv: {arxiv_number}>"  # URLをリンク形式にする
        paper_number = f"リンク: {paper_link}"
        paper_index = f"----- {paper_link}  -----"
        paper_title = f"タイトル: {paper.title}"
        authors = ', '.join(author.name for author in paper.authors)
        peper_authors = "著者:" + str(authors)
        paper_abstract = "アブストラクト:" + str(paper.summary)

        arxiv_paper_info.append(paper_index)
        arxiv_paper_info.append("\n")
        arxiv_paper_info.append(paper_title)
        arxiv_paper_info.append("\n")
        arxiv_paper_info.append(peper_authors)
        arxiv_paper_info.append("\n")
        arxiv_paper_info.append(paper_abstract)
        
        send_slack_message(bot_token, channel, str(''.join(arxiv_paper_info)))

if __name__ == "__main__":
    arXiv_info()
