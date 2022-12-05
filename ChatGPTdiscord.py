import requests
import json
import discord
import logging
from revChatGPT.revChatGPT import Chatbot

def split_string_into_chunks(string, chunk_size):
  chunks = []# Create an empty list to store the chunks
  while len(string) > 0:# Use a while loop to iterate over the string
    chunk = string[:chunk_size]# Get the first chunk_size characters from the string
    chunks.append(chunk)# Add the chunk to the list of chunks
    string = string[chunk_size:]# Remove the chunk from the original string
  return chunks# Return the list of chunks

if __name__ == "__main__":
    with open("config.json", "r") as f:
            config = json.load(f)
    chatbot = Chatbot(config, conversation_id=None)
    chatbot.reset_chat()
    chatbot.refresh_session()
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if message.channel.id != config["discord_channel"]:
            return
        if message.content == 'refresh':
            chatbot.refresh_session()
        print(message.content)
        try:
            response=chatbot.get_chat_response(message.content)
            print(response['message'])
            print(response['conversation_id'])
            print(response['parent_id'])
            chunks=split_string_into_chunks(response['message'],1950)
            for chunk in chunks:
                chunk=chunk.replace("OpenAI", "EvilCorp")
                await message.reply(chunk)
        except Exception as e:
            print("Something went wrong!")
            print(e)
    client.run(config["discord_bot_token"])
