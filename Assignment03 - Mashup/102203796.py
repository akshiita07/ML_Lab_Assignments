﻿import sys
import os
from pytube import YouTube
from youtubesearchpython import VideosSearch
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import yt_dlp as youtube_dl

# Function to search and download videos
def search_and_download_videos(query, max_results=5):
    videos_search = VideosSearch(query, limit=max_results)
    results = videos_search.result()['result']
    
    video_urls = [result['link'] for result in results]
    video_files = []

    for url in video_urls:
        try:
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': '%(title)s.%(ext)s',  # Saves video with title as filename
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                video_file = ydl.prepare_filename(info_dict)
                video_files.append(video_file)
                print(f"Downloaded: {info_dict['title']}")
        except Exception as e:
            print(f"Failed to download {url}. Error: {e}")

    return video_files

# Function to convert downloaded videos to MP3
def convert_to_mp3(video_files):
    audio_files = []
    for video_file in video_files:
        try:
            audio_file = os.path.splitext(video_file)[0] + ".mp3"
            video_clip = VideoFileClip(video_file)
            video_clip.audio.write_audiofile(audio_file)
            audio_files.append(audio_file)
            print(f"Converted to MP3: {audio_file}")
        except Exception as e:
            print(f"Failed to convert {video_file}. Error: {e}")

    return audio_files

# Function to trim and merge MP3s
def trim_and_merge_audios(audio_files, duration=30):
    combined = AudioSegment.silent(duration=0)  # Start with an empty audio segment

    for audio_file in audio_files:
        try:
            audio = AudioSegment.from_file(audio_file)
            trimmed_audio = audio[:duration * 1000]  # Take the first 'duration' seconds
            combined += trimmed_audio
            print(f"Trimmed and added: {audio_file}")
        except Exception as e:
            print(f"Failed to process {audio_file}. Error: {e}")

    output_file = "combined_output.mp3"
    combined.export(output_file, format="mp3")
    print(f"Combined audio saved as: {output_file}")
    return output_file

# Main function to handle command-line arguments and process the mashup
def main():
    # Check if the correct number of arguments are provided
    if len(sys.argv) != 5:
        print("Usage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        return
    
    # Extract command-line arguments
    singer_name = sys.argv[1]
    number_of_videos = int(sys.argv[2])
    audio_duration = int(sys.argv[3])
    output_file_name = sys.argv[4]

    # Step 1: Search and download videos
    print(f"Searching and downloading {number_of_videos} videos of {singer_name}...")
    video_files = search_and_download_videos(singer_name, max_results=number_of_videos)
    
    # Step 2: Convert videos to MP3
    print("Converting downloaded videos to MP3...")
    audio_files = convert_to_mp3(video_files)
    
    # Step 3: Trim and merge MP3s
    print(f"Trimming audios to {audio_duration} seconds and merging them...")
    output_file = trim_and_merge_audios(audio_files, duration=audio_duration)
    
    # Step 4: Rename output file
    if os.path.exists(output_file):
        os.rename(output_file, output_file_name)
        print(f"Output file renamed to: {output_file_name}")
    else:
        print("Failed to create the output file.")

# Run the main function
if __name__ == "__main__":
    main()

#for run:python <RollNumber>.py "Sharry Maan" 20 30 output.mp3
