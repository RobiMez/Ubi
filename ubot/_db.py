import pymongo
import os
from datetime import datetime
from telethon import events
from pymongo import MongoClient

DB_URI = os.getenv("DB_URI")
cluster = MongoClient(DB_URI)


db = cluster['ubot']
collection = db['afk_stat']


@ubot.on(events.NewMessage(pattern=r"\.dbt", outgoing=True))  # pylint: disable=E0602
async def database_test(event):
    serverStatus = db.command("serverStatus")

    uptime_ms = int(serverStatus['uptimeMillis'])

    await event.edit(f"""

        --------------- DataBase Status ------------------
        Version : {serverStatus['version']}
        Uptime : {uptime_ms}
        Persistence : {serverStatus['storageEngine']['persistent']}
        Readonly  : {serverStatus['storageEngine']['readOnly']}
        ----------------- Network -----------------
        Network Requests : {serverStatus['network']['numRequests']}
        Network In : {serverStatus['network']['bytesIn']}
        Network Out : {serverStatus['network']['bytesOut']}
        ------------------ Connections -----------------
        Current: {serverStatus['connections']['current']}
        available: {serverStatus['connections']['available']}
        totalCreated: {serverStatus['connections']['totalCreated']}

""")


@ubot.on(events.NewMessage(pattern=r"\.dbp", outgoing=True))  # pylint: disable=E0602
async def database_ping(event):
    start = datetime.now()  # pylint: disable=E0602
    await event.edit("Bonking...")
    db.command("ping")
    end = datetime.now()  # pylint: disable=E0602
    ms = (end - start).microseconds / 1000
    await event.edit(f"DB Ping : {ms}")
