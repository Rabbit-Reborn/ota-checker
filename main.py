#
# Rabbit R1 OTA Checker
# Made by Proton0
#

# -------- CONFIGURATIONS --------- #
r1_version = "rabbit_OS_v0.8.50_20240407162326"  # default
update_url_base = "https://ota.transactional.pub/qa/"
#update_url_base = "http://127.0.0.1:5000/"
webhook_url = None
# --------------------------------- #
import requests
import logging
import multiline
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
import sys
import os
from dotenv import load_dotenv

load_dotenv()
webhook_url = os.getenv("DISCORD_WEBHOOK")
# PM2 Logging Fix
out_stream_handler = logging.StreamHandler(sys.stdout)
out_stream_handler.setLevel(logging.DEBUG)
out_stream_handler.addFilter(lambda record: record.levelno <= logging.INFO)

err_stream_handler = logging.StreamHandler(sys.stderr)
err_stream_handler.setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s',
                    handlers=[out_stream_handler, err_stream_handler])

while True:
    try:
        logging.info("Checking for updates...")
        r = requests.get(f"{update_url_base}{r1_version}.json", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"})
        if r.status_code == 200:

            logging.info("Successfully got a new update")
            update_info = multiline.loads(r.text, strict=False) # Add support for multiline cuz rabbit
            webhook = DiscordWebhook(url=webhook_url, rate_limit_retry=True)  # type: ignore
            # Create embed

            embed = DiscordEmbed(title=f'New OTA: {update_info["version"]}', description=update_info["info"],
                                 color=0x00ff00)

            embed.add_embed_field(name="Name", value=update_info["name"])
            embed.add_embed_field(name="Version", value=update_info["version"])
            embed.add_embed_field(name="Info", value=update_info["info"])
            embed.add_embed_field(name="Update URL", value=update_info['url'])
            logging.info("set embeds!")
            streaming = False

            if "property_files" in update_info:
                streaming = True
                logging.info("update is streaming")

            embed.add_embed_field(name="Streaming?", value=str(streaming))

            webhook.add_embed(embed)

            # add streaming embed
            if streaming:
                streamebed = DiscordEmbed(title=f"{update_info['version']} streaming information", color=0x00ff00)
                for stream_file in update_info['property_files']:
                    logging.info(f"Adding {stream_file['filename']}")
                    mb = round(stream_file['size'] / (1024 * 1024), 2)
                    streamebed.add_embed_field(stream_file["filename"],
                                               value=f"{stream_file['size']} bytes ({mb} MB)\nFile Offset: {stream_file['offset']}")
                webhook.add_embed(streamebed)
                logging.info("Successfully made streaming embed")

            webhook.execute()
            logging.info(f"The current update URL is {r1_version}")
            r1_version = update_url_base + update_info['version'] + ".json"
            logging.info(f"Changed Update URL to {r1_version}")


        elif r.status_code == 403:
            logging.debug("No updates")
        else:
            logging.critical(f"OTA CHECK ERROR (REQUEST) : {r.status_code} {r.text}")
        time.sleep(10)
    except Exception as e:
        logging.critical(f"ERROR: {e}")
