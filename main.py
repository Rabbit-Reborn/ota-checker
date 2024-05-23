#
# Rabbit R1 OTA Checker
# Made by Proton0
#

# -------- CONFIGURATIONS --------- #
update_url = "rabbit_OS_v0.8.50_20240407162326.json" # default
update_url_base = "https://ota.transactional.pub/qa/"
webhook = "https://discord.com/api/webhooks/1243089400737304647/v0IcdxRLncS0u_2_LCPCbMOncQ5-RP_O3u2ZOo7yAWjw3JMgLKD_I_Dj1yUAw5ja3Bhw"
# --------------------------------- #
import requests
import time
from discord_webhook import DiscordWebhook, DiscordEmbed

while True:
    try:
        print("Checking for updates...")
        r = requests.get(f"{update_url_base}{update_url}")
        if r.status_code == 200:
            print("UPDATE FOUND!")
            print("GET info")
            update_info = r.json()
            webhook = DiscordWebhook(url=webhook, rate_limit_retry=True)
            # Create embed

            embed = DiscordEmbed(title=f'New OTA: {update_info["version"]}', description=update_info["info"], color=0x00ff00)

            embed.add_embed_field(name="Name", value=update_info["name"])
            embed.add_embed_field(name="Version", value=update_info["version"])
            embed.add_embed_field(name="Info", value=update_info["info"])
            embed.add_embed_field(name="Update URL", value=update_info['url'])

            streaming = False

            if "property_files" in update_info:
                streaming = True
                print("update is streaming")

            embed.add_embed_field(name="Streaming?", value=str(streaming))

            webhook.add_embed(embed)
            webhook.execute()
            update_url = update_info['version'] + ".json"


        elif r.status_code == 403:
            print("No updates")
        else:
            print(f"OTA CHECK ERROR (REQUEST) : {r.status_code} {r.text}")

        time.sleep(3600) # 1 hour
    except Exception as e:
        print("ERROR: {e}")