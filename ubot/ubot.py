# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""this guy handles the cli output"""
import asyncio
import importlib.util
import logging
import os
from pathlib import Path

import telethon.events
import telethon.utils
from telethon import TelegramClient

from . import hacks
from .storage import Storage


class ubot(TelegramClient):
    def __init__(
            self, session, *, plugin_path="plugins", storage=None,
            bot_token=None, api_config=None, **kwargs):

        self._name = "Ubot"
        self.storage = storage or (lambda n: Storage(Path("data") / n))
        self._logger = logging.getLogger("Ubot")
        self._plugins = {}
        self._plugin_path = plugin_path
        self.config = api_config

        kwargs = {
            "api_id": 6,
            "api_hash": "eb06d4abfb49dc3eeb1aeb98ae0f581e",
            "device_model": "GNU/Linux nonUI",
            "app_version": "@Ubot 0.0.1",
            "lang_code": "en",
            **kwargs
        }

        if api_config.TG_BOT_USER_NAME_BF_HER is not None:
            self.tgbot = TelegramClient(
                "Ubot",
                api_id=api_config.APP_ID,
                api_hash=api_config.API_HASH
            ).start(bot_token=api_config.TG_BOT_TOKEN_BF_HER) if api_config.TG_BOT_TOKEN_BF_HER is not None else None

        super().__init__(session, **kwargs)

        self._event_builders = hacks.ReverseList()

        self.loop.run_until_complete(self._async_init(bot_token=bot_token))
        # This plugin MUST be loaded
        core_plugin = Path(__file__).parent / "_core.py"
        self.load_plugin_from_file(core_plugin)
        db_plugin = Path(__file__).parent / "_db.py"
        self.load_plugin_from_file(db_plugin)
        eloop_plugin = Path(__file__).parent / "eloop.py"
        self.load_plugin_from_file(eloop_plugin)

        LOAD = self.config.LOAD
        NO_LOAD = self.config.NO_LOAD
        if LOAD or NO_LOAD:
            to_load = LOAD
            if to_load:
                self._logger.info(f" Modules to LOAD: {to_load}")
                # self._logger.info(to_load)
            not_to_load = NO_LOAD
            if not_to_load:
                self._logger.info(f" Modules to NOT load : {not_to_load}")
                for plugin_name in not_to_load:
                    if plugin_name in self._plugins:
                        self.remove_plugin(plugin_name)

        for p in Path().glob(f"{self._plugin_path}/*.py"):
            self.load_plugin_from_file(p)

    async def _async_init(self, **kwargs):
        await self.start(**kwargs)

        self.me = await self.get_me()
        self.uid = telethon.utils.get_peer_id(self.me)

    def load_plugin(self, shortname):
        self.load_plugin_from_file(f"{self._plugin_path}/{shortname}.py")

    def load_plugin_from_file(self, path):
        path = Path(path)
        shortname = path.stem
        name = f"Plugin.{self._name}.{shortname}"
        # print(name)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)

        mod.ubot = self
        mod.logger = logging.getLogger(shortname)
        mod.storage = self.storage(f"{self._name}/{shortname}")
        # declare Config and tgbot to be accessible by all modules
        mod.Config = self.config
        if self.config.TG_BOT_USER_NAME_BF_HER is not None:
            mod.tgbot = self.tgbot

        spec.loader.exec_module(mod)
        self._plugins[shortname] = mod
        self._logger.info(f" ✔️  Loaded plugin  : {shortname}")

    def remove_plugin(self, shortname):
        name = self._plugins[shortname].__name__

        for i in reversed(range(len(self._event_builders))):
            ev, cb = self._event_builders[i]
            if cb.__module__ == name:
                del self._event_builders[i]

        del self._plugins[shortname]
        self._logger.info(f" ✔️  Removed plugin  : {shortname}")

    def await_event(self, event_matcher, filter=None):
        fut = asyncio.Future()

        @self.on(event_matcher)
        async def cb(event):
            try:
                if filter is None or await filter(event):
                    fut.set_result(event)
            except telethon.events.StopPropagation:
                fut.set_result(event)
                raise

        fut.add_done_callback(
            lambda _: self.remove_event_handler(cb, event_matcher))

        return fut
