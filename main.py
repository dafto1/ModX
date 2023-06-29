import discord 
from discord.ext import commands
from discord import app_commands 
import os 
import openai

ModX = commands.Bot(intents= discord.Intents.all(), command_prefix = "!")
ModX.remove_command('help')


#help 
@ModX.command()
async def help(ctx, member:discord.Member = None):  
   bot_user = ModX.user
   avatar_url = bot_user.avatar
   embed = discord.Embed(title = "ModX commands", description= "Useful bot commands", colour=discord.Colour.pink())
   
   embed.add_field(name= "!help", value = "Gives list of commands")
   embed.set_thumbnail(url =avatar_url )
   embed.add_field(name= "!kick", value = 'Kicks the user from server')
   embed.add_field(name= "!ban", value = 'Bans the user from server')
   embed.add_field(name= "!embed", value = 'Gives information about a user')
   await ctx.send(embed = embed, content= None)

#kick 
@ModX.command()        
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member,*, reason = None):
    try:
     if reason == None:
        reason = "no reason provided"
     await ctx.guild.kick(member)
     await ctx.send(f'User {member.mention} has been kicked for {reason}')
    except:
       await ctx.send("User is at higher level ")

#Ban ----------
@ModX.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member, *, reason = None):
   if reason == None:
      reason = "no reason provided"
   await ctx.guild.ban(member)
   await ctx.reply(f'User {member.mention} banned  for {reason}')

#WHO IS 
@ModX.command(aliases=['user', 'infor'])
async def whois(ctx, member:discord.Member):
   if member == None:
      member= ctx.author 

   embed= discord.Embed(title= member.name, description= member.mention, color = discord.Colour.blue())
   embed.add_field(name= "ID", value = member.id, inline= True)
   embed.set_thumbnail(url = member.avatar)
   await ctx.send(embed= embed)

ModX.run("MTEyMzg1NjU3NDQxMTE5MDI4Mg.GVIfOS.E7vYPyBJwzKb-g4cpNRU_d3iueArovJkdcSEFs")