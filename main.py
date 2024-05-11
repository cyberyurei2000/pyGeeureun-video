# Copyright (c) cyberyurei2000 2024
# Released under the BSD 3-Clause License
# https://opensource.org/license/bsd-3-clause

from typing import Any
from pathlib import Path
import os
import yaml


def anime_full(data: dict[Any, Any]) -> None:
    """This function is for anime videos with subtitles and fonts already included."""
    os.chdir(data["dir"])
    files = sorted(os.listdir(os.getcwd()))
    counter = 0

    for file in files:
        title = f"{data['maintitle']} - {data[counter + 1]['title']}"
        final_filename = f"{data['maintitle']} - {data[counter + 1]['code']} - {data[counter + 1]['title']}"

        if not os.path.isdir(file):
            cmd = f"ffmpeg -i \"{file}\" " \
                  f"-metadata title=\"{title}\" " \
                  "-map 0:v -map 0:a:0 -map 0:s:0 -map 0:t -c copy " \
                  f"\"./final/{final_filename}.mkv\""
            os.system(cmd)
            counter += 1


def anime_raw(data: dict[Any, Any]) -> None:
    """This function is for anime raw files which needs to embend subtitles."""
    os.chdir(data["dir"])
    files = sorted(os.listdir(os.getcwd()))
    counter = 0

    for file in files:
        title = f"{data['maintitle']} - {data[counter + 1]['title']}"
        final_filename = f"{data['maintitle']} - {data[counter + 1]['code']} - {data[counter + 1]['title']}"

        if ".mp4" in str(file):
            sub_file = str(file).replace(".mp4", ".eng.ass")
        elif ".mkv" in str(file):
            sub_file = str(file).replace(".mkv", ".eng.ass")
        elif ".ts" in str(file):
            sub_file = str(file).replace(".ts", ".eng.ass")
        subtitle_file = f"./subtitles/{sub_file}"

        if not os.path.isdir(file):
            cmd = f"ffmpeg -i \"{file}\" " \
                  f"-i \"{subtitle_file}\" " \
                  f"-metadata title=\"{title}\" " \
                  "-map 0:v -map 0:a " \
                  "-map 1 -metadata:s:s:0 language=\"eng\" -metadata:s:a:0 language=\"jpn\" " \
                  "-c copy " \
                  f"\"./final/{final_filename}.mkv\""
            os.system(cmd)
            counter += 1


def globo_squished_fix(data: dict[Any, Any]) -> None:
    """Fix aspect ratio of content that was originally released in 4:3 but was poorly modified to 16:9."""
    os.chdir(data["dir"])
    files = sorted(os.listdir(os.getcwd()))
    counter = 0

    for file in files:
        strfile = str(Path(file).stem)
        lenght = len(strfile)
        if strfile.endswith("A"):
            string = strfile[lenght - 4:]
            while "0" in string[0]:
                s = list(string)
                s.pop(0)
                string = "".join(s)
            chapter = string
        else:
            string = strfile[lenght - 3:]
            while "0" in string[0]:
                s = list(string)
                s.pop(0)
                string = "".join(s)
            chapter = string

        title = f"{data['maintitle']} - Capítulo {chapter}"
        final_filename = Path(file).stem

        # ffmpeg -i video.ts -vf setsar=1,setdar=4/3 -aspect 4:3 -c:a copy video-fixed.mkv
        if not os.path.isdir(file):
            cmd = f"ffmpeg -i \"{file}\" " \
                  f"-metadata title=\"{title}\" " \
                  "-vf setsar=1,setdar=4/3 -aspect 4:3 " \
                  "-c:a copy " \
                  f"\"./final/{final_filename}.mkv\""
            os.system(cmd)
            counter += 1


with open("./data.yml", "r") as stream:
    try:
        DATA = yaml.safe_load(stream)
        TYPE = DATA["type"]
        match TYPE:
            case "anime-full":
                anime_full(DATA)
            case "anime-raw":
                anime_raw(DATA)
            case "globo-squished":
                globo_squished_fix(DATA)
    except yaml.YAMLError as err:
        print(err)
