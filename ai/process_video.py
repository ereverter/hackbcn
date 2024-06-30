import argparse
import os

import moviepy.editor as mp


def extract_audio(video_path, audio_path):
    video = mp.VideoFileClip(video_path)
    print(video.duration)
    audio = video.subclip(0, video.duration).audio
    audio.write_audiofile(audio_path)
