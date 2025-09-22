import numpy as np
import streamlit as st

# np.random.seed(1234)


def get_url(idx: str, name: str):
    url = f"https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/250922-robot-facial-mimicry-with-vlm-iter2/test_faces_results_iter2/face_{idx}/robot_frame_{name}.png"
    return url


def get_tgt_url(idx: str):
    url = f"https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/250922-robot-facial-mimicry-with-vlm-iter2/test_faces_results_iter2/face_{idx}/target_frame.png"
    return url


if "samples" not in st.session_state:
    idcs = ["001", "002", "003", "004", "005"] + [f"{x:03}" for x in range(7, 22)]
    samples = []
    for idx in idcs:
        for name in ["fim", "vlm"]:
            samples.append(
                {
                    "url_t": get_tgt_url(idx),
                    "url_a": get_url(idx, "fim_vlm"),
                    "url_b": get_url(idx, name),
                    "model_name": name,
                    "idx": idx,
                    "swap": np.random.rand() > 0.5,
                }
            )
    np.random.shuffle(samples)
    st.session_state["samples"] = samples
if "num_samples" not in st.session_state:
    st.session_state["num_samples"] = len(st.session_state["samples"])
if "sample_idx" not in st.session_state:
    st.session_state["sample_idx"] = 0


def choice_to_value(choice: str) -> int:
    value = 0
    match choice:
        case "A":
            value = 2
        case "ややA":
            value = 1
        case "ややB":
            value = -1
        case "B":
            value = -2
    return value


def on_form_submitted():
    # Record choice
    pair = st.session_state["samples"][st.session_state["sample_idx"]]
    similarity_value = choice_to_value(
        st.session_state[f'similarity_choice_{st.session_state["sample_idx"]}']
    )
    naturalness_value = choice_to_value(
        st.session_state[f'naturalness_choice_{st.session_state["sample_idx"]}']
    )

    if pair["swap"]:
        similarity_value = -similarity_value
        naturalness_value = -naturalness_value

    st.session_state["samples"][st.session_state["sample_idx"]][
        "similarity"
    ] = similarity_value
    st.session_state["samples"][st.session_state["sample_idx"]][
        "naturalness"
    ] = naturalness_value

    # Move to next pair
    st.session_state["sample_idx"] += 1


# Interface
st.title("実験")
st.warning(
    "ページを更新したりタブを閉じたりしないでください。入力済みのデータが失われます。"
)
progress_bar_text = "進捗"
progress_bar = st.progress(
    0, text=f"{progress_bar_text}: {0}/{st.session_state['num_samples']}"
)


@st.fragment
def exp_fragment():
    # Check if all completed
    if st.session_state["sample_idx"] == st.session_state["num_samples"]:
        st.session_state["log"] = {"com": st.session_state["samples"]}

        # Move to next
        st.switch_page("pages/comment.py")

    # Get sample info
    sample = st.session_state["samples"][st.session_state["sample_idx"]]
    url_t = sample["url_t"]
    url_a = sample["url_a"]
    url_b = sample["url_b"]
    if sample["swap"]:
        url_a, url_b = url_b, url_a

    # Place interface
    with st.container(border=True):
        st.subheader("類似度・自然さ")
        st.text(f"表情を見て、質問にお答えください。")
        col1, col2, col3 = st.columns([1, 1, 1], border=True)
        with col1:
            st.subheader("A", divider="gray")
            st.image(url_a)
        with col2:
            st.subheader("目標", divider="gray")
            st.image(url_t)
        with col3:
            st.subheader("B", divider="gray")
            st.image(url_b)
        # st.write(sample["idx"])

        similarity_choice = st.radio(
            "Q1: 表情の**類似度**について、どちらの方が目標表情と似ていますか？",
            options=[
                "A",
                "ややA",
                "どちらとも言えない",
                "ややB",
                "B",
            ],
            index=None,
            key=f'similarity_choice_{st.session_state["sample_idx"]}',
            horizontal=True,
        )
        naturalness_choice = st.radio(
            "Q2: 表情の**自然さ**について，どちらの方が自然な表情だと思いますか?",
            options=[
                "A",
                "ややA",
                "どちらとも言えない",
                "ややB",
                "B",
            ],
            index=None,
            key=f'naturalness_choice_{st.session_state["sample_idx"]}',
            horizontal=True,
        )
        choice_has_not_been_made = (
            similarity_choice == None or naturalness_choice == None
        )
        st.button(
            "次へ",
            on_click=on_form_submitted,
            disabled=choice_has_not_been_made,
            help="質問にお答えください。" if choice_has_not_been_made else "",
        )

    progress_bar.progress(
        st.session_state["sample_idx"] / st.session_state["num_samples"],
        f"{progress_bar_text}: {st.session_state['sample_idx']}/{st.session_state['num_samples']}",
    )


exp_fragment()
