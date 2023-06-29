import discord
import os
import openai

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents = intents)
@client.event
async def on_message(message):
  if client.user in message.mentions:
    openai.api_key = "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"

    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=message.content,
      temperature=1,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
   
    messageToSend = response.choices[0].text
    await message.reply(messageToSend)
   

client.run('MTEyMjkwMDg4MTY1NDk2MDE5Mg.Gx5vZY.UT7XHCB2bx12qeuo4uy5HGZXO-DHKAh7cEkm5U')