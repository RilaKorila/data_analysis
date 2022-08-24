import numpy as np
import pandas as pd

PREFECTURES = [
    "北海道",
    "青森県",
    "岩手県",
    "宮城県",
    "秋田県",
    "山形県",
    "福島県",
    "茨城県",
    "栃木県",
    "群馬県",
    "埼玉県",
    "千葉県",
    "東京都",
    "神奈川県",
    "新潟県",
    "富山県",
    "石川県",
    "福井県",
    "山梨県",
    "長野県",
    "岐阜県",
    "静岡県",
    "愛知県",
    "三重県",
    "滋賀県",
    "京都府",
    "大阪府",
    "兵庫県",
    "奈良県",
    "和歌山県",
    "鳥取県",
    "島根県",
    "岡山県",
    "広島県",
    "山口県",
    "徳島県",
    "香川県",
    "愛媛県",
    "高知県",
    "福岡県",
    "佐賀県",
    "長崎県",
    "熊本県",
    "大分県",
    "宮崎県",
    "鹿児島県",
    "沖縄県",
]


class Data:
    def __init__(self, title):
        self.title = title
        self.prefecture_filter = False
        self.transition_filter = False

        if self.title == "A: 市区町村":
            self.path = "./data/SSDSE-A-2022.csv"
            self.category_rows = ["地域コード", "都道府県", "市区町村"]

        elif self.title == "B: 県別推移":
            self.path = "./data/SSDSE-B-2022.csv"
            self.category_rows = []
            self.transition_filter = True

        elif self.title == "C: 家計消費":
            self.path = "./data/SSDSE-C-2022.csv"
            self.category_rows = ["地域コード", "都道府県", "市"]

        elif self.title == "D: 社会生活":
            self.path = "./data/SSDSE-D-2021.csv"
            self.category_rows = ["属性", "都道府県"]
            self.prefecture_filter = True

        else:
            self.path = "./data/SSDSE-E-2022.csv"
            self.category_rows = ["都道府県"]
            self.prefecture_filter = False

        self.df = pd.read_csv(self.path)

        # 数値データだけ取り出す
        tmp = self.df.copy()
        tmp = tmp.drop(self.category_rows, axis=1)
        self.only_numeric = tmp
        self.names = tmp.columns.values


def get_corrcoef(data, x_label, y_label):
    cor = np.corrcoef(data[x_label], data[y_label])
    return cor[0, 1].round(4)


# def pick_up_df(df, genre):
#     ans = pd.DataFrame()

#     for elem in genre:
#         grade = elem[0:2]
#         gender = elem[2]
#         ans = ans.append(df[(df["学年"] == grade) & (df["性別"] == gender)])


# # ジャンルに応じてデータをフィルタリングして返す
# def load_filtered_data(data, genre_filter):
#     if genre_filter == "女子":
#         filtered_data = data[data["性別"].isin(["女"])]
#     elif genre_filter == "高1女子":
#         filtered_data = data[data["性別"].isin(["女"])]
#         filtered_data = filtered_data[filtered_data["学年"].isin(["高1"])]
#     else:
#         filtered_data = data

#     return filtered_data


# def get_num_data():
#     tmp = score
#     # 任意の行をとる
#     # delete = teams - rows
#     rows = ["学年", "性別"]
#     tmp = tmp.drop(rows, axis=1)
#     return tmp
