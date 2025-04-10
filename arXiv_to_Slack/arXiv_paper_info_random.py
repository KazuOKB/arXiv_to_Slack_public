import os
#from slack_sdk import WebClient
#from slack_sdk.errors import SlackApiError
import arxiv
import openai
import random

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
        # arXiv番号を取得
        arxiv_number = paper.entry_id.split("/")[-1]  # “xxxx.xxxx” の部分だけを抽出
        print(f"----- Paper {idx} -----")
        print(f"タイトル: {paper.title}")
        print(f"arXiv番号: {arxiv_number}")  
        # 著者はリストなので、カンマ区切りの文字列に変換
        authors = ', '.join(author.name for author in paper.authors)
        print(f"著者: {authors}")
        print("アブストラクト:")
        print(paper.summary)
        print("\n")

if __name__ == "__main__":
    arXiv_info()
