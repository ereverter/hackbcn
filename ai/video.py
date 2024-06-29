import argparse
import os

import moviepy.editor as mp


def extract_audio(video_path, audio_path):
    video = mp.VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract audio from a video file.")
    parser.add_argument("-v", "--video_file", type=str, help="Path to the video file")
    parser.add_argument(
        "-a", "--audio_file", type=str, help="Path to save the extracted audio file"
    )
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.audio_file), exist_ok=True)

    extract_audio(args.video_file, args.audio_file)
