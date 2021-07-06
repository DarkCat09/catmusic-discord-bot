import os
import asyncio
import discord
from discord.ext import commands
from youtubesearchpython import VideosSearch
from pytube import YouTube

# Add bot to a server:
# https://discord.com/api/oauth2/authorize?client_id=861599847441104926&permissions=2184277249&scope=bot

# Options
token = '*** YOUR TOKEN ***'
bot = commands.Bot(command_prefix='/')

# Command /catplay <search query>
@bot.command(name='catplay', description='Plays the music in a voice channel')
async def catplay(ctx, *args):

	# Get the server (guild) and the music channel
	curserver = ctx.guild
	music_channel = None
	for vch in curserver.voice_channels:
		if (vch.name == 'Музыка'):
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

		# Connecting to the voice channel
		sp = await music_channel.connect()
		# Stopping previously playing music
		if (sp.is_playing()):
			sp.stop()
		# Playing music to the voice channel
		sp.play(discord.FFmpegPCMAudio(source='music.mp3'), after=None)
		await ctx.send(embed=notif)
		while (sp.is_playing()):
			await asyncio.sleep(1)
		sp.stop()
		os.remove('music.mp3')

# Starting bot after setup
bot.run(token)
