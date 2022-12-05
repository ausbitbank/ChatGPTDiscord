import requests
import json
import uuid
import discord
import logging

class Chatbot:
    config: json
    conversation_id: str
    parent_id: str
    def __init__(self, config, conversation_id=None):
        self.config = config
        self.conversation_id = conversation_id
        self.parent_id = self.generate_uuid()

    def generate_uuid(self):
        uid = str(uuid.uuid4())
        return uid
        
    def get_chat_response(self, prompt):
        Authorization = self.config["Authorization"]
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + Authorization,
            "Content-Type": "application/json"
        }
        data = {
            "action":"next",
            "messages":[
                {"id":str(self.generate_uuid()),
                "role":"user",
                "content":{"content_type":"text","parts":[prompt]}
            }],
            "conversation_id":self.conversation_id,
            "parent_message_id":self.parent_id,
            "model":"text-davinci-002-render"
        }
        response = requests.post("https://chat.openai.com/backend-api/conversation", headers=headers, data=json.dumps(data))
        try:
            response = response.text.splitlines(True)[-4]
        except:
            print(response.text)
            return ValueError("Error: Response is not a text/event-stream")
        try:
            response = response[6:]
        except:
            print(response.text)
            return ValueError("Response is not in the correct format")
        response = json.loads(response)
        self.parent_id = response["message"]["id"]
        self.conversation_id = response["conversation_id"]
        message = response["message"]["content"]["parts"][0]
        return message

def split_string_into_chunks(string, chunk_size):
  chunks = []# Create an empty list to store the chunks
  while len(string) > 0:# Use a while loop to iterate over the string
    chunk = string[:chunk_size]# Get the first chunk_size characters from the string
    chunks.append(chunk)# Add the chunk to the list of chunks
    string = string[chunk_size:]# Remove the chunk from the original string
  return chunks# Return the list of chunks

if __name__ == "__main__":
    print("""
    ChatGPT discord bot
    """)
    with open("config.json", "r") as f:
            config = json.load(f)
    chatbot = Chatbot(config)
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
        print(message.content)
        try:
            response=chatbot.get_chat_response(message.content)
            response=response.replace("OpenAI", "EvilCorp")
            chunks=split_string_into_chunks(response,1950)
            for chunk in chunks:
                await message.reply(chunk)
        except Exception as e:
            print("Something went wrong!")
            print(e)
    client.run(config["discord_api_key"])