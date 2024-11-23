import os
import json
import glob
from datetime import datetime
import matplotlib.pyplot as plt

# データが保存されているディレクトリ
data_dir = "data"

# conversation_idごとの時系列データを保存する辞書
conversation_data = {}

# dataディレクトリのすべてのJSONファイルを取得
json_files = glob.glob(os.path.join(data_dir, "*.json"))

# 各ファイルを読み込み
for file in json_files:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

        # ファイル名からconversation_idと日付を抽出
        filename = os.path.basename(file)
        conversation_id, timestamp = filename.split("-", 1)
        timestamp = timestamp.replace(".json", "")
        timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H-%M-%S.%fZ")

        # クラスタ数を取得
        pca = json.loads(data.get("pca", "{}"))
        group_clusters = pca.get("group-clusters", [])
        cluster_count = len(group_clusters)

        # 投票数を取得
        num_votes = pca.get("n", 0)

        # データを辞書に追加
        if conversation_id not in conversation_data:
            conversation_data[conversation_id] = []

        conversation_data[conversation_id].append((cluster_count, timestamp, num_votes))


# # クラスタ数を時系列でプロット
# plt.figure(figsize=(10, 6))
import pandas as pd

# 時系列でソート
for conversation_id in conversation_data:
    conversation_data[conversation_id].sort(key=lambda x: x[1])


conversation_dict = {
    "69rmeiumcr": "経済政策・物価高対策",
    "32ffrfvrrf": "政治資金規制改革",
    "77anwcwh4b": "憲法",
    "42pditmrma": "社会保障（年金・医療）",
    "35r8w9kkfp": "税制",
    "3dzkftnmrm": "エネルギー政策",
    "3zwj5fwytm": "デジタル民主主義",
}


for conversation_id, records in conversation_data.items():
    xs = []
    ys = []
    for record in records:
        cluster_counts = record[0]
        num_votes = record[2]
        if xs == [] or xs[-1] != num_votes:  # remove duplicated data
            xs.append(num_votes)
            ys.append(cluster_counts)

    # # DataFrameに変換
    # df = pd.DataFrame(cluster_counts, columns=["Value"])

    # # 移動平均（例: 窓幅=10）でスムージング
    # df["Smoothed"] = df["Value"].rolling(window=48, center=True).mean()
    # plt.plot(df["Smoothed"], label=f"Conversation {conversation_id}")
    plt.plot(
        xs,
        ys,
    )
    plt.ylim((2, 5))
    # plt.title(conversation_dict[conversation_id])
    plt.show()

# plt.xlabel("Time")
# plt.ylabel("Number of Clusters")
# plt.title("Number of Clusters over Time for Each Conversation")
# plt.legend()
# plt.grid(True)
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()
