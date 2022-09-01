import google_auth_httplib2
import httplib2
import pandas as pd
import plotly.express as px
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest

from data import PREFECTURES, Data, get_corrcoef

SCOPE = "https://www.googleapis.com/auth/spreadsheets"
SHEET_ID = "RIQusere1l7Y-GpCrevV2C1im-n7auMphOqoWiAfkUE"
SHEET_NAME = "db"


@st.experimental_singleton()
def connect_to_gsheet():
    # Create a connection object
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=[SCOPE]
    )

    # Create a new Http() object for every request
    def build_request(http, *args, **kwargs):
        new_http = google_auth_httplib2.AuthorizedHttp(
            credentials, http=httplib2.Http()
        )

        return HttpRequest(new_http, *args, **kwargs)

    authorized_http = google_auth_httplib2.AuthorizedHttp(
        credentials, http=httplib2.Http()
    )

    service = build("sheets", "v4", requestBuilder=build_request, http=authorized_http)
    gsheet_connector = service.spreadsheets()

    return gsheet_connector


def add_row_to_gsheet(gsheet_connector, row):
    gsheet_connector.values().append(
        spreadsheetId=SHEET_ID,
        range=f"{SHEET_NAME}!A:E",
        body=dict(values=row),
        valueInputOption="USER_ENTERED",
    ).execute()

## ログ取得用
gsheet_connector = connect_to_gsheet()

@st.cache
def load_full_data(d_name):
    return Data(d_name)


def main():
    if "page" not in st.session_state:
        st.session_state.page = "vis"

    st.sidebar.markdown("## ページ切り替え")
    # --- データ: 選択ラジオボタン
    d_name = st.sidebar.radio(
        "データ選択", ("A: 市区町村", "B: 県別推移", "C: 家計消費", "D: 社会生活", "E: 基本生活")
    )

    # --- page振り分け
    st.session_state.page = "vis"
    vis(d_name)


# ---------------- グラフで可視化 :  各グラフを選択する ----------------------------------
def vis(d_name):
    st.title("選択したデータ - " + d_name)
    data = load_full_data(d_name)

    st.sidebar.markdown("## いろんなグラフを試してみよう")

    # sidebar でグラフを選択
    graph = st.sidebar.radio("グラフの種類", ("散布図", "ヒストグラム", "箱ひげ図", "折れ線グラフ"))

    if graph == "散布図":

        if data.transition_filter:
            st.warning("このデータは散布図には対応していません")

        elif data.prefecture_filter:
            left, right = st.columns(2)
            with left:  # 散布図の表示
                x_label = st.selectbox("横軸を選択", data.names)
                y_label = st.selectbox("縦軸を選択", data.names)
            with right:
                prefec = st.radio("グラフの色分け", ("総人口", "男性", "女性"))

            if prefec == "男性":
                filtered_data = data.df[data.df["属性"].isin(["male"])]
                fig = px.scatter(
                    filtered_data,
                    x=x_label,
                    y=y_label,
                )
            elif prefec == "女性":
                filtered_data = data.df[data.df["属性"].isin(["female"])]
                fig = px.scatter(
                    filtered_data,
                    x=x_label,
                    y=y_label,
                )
            else:
                filtered_data = data.df[data.df["属性"].isin(["all"])]
                fig = px.scatter(
                    filtered_data,
                    x=x_label,
                    y=y_label,
                )

            # グラフ描画
            st.plotly_chart(fig, use_container_width=True)

        else:
            left, right = st.columns(2)
            with left:  # 散布図の表示
                x_label = st.selectbox("横軸を選択", data.names)
            with right:
                y_label = st.selectbox("縦軸を選択", data.names)

            # グラフ描画
            fig = px.scatter(
                data.only_numeric,
                x=x_label,
                y=y_label,
            )

            # 相関係数算出
            cor = get_corrcoef(data.only_numeric, x_label, y_label)
            st.write("相関係数：" + str(cor))

            # グラフ描画
            add_row_to_gsheet(gsheet_connector, [[text1, text2]])
            st.plotly_chart(fig, use_container_width=True)

    # ヒストグラム
    elif graph == "ヒストグラム":
        hist_val = st.selectbox("変数を選択", data.names)
        fig = px.histogram(data.only_numeric, x=hist_val)
        st.plotly_chart(fig, use_container_width=True)

    # 箱ひげ図
    elif graph == "箱ひげ図":
        if d_name == "E: 基本生活":
            # 箱ひげ図はEのみ
            box_val_y = st.selectbox("箱ひげ図にする変数を選択", data.names)
            fig = px.box(data.df, y=box_val_y)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("このデータは箱ひげ図には対応していません")

    # 折れ線
    elif graph == "折れ線グラフ":
        if data.transition_filter:
            # 都道府県を選択
            prefecs = st.multiselect("グラフに表示する都道府県を選択", PREFECTURES)
            selected_df = pd.DataFrame()
            for pre in prefecs:
                selected_df = selected_df.append(data.df[data.df["都道府県"] == pre])

            # 縦軸を選択
            y_label = st.selectbox("縦軸を選択", data.names)

            # グラフを描画
            if len(selected_df) == 0:
                fig = px.line(data.df, x="年", y=y_label, color="都道府県")
            else:
                fig = px.line(selected_df, x="年", y=y_label, color="都道府県")

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("このデータは折れ線グラフに対応していません")


## メイン
main()
