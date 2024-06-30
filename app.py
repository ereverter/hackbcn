import json

import pandas as pd
import requests
import streamlit as st

# URL of your FastAPI endpoint
API_URL = "http://localhost:8001/process_video"


def upload_files(video_file, text_file):
    files = {
        "video_file": video_file,
        "text_file": text_file,
    }
    response = requests.post(API_URL, files=files)
    return response.json()


import matplotlib.pyplot as plt


def plot_emotions_over_time(grouped_transcription):
    time_stamps = [item[0] for item in grouped_transcription]
    emotions = [item[2] for item in grouped_transcription]

    df_emotions = pd.DataFrame(emotions, index=time_stamps)

    st.subheader("Emotions Over Time")
    fig, ax = plt.subplots(figsize=(10, 6))
    df_emotions.plot(ax=ax)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Emotion Scores")
    ax.set_title("Evolution of Emotions Over Time")
    st.pyplot(fig)


def main():
    st.title("Video and Text Analysis Interface")

    st.write("Upload a video file and a text file for analysis.")

    video_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])
    text_file = st.file_uploader("Upload a text file", type=["txt"])

    if st.button("Analyze") and video_file and text_file:
        with st.spinner("Processing..."):
            result = upload_files(video_file, text_file)

        st.subheader("Original Text")
        st.text_area("", result.get("original_text", ""), height=300)

        st.subheader("Transcript")
        st.text_area("", result.get("transcription", ""), height=300)

        st.subheader("Emotions Summary")
        emotions_summary = result.get("emotions_summary", {})
        if emotions_summary:
            df = pd.DataFrame(
                list(emotions_summary.items()), columns=["Emotion", "Score"]
            )
            st.bar_chart(df.set_index("Emotion"))

        grouped_transcription = result.get("grouped_transcription", [])
        if grouped_transcription:
            plot_emotions_over_time(grouped_transcription)

        st.subheader("Evaluation")
        evaluation = result.get("evaluation", "{}")
        evaluation_dict = json.loads(evaluation)
        if evaluation_dict:
            st.write("### Errors")
            st.write(
                "\n".join(f"- {error}" for error in evaluation_dict.get("errors", []))
            )
            st.write("### Recommendations")
            st.write(
                "\n".join(
                    f"- {rec}" for rec in evaluation_dict.get("recommendations", [])
                )
            )


if __name__ == "__main__":
    main()
