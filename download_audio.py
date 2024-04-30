#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

import questionary
from rich.console import Console
from rich.panel import Panel
from youtubesearchpython import CustomSearch, VideoSortOrder


def main():
    if len(sys.argv) < 2:
        print("please enter the name of the song")
        return
    search_item = sys.argv[1]
    download_audio(search_item)


def download_audio(search_item):
    console = Console()
    custom_play_search = CustomSearch(
        search_item, VideoSortOrder.relevance, limit=3
    )
    custom_play_search_content = custom_play_search.result()
    console.print(Panel(
        f'Details for [yellow]{search_item.capitalize()}[/]\'s video'), justify="center"
    )
    options = [video['title']
               for video in custom_play_search_content["result"]]
    option = questionary.select(
        "please choose an option",
        choices=options).ask()
    selected_index = options.index(option)
    desc = "".join(item['text'] for item in custom_play_search_content["result"]
                   [selected_index]["descriptionSnippet"])
    console.print(Panel(f' \
                        [green bold]Most Relevant Video: [/]{custom_play_search_content["result"][selected_index]["title"]}\n \
                        [green bold]URL: [/]{custom_play_search_content["result"][selected_index]["link"]}\n \
                        [green bold]Channel: [/]{custom_play_search_content["result"][selected_index]["channel"]["name"]}\n \
                        [green bold]Duration: [/]{custom_play_search_content["result"][selected_index]["duration"]}\n \
                        [green bold]Views: [/]{custom_play_search_content["result"][selected_index]["viewCount"]["short"]}\n \
                        [green bold]Desc: [/]{desc}\n'
                        ))

    url = custom_play_search_content["result"][selected_index]["link"]
    cmd = "yt-dlp -x --audio-format mp3 " + url
    # print(cmd)
    os.system(cmd)


if __name__ == "__main__":
    main()
