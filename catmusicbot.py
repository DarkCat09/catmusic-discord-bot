import os
import asyncio
import discord
from discord.ext import commands
from discord.utils import get
from youtubesearchpython import VideosSearch
from pytube import YouTube

# Add bot to a server:
# https://discord.com/api/oauth2/authorize?client_id=861599847441104926&permissions=2184277249&scope=bot

# Options
prefs__music_channel = 'Музыка'
token = '*** YOUR TOKEN ***'
bot = commands.Bot(command_prefix='/')

# Command /catplay <search query>
@bot.command()
async def catplay(ctx, *args):

	# Get the server (guild) and the music channel
	curserver = ctx.guild
	music_channel = None
	for vch in curserver.voice_channels:
		if (vch.name == prefs__music_channel):
			music_channel = vch

	if (music_channel != None):

		song_query = ' '.join(args)
		await ctx.send(':mag: **Searching...**')

		# Find music on YouTube and download it
		vs = VideosSearch(song_query, limit=1)
		yt = YouTube(vs.result()['result'][0]['link'])
		await ctx.send(':open_file_folder: **Downloading...**')
		dl = yt.streams.filter(only_audio=True).first().download()
		os.rename(yt.streams.filter(only_audio=True).first().default_filename, 'music.mp3')

		# Beautiful notification
		notif = discord.Embed(color=0xe3813e, title='Playing:', description=f'{yt.author} - {yt.title}')
		notif.set_image(url=yt.thumbnail_url)

		await ctx.send(':inbox_tray: **Connecting...**')

		# Get the VoiceClient and connect to the channel
		vc = get(bot.voice_clients, guild=curserver)
		if vc and vc.is_connected():
			await vc.move_to(music_channel)
		else:
			vc = await music_channel.connect()
		# Playing music to the voice channel
		vc.play(discord.FFmpegPCMAudio(source='music.mp3'), after=None)
		await ctx.send(embed=notif)
		while vc.is_playing():
			await asyncio.sleep(1)
		if vc.is_playing():
			vc.stop()
		os.remove('music.mp3')

# Command /catpause
@bot.command()
async def catpause(ctx):
	curserver = ctx.guild
	music_channel = None
	for vch in curserver.voice_channels:
		if (vch.name == prefs__music_channel):
			music_channel = vch

	if (music_channel != None):
		vc = get(bot.voice_clients, guild=curserver)
		await vc.move_to(music_channel)
		if (vc.is_paused()):
			vc.resume()
			await ctx.send(':arrow_forward: **Playing**')
		else:
			vc.pause()
			await ctx.send(':pause_button: **Paused**\n> To resume the playback, type the command /catpause again.')

# Command /catstop
@bot.command()
async def catstop(ctx):
	curserver = ctx.guild
	music_channel = None
	for vch in curserver.voice_channels:
		if (vch.name == prefs__music_channel):
			music_channel = vch

	if (music_channel != None):
		vc = get(bot.voice_clients, guild=curserver)
		await vc.move_to(music_channel)
		vc.stop()
		await ctx.send(':stop_button: **Stopped**')

# Starting bot after setup
bot.run(token)
