#
# Rabbit R1 OTA Checker
# Made by Proton0
#

# -------- CONFIGURATIONS --------- #
update_url = "rabbit_OS_v0.8.50_20240407162326.json" # default
update_url_base = "https://ota.transactional.pub/qa/"
webhook_url = "https://discord.com/api/webhooks/1243089400737304647/v0IcdxRLncS0u_2_LCPCbMOncQ5-RP_O3u2ZOo7yAWjw3JMgLKD_I_Dj1yUAw5ja3Bhw"
# --------------------------------- #
import requests
import logging
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
import sys

# PM2 Logging Fix
out_stream_handler = logging.StreamHandler(sys.stdout)
out_stream_handler.setLevel(logging.DEBUG)
out_stream_handler.addFilter(lambda record: record.levelno <= logging.INFO)

err_stream_handler = logging.StreamHandler(sys.stderr)
err_stream_handler.setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s', handlers=[out_stream_handler, err_stream_handler])

while True:
    try:
        logging.info("Checking for updates...")
        r = requests.get(f"{update_url_base}{update_url}")
        if r.status_code == 200:
            logging.info("Successfully got a new update")
            update_info = r.json()
            webhook = DiscordWebhook(url=webhook_url, rate_limit_retry=True)
            # Create embed

            embed = DiscordEmbed(title=f'New OTA: {update_info["version"]}', description=update_info["info"], color=0x00ff00)

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
                    streamebed.add_embed_field(stream_file["filename"], value=f"{stream_file['size']} bytes ({mb} MB)\nFile Offset: {stream_file['offset']}")
                webhook.add_embed(streamebed)
                logging.info("Successfully made streaming embed")

            webhook.execute()
            logging.info(f"The current update URL is {update_url}")
            update_url = update_url_base + update_info['version'] + ".json"
            logging.info(f"Changed Update URL to {update_url}")


        elif r.status_code == 403:
            logging.debug("No updates")
        else:
            logging.critical(f"OTA CHECK ERROR (REQUEST) : {r.status_code} {r.text}")

        time.sleep(3600) # 1 hour
    except Exception as e:
        logging.critical("ERROR: {e}")