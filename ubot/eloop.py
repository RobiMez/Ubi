"""code that must be executed on every single update from telegram will go here
and ill make this file a core file cus .... feels like this isnt just your average plugin

ie :

shit like checking if afk
checking if a person of interest does sth
looking if the bot is going on a rampage

"""
import os
import logging
import asyncio
from telethon import events, errors
from datetime import datetime

import pymongo
from pymongo import MongoClient
DB_URI = os.getenv("DB_URI")

cluster = MongoClient(DB_URI)

db = cluster['ubot']
collection = db.afk_stat
kill_cooldown = 1


@ubot.on(events.NewMessage(pattern="\.afk (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Processing...")
    str = event.pattern_match.group(1)
    print(f' afk reason : {str}')
    # set afk to true
    db.afk_stat.update_one({"name": "afkobj", }, {
        "$set": {'afk': True, "name": "afkobj", 'reason': str}}, upsert=True)

    msg = await event.edit("Yay .....")

    await asyncio.sleep(kill_cooldown)
    await msg.delete()

    # print(f"user is afk now ")


@ubot.on(events.NewMessage(outgoing=True))
async def outgoing_handler(event):
    # print("\n 🧪  Outgoing tripped :\n")
    # check afk status and deafk
    start = datetime.now()
    if collection.find_one({"name": "afkobj", })['afk']:
        end = datetime.now()
        ms = (end - start).microseconds / 1000
        # print(f"user is afk < check took {ms} ms")
        db.afk_stat.update_one({"name": "afkobj", }, {
            "$set": {'afk': False, "name": "afkobj", "reason": ""}}, upsert=True)
        # print("user is no longer afk ")

    # else:
        # print("user is active")
    message = event.message.message
    fwd_from = event.message.fwd_from
    mtype = None
    is_scheduled = event.message.from_scheduled
    to = event.message.to_id

    try:

        to_id = to.chat_id
    except AttributeError as e:
        # print(e)
        # print("Probably cus they using a normal group instead of a super group ... implementing workaround ")
        to_id = to.channel_id

    # print(f'mtype : {mtype}')
    # print(f'fwd_from : {fwd_from}')
    # print(f'message : {message}')
    # print(f'is_scheduled : {is_scheduled}')
    # print(f'In chat : {to_id}')
    # DEBUG HERE
    # print(f"\n{event}\n")


@ubot.on(events.NewMessage(incoming=True))
async def incoming_handler(event):
    # print("\n ⬇️  Incoming tripped\n")
    mentioned = event.message.mentioned
    start = datetime.now()
    if collection.find_one({"name": "afkobj", })['afk']:

        end = datetime.now()
        ms = (end - start).microseconds / 1000
        # print(f"user is afk < check took {ms} ms")
        rsn = collection.find_one({"name": "afkobj", })['reason']
        if mentioned:
            # print("user mentioned me ")
            await event.respond(f"""
Im AFK( offline ) right now
**Reason** : 
__{rsn}__

    """)

    # else:
        # print("user is active")
    message = event.message.message
    # print(f"\n{event}\n")

    from_id = event.message.from_id
    to = event.message.to_id
    try:
        to_id = to.channel_id
    except AttributeError as e:
        # print(e)
        # print("Probably cus they using a normal group instead of a super group ... implementing workaround ")
        to_id = to.chat_id

    # print(f'message : {message}')
    # print(f'mentioned : {mentioned}')
    # print(f'from_id : {from_id}')
    # print(f'In chat : {to_id}')


# @ubot.on(events.MessageEdited())
# async def incoming_handler(event):
#     print("edited tripped")


# @ubot.on(events.MessageRead())
# async def incoming_handler(event):
#     print("read tripped")


# @ubot.on(events.MessageDeleted())
# async def incoming_handler(event):
#     print("deleted tripped")

# @ubot.on(events.UserUpdate())
# async def incoming_handler(event):
#     print("user status tripped")
