import discord
from discord.ext import commands
import random

intents = discord.Intents.all()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='?', intents=intents)

target_channel_ids = []

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Through Servers"))
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('?cross'):
        sender_name = message.author.name
        sender_tag = message.author.discriminator
        server_name = message.guild.name
        server_icon_url = str(message.guild.icon.url)
        embed_color = random.randint(0, 0xffffff)
        embed = discord.Embed(description=message.content[6:], color=embed_color)
        embed.set_author(name=f'{sender_name}#{sender_tag}')
        embed.set_thumbnail(url=server_icon_url)
        embed.set_footer(text=f'From {server_name}')
        for target_channel_id in target_channel_ids:
            target_channel = bot.get_channel(int(target_channel_id))
            await target_channel.send(embed=embed)

    elif message.content.startswith('?invite'):
        channel_ids = message.content.split()[1:]
        for channel_id in channel_ids:
            # Only add valid channel IDs to the target_channel_ids list
            if channel_id.isdigit() and channel_id not in target_channel_ids: 
                target_channel_ids.append(channel_id)
        await message.channel.send(f'Channels {", ".join(channel_ids)} have been added to the list of target channels.')

    elif message.content.startswith('?remove'):
        channel_ids = message.content.split()[1:]
        for channel_id in channel_ids:
            # Only remove valid channel IDs from the target_channel_ids list
            if channel_id.isdigit() and channel_id in target_channel_ids:
                target_channel_ids.remove(channel_id)
        await message.channel.send(f'Channels {", ".join(channel_ids)} have been removed from the list of target channels.')
    
    elif message.content.startswith('?help'):
        embed = discord.Embed(title="Help", description="List of commands available:", color=0x00ff00)
        embed.add_field(name="?cross", value="Crosspost a message to all target channels.", inline=False)
        embed.add_field(name="?invite", value="Add channels to the list of target channels.", inline=False)
        embed.add_field(name="?remove", value="remove channels to the list of target channels.", inline=False)
        await message.channel.send(embed=embed)

bot.run('YOUR_BOT_TOKEN')
