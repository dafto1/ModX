import discord 
import random
import praw
import openai
import asyncio
import os 
import DiscordUtils
from discord.ext import commands
from discord import app_commands 
from dotenv import load_dotenv

load_dotenv()
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
client_pass = os.environ.get('CLIENT_PASS')
client_user = os.environ.get('CLIENT_USER')
api_key = os.environ.get('OPENAI_API_KEY')
dc_token = os.environ.get('TOKEN')


reddit = praw.Reddit(client_id = client_id,
                     client_secret = client_secret, 
                     username = client_user,
                     password= client_pass,
                     user_agent = 'pythonPraw')

ModX = commands.Bot(intents= discord.Intents.all(), command_prefix = "!")
ModX.remove_command('help')



@ModX.event
async def on_ready():
  await  ModX.change_presence(status = discord.Status.dnd, activity = discord.Game("Moderating, Answering and Memeing!"))
 
#help 
@ModX.command()
async def help(ctx, member:discord.Member = None):  
   bot_user = ModX.user
   avatar_url = bot_user.avatar
   embed = discord.Embed(title = "__ModX commands__", description= "Useful bot commands", colour=discord.Colour.pink())
   
   embed.add_field(name= "`!help`", value = "Gives list of commands")
   embed.set_thumbnail(url =avatar_url )
   embed.add_field(name= "`!kick`", value = 'Kicks the user from server')
   embed.add_field(name= "`!ban`", value = 'Bans the user from server')
   embed.add_field(name= "`!mute`", value = 'Mutes the user in voice channel')
   embed.add_field(name = "`!unmute`", value = "Unmutes the user in voice channel")
   embed.add_field(name= "`!createText`", value = "!createText <channel> <category>")
   embed.add_field(name = "`!createVoice`", value = "!createText <channel> <category>")
   embed.add_field(name= "`!delTxt`", value = "Deletes the text channel")
   embed.add_field(name= "`!delVc`", value = "Deletes the Voice Channel")
   embed.add_field(name="`!invite`", value = "Creates an Instant Server Invite")
   embed.add_field(name = "`!ask`", value = "Ask any question , ChatGPT shall answer")
   embed.add_field(name= "`!meme`", value = "Trending memes from r/memes")
   embed.add_field(name= "`!memeIn`", value = "Trending memes from r/SaimanSays")
   embed.add_field(name= "`!checkSub`", value = "Check trending posts of your favourite subreddit : \n !checkSub <subreddit-name>")
   embed.add_field(name= "`!whois`", value = 'Gives information about a user in an embed') 
   
   await ctx.message.reply(embed = embed)


   
# !meme
@ModX.command()
async def meme(ctx):
   subreddit = reddit.subreddit("memes")
   posts = []

   for submission in subreddit.hot(limit = 50) :
      posts.append(submission)
  

   random_post = random.choice(posts)
   name = random_post.title
   url = random_post.url 
   

   redditEm = discord.Embed(title = name, color = discord.Color.random())
   redditEm.set_image(url = url)
  
   await ctx.message.reply(embed= redditEm)

#memeIn
@ModX.command()
async def memeIn(ctx):
   subreddit =reddit.subreddit("SaimanSays")
   posts = []

   for submission in subreddit.hot(limit = 50) :
      posts.append(submission)

   random_post = random.choice(posts)
   name = random_post.title
   url = random_post.url 

   redditEm = discord.Embed(title = name, color = discord.Color.orange())
   redditEm.set_image(url = url)

   await ctx.message.reply(embed= redditEm)

@ModX.command()
async def checkSub(ctx, subreddit_name):
   subreddit = reddit.subreddit(subreddit_name)
   posts = []

   for submission in subreddit.hot(limit = 50):
      posts.append(submission)
   
   random_post = random.choice(posts)
   name = random_post.title
   url = random_post.url 

   redditEm = discord.Embed(title = name, color = discord.Color.random())
   redditEm.set_image(url = url)

   await ctx.message.reply(embed= redditEm)


#ask 
@ModX.command()
async def ask(ctx):
   openai.api_key = os.getenv(api_key)

   response = openai.Completion.create(
            model="text-davinci-003",
            prompt=ctx.message.content,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        
   messageToSend = response.choices[0].text
   await ctx.message.reply(messageToSend)
   
#kick 
@ModX.command()        
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member,*, reason = None):
    try:
     if reason == None:
        reason = "no reason provided"
     await ctx.guild.kick(member)
     await ctx.send(f'❌User {member.mention} has been kicked for {reason}')
    except:
       await ctx.send("User is at higher level ")


#Ban ----------
@ModX.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member, *, reason = None):
   if reason == None:
      reason = "no reason provided"
   await ctx.guild.ban(member)
   await ctx.reply(f'❌User {member.mention} banned  for {reason}')

#WHO IS 
@ModX.command(aliases=['user', 'infor'])
async def whois(ctx, member:discord.Member = None):
   if member == None:
      member= ctx.author 
   join = member.joined_at
   joinSTR =   join.strftime('%D')

   embed= discord.Embed(title= member.name, description= member.mention, color = discord.Colour.blue())
   embed.add_field(name= "ID", value = member.id, inline= True)
   embed.set_thumbnail(url = member.avatar)
   embed.add_field(name='Server Join Date', value=joinSTR, inline=False)
   await ctx.message.reply(embed= embed)


#createCategory
@ModX.command()
@commands.has_permissions(manage_guild = True)
async def createCategory(ctx, category_name):
   guild  = ctx.guild 
   category = await guild.create_category(category_name)
   await ctx.message.reply(f'👥{ctx.author.mention} created {category.mention}')


#createText
@ModX.command()
@commands.has_permissions(manage_channels=True)
async def createText(ctx, channel_name, *, category_name = None):
   guild=  ctx.guild 
   if category_name : 
      category = discord.utils.get(guild.categories, name = category_name)
      if category: 
         channel = await category.create_text_channel(channel_name)
         await ctx.message.reply(f'📜{ctx.author.mention} created {channel.mention}')
      else : 
         category = await guild.create_category(category_name)
         channel = await category.create_text_channel(channel_name)
         await ctx.message.reply(f'📜{ctx.author.mention} created {channel.mention} in {category_name}')

   else : 
      channel = await guild.create_text_channel(channel_name)
      await ctx.message.reply(f'📜{ctx.author.mention} created {channel.mention}')

      
   # await ctx.send(f'{mention} created the text channel  {channel.mention} !')

#createVoice
@ModX.command()
@commands.has_permissions(manage_channels=True)
async def createVoice(ctx, channel_name, *, category_name = None):
   guild = ctx.guild 

   if category_name :
      category = discord.utils.get(guild.categories, name = category_name)
      if category : 
         channel = await category.create_voice_channel(channel_name)
         await ctx.message.reply(f'🎤{ctx.author.mention} created {channel.mention}')
      else : 
         category = await guild.create_category(category_name)
         channel = await category.create_voice_channel(channel_name)
         await ctx.message.reply(f'🎤{ctx.author.mention} created {channel.mention} in {category_name}')

   else : 
      channel = await  guild.create_voice_channel(channel_name)
      await ctx.message.reply(f'🎤{ctx.author.mention} created {channel.mention}')


#delTxt
@ModX.command()
@commands.has_permissions(manage_channels=True)
async def delTxt(ctx):
   channel_name = ctx.channel.name
   channel = ctx.channel.delete(channel_name)
   await ctx.message.reply(f'{ctx.author.name} deleted the {channel.mention}')

#delVc
@ModX.command()
@commands.has_permissions(manage_channels=True)
async def delVc(ctx, vc_name):
   guild = ctx.guild
   channel = await guild.delete_voice_channel(vc_name)
   await ctx.message.reply(f'{ctx.author.name} delted the {channel.meniton}')

#mute 
@ModX.command()
@commands.has_guild_permissions(mute_members=True)  
async def mute(ctx, member: discord.Member):
    if member.voice:
        await member.edit(mute=True)
        await ctx.message.reply(f'{member.mention} was muted by {ctx.author.mention}')
    else:
        await ctx.message.reply(f'{member.mention} is not currently in a voice channel.')

#unmute 
@ModX.command()
@commands.has_guild_permissions(mute_members = True)
async def unmute(ctx, member:discord.Member):
   if member.voice:
      await member.edit(mute= False)
      await ctx.message.reply(f"{member.mention} was unmuted by {ctx.author.mention}")
   else:
      await ctx.message.reply(f"{member.mention} is not in the voice channel right now {ctx.author.mention}")

#mute error
@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"You don't have permission to mute or unmute  members {ctx.author.mention}")

#invite
@ModX.command()
async def invite(ctx):
   link = await ctx.channel.create_invite(max_age = 3600)
   await ctx.message.reply(f"Here is your server invite {ctx.author.mention}: \n {link}")

ModX.run(dc_token)