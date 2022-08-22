import plotly.express as px
import streamlit as st

from data import Data, get_corrcoef


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
        left, right = st.columns(2)

        with left:  # 散布図の表示
            x_label = st.selectbox("横軸を選択", data.names)
        with right:
            y_label = st.selectbox("縦軸を選択", data.names)

        # with right:  # 色分けオプション
        #     coloring = st.radio("グラフの色分け", ("なし", "学年", "性別"))

        # if coloring == "学年":
        #     fig = px.scatter(data.only_numeric, x=x_label, y=y_label, color="学年")
        # elif coloring == "性別":
        #     fig = px.scatter(
        #         data.only_numeric,
        #         x=x_label,
        #         y=y_label,
        #         color="性別",
        #     )
        # else:
        # fig = px.scatter(
        #     data.only_numeric,
        #     x=x_label,
        #     y=y_label,
        # )

        # 相関係数算出
        cor = get_corrcoef(data.only_numeric, x_label, y_label)
        st.write("相関係数：" + str(cor))

        # グラフ描画
        fig = px.scatter(
            data.only_numeric,
            x=x_label,
            y=y_label,
        )
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
