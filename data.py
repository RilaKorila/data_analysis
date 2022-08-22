import numpy as np
import pandas as pd


class Data:
    def __init__(self, title):
        self.title = title

        if self.title == "A: 市区町村":
            self.path = "./data/SSDSE-A-2022.csv"
            self.category_rows = ["地域コード", "都道府県", "市区町村"]

        elif self.title == "B: 県別推移":
            self.path = "./data/SSDSE-B-2022.csv"
            self.category_rows = []

        elif self.title == "C: 家計消費":
            self.path = "./data/SSDSE-C-2022.csv"
            self.category_rows = []

        elif self.title == "D: 社会生活":
            self.path = "./data/SSDSE-D-2022.csv"
            self.category_rows = []

        else:
            self.path = "./data/SSDSE-E-2022.csv"
            self.category_rows = []

        self.df = pd.read_csv(self.path)

        # 数値データだけ取り出す
        tmp = self.df.copy()
        self.only_numeric = tmp.drop(self.category_rows, axis=1)
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
