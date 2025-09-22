import datetime

import pytz
import streamlit as st
from google.cloud import firestore

st.title("終わり")

with st.status(
    "ただいまデータをアップロード中です。タブを閉じないでください。"
) as status:
    # Connect to database
    st.write("Connect to database")
    db = firestore.Client.from_service_account_info(st.secrets["firestore"])

    # Create document data for Firestore
    doc_data = {
        "userid": st.session_state.get("userid", ""),
        "gender": st.session_state.get("gender", ""),
        "age": st.session_state.get("age", ""),
        "comment": st.session_state["comment"],  # Record comment
        "start_time": st.session_state.get("start_time"),
        "finishing_time": datetime.datetime.now(pytz.timezone("Asia/Tokyo")).strftime(
            "%Y-%m-%d_%H-%M-%S"
        ),  # Record finishing time
        "log": st.session_state["log"],
    }

    # Write to Firestore collection
    st.write("Write data")
    db.collection("250922-robot-facial-mimicry-test-faces").add(doc_data)
    status.update(label="ご回答は正常に記録されました。", state="complete")

st.text(
    "ご協力ありがとうございました。\n\n"
    "これで終了です。タブを閉じていただいて構いません。"
)

st.header("Crowd Works ユーザーへ")
st.caption("Crowd Works以外のユーザーは無視してください。")
st.text(
    "Crowd Worksの画面上で、合言葉を入れる欄に次のひらがな4文字を入力してください。\n\n"
    "「ろぼっと」"
)
