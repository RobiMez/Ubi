#!/usr/bin/env python3
# (c) https://t.me/TelethonChat/37677
# This Source Code Form is subject to the terms of the GNU
# General Public License, v.3.0. If a copy of the GPL was not distributed with this
# file, You can obtain one at https://www.gnu.org/licenses/gpl-3.0.en.html.

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import os

print(""" APP_ID and API_HASH from :  my.telegram.org """)

APP_ID = int(os.getenv("APP_ID") or input("Enter APP ID here: "))
API_HASH = os.getenv("API_HASH") or input("Enter API HASH here: ")

with TelegramClient(StringSession(), APP_ID, API_HASH) as client:
    print(" -------------- StringSession ------------- ")
    print(client.session.save())
    print("-------------------------------------------")
