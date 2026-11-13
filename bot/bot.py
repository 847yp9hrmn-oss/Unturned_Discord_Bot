#Imports all needed libraries
import os
import asyncio
import nextcord
from nextcord.ext import tasks
import a2s

#Fetch from the .env file
bot_token = os.getenv("DISCORD_TOKEN")
server_ip = os.getenv("UNTURNED_SERVER")
query_port = int(os.getenv("QUERY_PORT"))

intents = nextcord.Intents.default()
client = nextcord.Client(intents=intents)

#When someone joins the server, start the bot.
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    update_status.start()


#update status task for the bot status.
@tasks.loop(seconds=30)
async def update_status():
    try:
        #Query the player count from the server.
        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(None, lambda: a2s.info((server_ip, query_port), timeout=5))

        status_text = f"{info.player_count}/{info.max_players} online"
        activity = nextcord.Game(name=status_text)
        await client.change_presence(activity=activity)
        print(f"Updated status: {status_text}")

    except Exception as e:
        print(f"Failed to query server: {e}")#Server offline warning
        await client.change_presence(activity=nextcord.Game(name="Server Offline ❌"))
        
if __name__ == "__main__":
    if not bot_token or not server_ip:
        print("Error: BOT_TOKEN and SERVER_IP must be set in the .env file.")
    else:
        client.run(bot_token)