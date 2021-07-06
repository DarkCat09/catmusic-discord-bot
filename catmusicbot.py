import os
import asyncio
import discord
from discord.ext import commands
import yandex_music

# Add bot to a server:
# https://discord.com/api/oauth2/authorize?client_id=861599847441104926&permissions=2184277249&scope=bot

# Options
token = '*** YOUR TOKEN ***'
bot = commands.Bot(command_prefix='/')
# Setting up YandexMusic
ymcl = yandex_music.Client.from_credentials('achtest22@yandex.ru', 'tEs#t22')

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

		song = ymcl.search(song_query, True, 'track').tracks.results[0]
		song.download(str(song.id) + '.mp3', 'mp3')
		artist = ''

		# Joining artists into a string
		for artist_obj in song.artists:
			artist += artist_obj.name + ', '
		# Removing a comma in the end of the string
		artist = artist[:len(artist)-2]

		# Beautiful notification
		notif = discord.Embed(color=0xe3813e, title='Playing:', description=f'{artist} - {song.title}')
		notif.set_image(url=song.cover_uri)

		# Connecting to the voice channel
		sp = await music_channel.connect()
		# Stopping previously playing music
		if (sp.is_playing()):
			sp.stop()
		# Playing music to the voice channel
		sp.play(discord.FFmpegPCMAudio(source=(str(song.id) + '.mp3')), after=None)
		await ctx.send(embed=notif)
		while (sp.is_playing()):
			await asyncio.sleep(1)
		sp.stop()
		os.remove(str(song.id) + '.mp3')

# Starting bot after setup
bot.run(token)
