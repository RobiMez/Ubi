# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Urban Dictionary
Syntax: .ud Query"""
from telethon import events, errors
import urbandict
import asyncio
kill_cooldown = 130


@ubot.on(events.NewMessage(pattern="\.ud (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Processing...")
    str = event.pattern_match.group(1)
    try:
        res = urbandict.define(str)
        if len(res) > 0:
            await event.edit(f"""
───────────────────
**{str.capitalize()}** :

__{res[0]['def']}__

───────────────────
** Example **:
{res[0]['example']}
───────────────────
    """)
        else:
            await event.edit("No result found for **" + str + "**")
    except:
        await event.edit("No result found for **" + str + "**")


@ubot.on(events.NewMessage(pattern="\.udd (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Processing...")
    str = event.pattern_match.group(1)
    try:
        res = urbandict.define(str)
        defn_str = ""

        # loop thru the defnitions and add them to the string

        for resu in res:
            defn_str = defn_str + "**Definition : **" + "\n"
            defn_str = defn_str + resu['def'] + "\n\n"
            defn_str = defn_str + "**Example : **" + "\n"
            defn_str = defn_str + resu['example'] + "\n\n"
            defn_str = defn_str + "───────────────────" + "\n"

        if len(res) > 0:
            await event.edit(f"""
───────────────────
**{str.capitalize()}** `{len(res)}` Matches
───────────────────
{defn_str}
        """)
        else:
            await event.edit("No result found for **" + str + "**")
    except errors.MessageTooLongError as e:

        await event.edit(f"**[* Internal panic noises *]** \n __Command [ .udd {str} ]__ \n `{e}`")


@ubot.on(events.NewMessage(pattern="\.ud (.*)", incoming=True))
async def _(event):
    if event.fwd_from:
        return
    mentioned = event.message.mentioned
    if mentioned:
        str = event.pattern_match.group(1)
        try:
            res = urbandict.define(str)
            if len(res) > 0:
                msg = await event.respond(f"""
    ───────────────────
    **{str.capitalize()}** :

    __{res[0]['def']}__

    ───────────────────
    ** Example **:
    {res[0]['example']}
    ───────────────────
        """)
                await asyncio.sleep(kill_cooldown)
                await msg.delete()

            else:
                await event.respond("No result found for **" + str + "**")
        except:
            await event.respond("No result found for **" + str + "**")


@ubot.on(events.NewMessage(pattern="\.udd (.*)", incoming=True))
async def _(event):
    if event.fwd_from:
        return
    mentioned = event.message.mentioned
    if mentioned:
        str = event.pattern_match.group(1)
        try:
            res = urbandict.define(str)
            defn_str = ""

        # loop thru the defnitions and add them to the string

            for resu in res:
                defn_str = defn_str + "**Definition : **" + "\n"
                defn_str = defn_str + resu['def'] + "\n\n"
                defn_str = defn_str + "**Example : **" + "\n"
                defn_str = defn_str + resu['example'] + "\n\n"
                defn_str = defn_str + "───────────────────" + "\n"

            if len(res) > 0:
                msg = await event.respond(f"""
─────────────────── 
**{str.capitalize()}** `{len(res)}` Matches 
───────────────────
{defn_str}
        """)
                await asyncio.sleep(kill_cooldown)
                await msg.delete()
            else:
                await event.respond("No result found for **" + str + "**")
        except errors.MessageTooLongError as e:

            await event.respond(f"**[* Internal panic noises *]** \n __Command [ .udd {str} ]__ \n `{e}`")
