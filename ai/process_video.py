import argparse
import os

import moviepy.editor as mp


def extract_audio(video_path: str, audio_path: str) -> None:
    video = mp.VideoFileClip(video_path)
    audio = video.subclip(0, video.duration).audio
    audio.write_audiofile(audio_path)


def extract_frames(video_path: str, output_folder: str, frame_interval: int) -> None:
    video = mp.VideoFileClip(video_path)
    os.makedirs(output_folder, exist_ok=True)

    frame_count = int(video.fps * video.duration)
    for i in range(0, frame_count, frame_interval):
        frame = video.get_frame(i / video.fps)
        frame_path = os.path.join(output_folder, f"frame_{i}.png")
        mp.ImageClip(frame).save_frame(frame_path)
