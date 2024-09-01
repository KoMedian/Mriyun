import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
from youtube_dl import YoutubeDL

bot = commands.Bot(command_prefix='!')
slash = SlashCommand(bot, sync_commands=True)

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@slash.slash(name="play", description="Play music from a URL", options=[
    create_option(
        name="url",
        description="The URL of the music",
        option_type=3,
        required=True
    )
])
async def play(ctx, url: str):
    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.send("You need to be in a voice channel to play music!")
        return

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice is None:
        voice = await voice_channel.connect()

    filename = await YTDLSource.from_url(url, loop=bot.loop)
    voice.play(discord.FFmpegPCMAudio(filename, **ffmpeg_options))
    await ctx.send(f"Playing music from {url}!")

bot.run("MTI3NzExMjI2NzUxMDUxNzgyMg.Gmm1eu.pKbaDCcOVSACI9CngmDs4lGjD1uKHsIGK3hw1c")