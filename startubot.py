# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys
import logging
from pathlib import Path
from telethon.sessions import StringSession

from ubot import ubot
from ubot.storage import Storage


logging.basicConfig(level=logging.INFO)

# Confguration
ENV = bool(os.environ.get("ENV", False))
if ENV:
    from sample_config import Config
else:
    if os.path.exists("config.py"):
        from config import Development as Config
    else:
        logging.warning("No config.py Found!")
        logging.info("Run the command again after creating a config.py")
        sys.exit(1)


if Config.HU_STRING_SESSION is not None:
    # for Running on Heroku
    session_name = str(Config.HU_STRING_SESSION)
    ubot = ubot(
        StringSession(session_name),
        plugin_path="ubot/plugins/",
        storage=lambda n: Storage(Path("data") / n),
        api_config=Config,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH
    )
    ubot.run_until_disconnected()

elif len(sys.argv) == 2:
    # for running on GNU/Linux
    session_name = str(sys.argv[1])
    ubot = ubot(
        session_name,
        plugin_path="plugins/",
        storage=lambda n: Storage(Path("data") / n),
        connection_retries=None,
        api_config=Config,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH
    )
    ubot.run_until_disconnected()
else:
    logging.error("Do: python3 -m startubot  after making config.py")
