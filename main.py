import pandas as pd
import plotly.express as px
import streamlit as st

from data import PREFECTURES, Data, get_corrcoef


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
    graph = st.sidebar.radio("グラフの種類", ("散布図", "ヒストグラム", "箱ひげ図"))

    if graph == "散布図":

        if data.transition_filter:
            # 年推移のグラフ: 折れ線グラフで表示

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
        st.plotly_chart(fig, use_container_width=True)

    # ヒストグラム
    elif graph == "ヒストグラム":
        hist_val = st.selectbox("変数を選択", data.names)
        fig = px.histogram(data.only_numeric, x=hist_val)
        st.plotly_chart(fig, use_container_width=True)

    # 箱ひげ図
    elif graph == "箱ひげ図":
        box_val_y = st.selectbox("箱ひげ図にする変数を選択", data.names)

        left, right = st.columns(2)
        with left:  # 散布図の表示
            fig = px.box(
                data.only_numeric,
                x="学年",
                y=box_val_y,
            )
            st.plotly_chart(fig, use_container_width=True)
        with right:
            fig = px.box(data.only_numeric, x="性別", y=box_val_y)
            st.plotly_chart(fig, use_container_width=True)


## メイン
main()
