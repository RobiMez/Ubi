# from telethon import events
# import pprint
# from telethon.utils import pack_bot_file_id
# from telethon.tl.types import PeerUser, PeerChat, PeerChannel


# @ubot.on(events.UserUpdate())  # pylint: disable=E0602
# async def _(event):

#     if event.typing:
#         try:
#             userid = event.user_id
#             chatid = event.chat_id
#             useres = await ubot.get_entity(userid)
#             groupres = await ubot.get_entity(chatid)

#             print(
#                 f" User:{useres.first_name} @{useres.username} is typing in chat : {groupres.title}")
#         except ValueError:

#             print(
#                 f" Entity: {event.user_id} is typing in chat : {event.chat_id}")
#             pass

# elif event.online:
#     print(f" User: {event.user_id} is online ")
# elif event.status:
#     print(f" User :{event.user_id} status change : {event.status} ")
