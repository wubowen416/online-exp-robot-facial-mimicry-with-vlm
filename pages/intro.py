import streamlit as st

st.title("実験内容")

with st.container(border=True):
    st.header("実験説明")
    st.markdown(
        """
        本実験では、ロボットが人の表情を模倣しています。
        人の表情とロボットの表情を2個見て、以下の2点について印象評価をしていただきます。
        - **類似度**：ロボットの2個の表情は、どちらの方が人の表情と似ているか？顔の形態ではなく、表情についてご比較ください。
        - **自然さ**：ロボットの2個の表情は、どちらの方がロボットにとって自然な表情であるか？
        
        各質問にはラジオボタン式の選択肢があります。もっとも当てはまるものを選択してください。

        合計5セットを評価していただきます。所要時間は10分程度です。

        画面が大きすぎる、または小さすぎる場合は、ブラウザのズーム機能（Ctrl/CMD＋「+」「-」キー）で調整が可能です。
        """
    )

    st.header("実験ページの例")
    st.markdown(
        """
        実験のページは以下のように表示されます。
        """
    )

    with st.container(border=True):
        st.subheader("類似度・自然さ")
        st.text(f"表情を見て、質問にお答えください。")
        col1, col2, col3 = st.columns([1, 1, 1], border=True)
        with col1:
            st.subheader("A", divider="gray")
            st.image(
                "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/250921-robot-facial-mimicry-with-vlm-pre-exp/face_001/robot_frame_fim.png"
            )
        with col2:
            st.subheader("目標", divider="gray")
            st.image(
                "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/250921-robot-facial-mimicry-with-vlm-pre-exp/face_001/target_frame.png"
            )
        with col3:
            st.subheader("B", divider="gray")
            st.image(
                "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/250921-robot-facial-mimicry-with-vlm-pre-exp/face_001/robot_frame_fim.png"
            )
        st.radio(
            "Q1: 表情の**類似度**について、どちらの方が目標表情と似ていますか？",
            options=[
                "A",
                "ややA",
                "どちらとも言えない",
                "ややB",
                "B",
            ],
            index=None,
            horizontal=True,
        )
        st.radio(
            "Q2: 表情の**自然さ**について，どちらの方が自然な表情だと思いますか?",
            options=[
                "A",
                "ややA",
                "どちらとも言えない",
                "ややB",
                "B",
            ],
            index=None,
            horizontal=True,
        )

    st.warning(
        "回答の仕方が明らかに不誠実と判断される場合は、報酬をお支払いできないことがあります。問題文をよく読み、ご理解いただいた上でご回答ください。"
    )

next_button = st.button(label="実験へ")
if next_button:
    st.switch_page("pages/exp.py")
