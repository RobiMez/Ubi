''' Deal with sauce and hentai 
commands : 
.dhen sauce > downloads the hentai to local drive
.hen sauce > recons to make sure it isnt ...... cursed 
'''
import os
import asyncio
import time
import requests
import urllib
import urllib.request
from tqdm import tqdm
from datetime import datetime
from telethon import events, errors
from hentai import Hentai, Format, Page
from requests.exceptions import HTTPError
from pathlib import Path


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(
            url, filename=output_path, reporthook=t.update_to)


def progressBar(iterable, prefix='█ Progress:', suffix='Complete ', decimals=1, length=100, fill='█', unfill='–', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        unfill      - Optional  : bar not filled character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """

    total = len(iterable)
    # Progress Bar Printing Function

    def printProgressBar(iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                         (iteration / float(total)))
        filledLength = int(length * iteration // total)

        bar = fill * filledLength + unfill * (length - filledLength)
        # bar printing is here
        print(f'\r{prefix} │{bar}│ {percent}% {suffix}', end=printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()


@ubot.on(events.NewMessage(pattern="\.dhen (.*)", outgoing=True))  # pylint: disable=E0602
async def _(event):
    if event.fwd_from:
        return
    await event.edit("__Command__ : `.dhen {str}`")
    str = event.pattern_match.group(1)
    print(f'Command : .dhen {str}')
    try:
        pass
    except ValueError as e:
        await event.edit(f" {str} is not a number")
        print(e)
        return

    doujin = Hentai(int(str))
    if Hentai.exists(doujin.id):

        urls = doujin.image_urls
        total_pages = len(urls)
        await event.edit("__Download starting ... __")
        bar = 'loading...'

        length = 10
        fill = '█'
        unfill = '─'
        folder_title = str

        for count, page in enumerate(urls, start=1):

            iteration = count
            filledLength = int(length * iteration // total_pages)
            bar = fill * filledLength + unfill * (length - filledLength)
            # do sth here
            folder_path = Path(f'Dhentai/{folder_title}')
            path = Path(f'Dhentai/{folder_title}/{iteration}.jpg')

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            download_url(page, path)
            try:
                await event.edit(f"""
    __Downloading #{str}__
        {bar} {count} / {total_pages} pages

    nhentai.net/g/{str}
    """)

            except errors.MessageNotModifiedError as e:
                pass

        await event.edit(f"""
    **Downloaded  #{str}**
        {bar} {count} / {total_pages} pages

        nhentai.net/g/{str}
    """)


@ubot.on(events.NewMessage(pattern="\.hen (.*)", outgoing=True))  # pylint: disable=E0602
async def _(event):
    if event.fwd_from:
        return
    str = event.pattern_match.group(1)
    await event.edit(f"__Command__ `.hentai {str}`")
    print(f"Command : .hentai {str}")
    try:
        int(str)
    except ValueError as e:
        await event.edit(f" {str} is not a number")
        print(e)
        return

    try:
        doujin = Hentai(int(str))
        if Hentai.exists(doujin.id):
            await event.edit(f"""
__Command__ `.hentai {str}`
....... Hentai Exists .......
""")
            await event.edit(f"""
__Command__ `.hentai {str}`

**Hentai** : {doujin.title(Format.Pretty)}

**Hentai #** : `{str}`
**Pages** : {doujin.num_pages} 
**favorites** : {doujin.num_favorites}
**Upload date : ** {doujin.upload_date}

**language** : {[ " __" + tag.name + "__ " for tag in doujin.language]} 
**Tags** : {[ " __" + tag.name + "__ " for tag in doujin.tag]} 
**Artist** : {[" __" + tag.name + "__ " for tag in doujin.artist]}
**Category** : {[ " __" + tag.name + "__ " for tag in doujin.category]}

**Link** : `nhentai.net/g/{str}`

""")

    except HTTPError as e:
        await event.edit(f"#{str} is not a Hentai, double check the numbers or try another.")
        print(e)
