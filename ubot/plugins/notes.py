''' notes to self '''
import os
import asyncio
from telethon import events
from datetime import datetime

import pymongo
from pymongo import MongoClient

DB_URI = os.getenv("DB_URI")
cluster = MongoClient(DB_URI)

db = cluster['ubot']
collection = db.notes
kill_cooldown = 5


@ubot.on(events.NewMessage(pattern="\.nts (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    # get all the notes and the length
    await event.edit("Adding note ...")
    str = event.pattern_match.group(1)
    print("ubi is reading your notes ")
    notes = db.notes.find()
    leng = 0

    for note in notes:
        leng = leng + 1
    # print(leng)
    index = leng + 1
    print(f"ubi reads {leng} notes ")
    db.notes.insert_one({"note": str, "index": index})
    print(f"ubi saved your new note ")
    msg = await event.edit("ubi saved your new note")

    await asyncio.sleep(kill_cooldown)
    await msg.delete()

# delete note by number


@ubot.on(events.NewMessage(pattern="\.dnts (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    # get the num to be deleted
    try:
        index = int(event.pattern_match.group(1))
    except ValueError as e:
        await event.edit(f"This isnt a number dummy ")
        print(f"{e}")
    await event.edit(f"ubi is deleting note number {index}")
    print(f"ubi is deleting note number {index}")
    # gets the total number of notes
    print("ubi is reading your notes ")
    notes = db.notes.find()
    leng = 0

    for note in notes:
        leng = leng + 1
    # print(leng)
    # checks if the num is valid
    if index <= leng:

        # delete the note
        db.notes.delete_one({"index": index})

        msg = await event.edit("deleted note ...")
        await asyncio.sleep(kill_cooldown)
        await msg.delete()
    else:
        msg = await event.edit("This isnt a note ... check your numbers again ")
        await asyncio.sleep(kill_cooldown)
        await msg.delete()


@ubot.on(events.NewMessage(pattern="\.notes", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    notes_str = ""

    notes = db.notes.find()
    leng = 0

    for note in notes:
        notes_str = notes_str + \
            str(note["index"]) + " : " + note["note"] + " \n"

        leng = leng + 1
    # print(notes_str)
    print(f"ubi reads {leng} notes ")
    msg = await event.edit(f"NOTES : \n{notes_str}")
