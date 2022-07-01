from discord_webhook import DiscordWebhook, DiscordEmbed # pip install discord-webhook
import config

def send_hook(title, des, color):
    webhook = DiscordWebhook(url=config.web_hook_url, rate_limit_retry=True)# , content='Webhook Message')
    embed = DiscordEmbed(title=title, description=des, color=color)
    webhook.add_embed(embed)
    response = webhook.execute()