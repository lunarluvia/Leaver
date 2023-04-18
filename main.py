import discord
from discord.ext import commands
import os
import asyncio
import logging
from keep_alive import keep_alive

# Retrieve the bot token from a Replit Secret
TOKEN = os.environ.get('BOT_TOKEN')

# Define the intents that the bot will use
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

async def update_status():
    while True:
        servers = len(bot.guilds)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{servers} Server/s"))
        await asyncio.sleep(20)

@bot.event
async def on_ready():
    logger.info(f'{bot.user.name} has connected to Discord!')
    bot.loop.create_task(update_status())

@bot.event
async def on_member_remove(member):
    # Loop through each channel and delete all messages sent by the user
    for channel in member.guild.channels:
        try:
            await channel.purge(check=lambda m: m.author == member)
        except Exception as e:
            logger.exception(e)

# Handle errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    logger.exception(error)
    await ctx.send(f"An error occurred: {str(error)}")

# Keep the app running
keep_alive()

# Run the bot
if TOKEN:
    bot.run(TOKEN)
else:
    logger.error("Bot token not found in environment variables.")
