import json

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

from ai.config import NEGATIVE_EMOTIONS, POSITIVE_EMOTIONS

# URL of your FastAPI endpoint
API_URL = "http://localhost:8001/process_video"


def upload_files(video_file, text_file):
    files = {
        "video_file": video_file,
        "text_file": text_file,
    }
    response = requests.post(API_URL, files=files)
    return response.json()


def plot_emotions_summary(emotions_summary):
    if emotions_summary:
        df = pd.DataFrame(emotions_summary.items(), columns=["Emotion", "Score"])
        df.set_index("Emotion", inplace=True)

        # Ensure the order of emotions
        ordered_emotions = [
            emotion.capitalize()
            for emotion in POSITIVE_EMOTIONS + NEGATIVE_EMOTIONS
            if emotion.capitalize() in df.index
        ]
        df = df.loc[ordered_emotions]

        # Set colors
        colors = [
            "green" if emotion.lower() in POSITIVE_EMOTIONS else "red"
            for emotion in df.index
        ]
        df["Color"] = colors

        fig = px.bar(
            df,
            x=df.index,
            y="Score",
            color="Color",
            color_discrete_map="identity",
            title="Emotions Summary",
            labels={"x": "Emotion", "y": "Score"},
        )
        st.plotly_chart(fig)


def plot_emotions_over_time(grouped_transcription):
    time_stamps = [item[0] for item in grouped_transcription]
    emotions = [item[2] for item in grouped_transcription]

    df_emotions = pd.DataFrame(emotions, index=time_stamps)

    fig = px.line(
        df_emotions,
        title="Evolution of Emotions Over Time",
        labels={"index": "Time (s)", "value": "Emotion Score", "variable": "Emotion"},
    )
    st.plotly_chart(fig)


def main():
    st.title("Presentation Feedback Interface")

    st.write("Upload a video file and a text file for analysis.")

    col1, col2 = st.columns(2)
    with col1:
        video_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])
    with col2:
        text_file = st.file_uploader("Upload a text file", type=["txt"])

    if st.button("Analyze") and video_file and text_file:
        with st.spinner("Processing..."):
            result = upload_files(video_file, text_file)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original Text")
            st.text_area("", result.get("original_text", ""), height=300, key="ot")
        with col2:
            st.subheader("Transcript")
            st.text_area("", result.get("transcription", ""), height=300, key="tt")

        st.subheader("Conveyed emotions")
        emotions_summary = result.get("emotions_summary", {})
        if emotions_summary:
            plot_emotions_summary(emotions_summary)

        grouped_transcription = result.get("grouped_transcription", [])
        if grouped_transcription:
            plot_emotions_over_time(grouped_transcription)

        st.subheader("Feedback")
        evaluation = result.get("evaluation", "{}")
        evaluation_dict = json.loads(evaluation)
        if evaluation_dict:
            st.write("### Mistakes")
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
