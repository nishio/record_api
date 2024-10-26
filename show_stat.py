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

# 時系列でソート
for conversation_id in conversation_data:
    conversation_data[conversation_id].sort(key=lambda x: x[0])

# # クラスタ数を時系列でプロット
# plt.figure(figsize=(10, 6))
# for conversation_id, records in conversation_data.items():
#     times = [record[0] for record in records]
#     cluster_counts = [record[1] for record in records]
#     plt.plot(times, cluster_counts, label=f"Conversation {conversation_id}")

# plt.xlabel("Time")
# plt.ylabel("Number of Clusters")
# plt.title("Number of Clusters over Time for Each Conversation")
# plt.legend()
# plt.grid(True)
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

# Conversation IDごとに、最もクラスタ数が多くて、その中で最も新しいデータを表示
for conversation_id, records in conversation_data.items():
    records.sort()
    best_record = records[-1]
    num_cluster = best_record[0]
    timestamp = best_record[1]
    num_votes = best_record[2]

    print(
        f"Conversation ID: {conversation_id}, Number of Clusters: {num_cluster}, Timestamp: {timestamp}, Total Votes: {num_votes}"
    )

conversation_dict = {
    "69rmeiumcr": "経済政策・物価高対策",
    "42pditmrma": "社会保障（年金・医療）",
    "77anwcwh4b": "憲法",
    "35r8w9kkfp": "税制",
    "32ffrfvrrf": "政治資金規制改革",
    "3dzkftnmrm": "エネルギー政策",
}

print("-" * 50)
print("Conversationごと、クラスタサイズごとに最新のデータを表示")
# Conversation IDごとに、クラスタサイズごとに最新のデータを表示
for conversation_id, records in conversation_data.items():
    records.sort()
    # クラスタサイズごとにデータを格納する辞書
    cluster_size_dict = {}

    # 各レコードを確認して、クラスタサイズごとに最新のタイムスタンプを記録
    for record in records:
        num_cluster, timestamp, num_votes = record
        # if num_cluster not in cluster_size_dict:
        cluster_size_dict[num_cluster] = (timestamp, num_votes)
        # elif timestamp > cluster_size_dict[num_cluster][1]:
        #     cluster_size_dict[num_cluster] = (timestamp, num_votes)

    # 結果を表示
    for num_cluster, (timestamp, num_votes) in sorted(cluster_size_dict.items()):
        print(
            f"{conversation_dict[conversation_id]}: Cluster Size: {num_cluster}, Latest Timestamp: {timestamp}, Total Votes: {num_votes}"
        )
    print()
