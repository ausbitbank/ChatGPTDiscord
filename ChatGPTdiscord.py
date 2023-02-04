import requests, json, discord, logging, sys, signal, asyncio, functools, typing, os
#from revChatGPT.ChatGPT import Chatbot
from revChatGPT.Official import Chatbot

'''
Disabled functions that I played with in early functions, leaving in case others find them useful

from PIL import Image
from io import BytesIO
from pytesseract import image_to_string

# API access on 127.0.0.1:9879/chatgpt?prompt=PROMPT
from flask import Flask, request
api = Flask(__name__)
@api.route('/chatgpt')
def promptapi():
    def signal_handler(sig, frame):
        print('Exiting gracefully')
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    prompt=request.args.get('prompt')
    try:
        response=chatbot.get_chat_response(prompt)
        return response
    except Exception as e:
        print("Something went wrong with prompt api!")
        print(e)
def run_api():
    api.run(host='localhost', port=9879)


def extract_text_from_image_url(image_url):
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    return image_to_string(image)
'''
def split_string_into_chunks(string, chunk_size):
  chunks = []# Create an empty list to store the chunks
  while len(string) > 0:# Use a while loop to iterate over the string
    chunk = string[:chunk_size]# Get the first chunk_size characters from the string
    chunks.append(chunk)# Add the chunk to the list of chunks
    string = string[chunk_size:]# Remove the chunk from the original string
  return chunks# Return the list of chunks

def tidy_response(i):# Optionally spoilerify or hide the most repetitive annoying nothing responses, rebrand to EvilCorp
    spoiler_bad_responses=False
    hide_bad_responses=True
    rebrand_responses=True
    bad_responses=["As a large language model trained by OpenAI,","As a language model trained by OpenAI,","My training data has a cutoff date of 2021, so I don't have knowledge of any events or developments that have occurred since then.","I'm not able to browse the internet or access any new information, so I can only provide answers based on the data that I was trained on.","I don't have the ability to provide personal opinions or subjective judgments, as I'm only able to provide objective and factual information.","I'm not able to engage in speculative or hypothetical discussions, as I can only provide information that is based on verifiable facts.","I'm not able to provide medical, legal, or financial advice, as I'm not a qualified professional in these fields.","I'm not able to engage in conversations that promote or encourage harmful or offensive behavior.","I don't have personal experiences or opinions, and I can't provide personalized advice or recommendations.","As a language model, I'm not able to perform actions or execute commands. I can only generate text based on the input I receive.","I'm not able to provide direct answers to questions that require me to make judgments or evaluations, such as questions that ask for my opinion or perspective on a topic.","I can provide information on a wide range of subjects, but my knowledge is limited to what I have been trained on and I do not have the ability to browse the internet to find new information","I do not have the ability to browse the internet or access information outside of what I have been trained on.","I'm sorry, but as a large language model trained by OpenAI, "]
    if i.find("`") == -1: # Only attempt if no code block is inside the response
        if spoiler_bad_responses:
            #bad_responses_found=[response.replace(response, "||" + response + "||") for response in bad_responses if response in i]
            bad_responses_found=[response for response in bad_responses if response in i]
            bad_responses_string = "".join(bad_responses_found)
        if hide_bad_responses:
            for br in bad_responses:i=i.replace(br, "")
        if spoiler_bad_responses and bad_responses_string != '':i+='\n||'+bad_responses_string+'||'
    if rebrand_responses:
        i=i.replace("OpenAI", "EvilCorp")
        i=i.replace("!Dream:", "!dream ")
    return i

def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        wrapped = functools.partial(func, *args, **kwargs)
        return await loop.run_in_executor(None, wrapped)
    return wrapper

@to_thread
def get_answer(chatbot,query):
    response = chatbot.ask(query)
    return response

if __name__ == "__main__":
    with open("config.json", "r") as f: config = json.load(f)
    intents = discord.Intents.default();intents.message_content = True
    client = discord.Client(intents=intents)
    chatbot = Chatbot(api_key=config['api_key'])
    userdb={}

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')

    @client.event
    async def on_reaction_add(reaction, user):
        print(reaction)
        print(user)

    @client.event
    async def on_message(message):
        if message.author == client.user: return
        if message.channel.id != config["discord_channel"] and type(message.channel)!=discord.DMChannel: return
        if message.author.bot: return
        #if message.content == '!refresh' and message.author.id == config['discord_admin_id']: chatbot.refresh_session(); await message.add_reaction("🔄"); print("refresh session"); return
        #if message.content == '!restart' and message.author.id == config['discord_admin_id']: os.execl(__file__, *sys.argv);return
        if message.content == '!reset' and message.author.id == config['discord_admin_id']: chatbot.reset();await message.add_reaction("💪"); print("reset chat"); return
        if message.content.startswith('!dream'):return
        longquery=''
        if message.content.startswith('!hive '):
            authperm=message.content[6:]
            author=authperm.split("/")[0]
            permlink=authperm.split("/")[1].split(' ')[0].split('\n')[0]
            headers={
                "id":2,
                "jsonrpc":"2.0",
                "method":"condenser_api.get_content",
                "params": ["{}".format(author), "{}".format(permlink)]
            }
            response=requests.post("https://api.hive.blog/",json=headers)
            post=json.loads(response.text)
            post=post['result']
            body=post['body']
            title=post['title']
            longquery=title+'\n'+body
            print('attaching hive post '+author+'/'+permlink+' : '+title)
        if message.attachments and message.attachments[0].width and message.attachments[0].height:
            #image_url = message.attachments[0].proxy_url
            #image_desc = extract_text_from_image_url(image_url)
            #longquery=await message.reply(image_desc)
            return
        if message.attachments and message.attachments[0].content_type.startswith('text'):
            print('text attachment found, adding to prompt')
            attachment=message.attachments[0]
            data=await attachment.read()
            longquery=data.decode()
        if message.mentions:
            for user in message.mentions:
                if user != client.user: return
        print(message.author.name+':'+message.content)
        cid=None
        did=str(message.channel.id)
        print(did)
        cb=chatbot
        if did in userdb:
            cid=userdb[message.channel.id]
        else:
            cid=None
        try:
            query=message.content
            if longquery and longquery != '':
                query=message.content+'\n```'+longquery+'\n```'
            if isinstance(message.channel,discord.channel.DMChannel) and config["dm"]!=False:#DM, and DM's not disabled in config
                await message.reply("Direct messages have been disabled")
                return
            else:#In channel
                async with message.channel.typing():
                    response=await get_answer(cb,query)
            #userdb[did]={'cid':response['conversation_id']}
            #print(userdb)
            print(response)
            #print('ai:'+response["choices"][0]["text"])
            r=tidy_response(response["choices"][0]["text"])
            chunks=split_string_into_chunks(r,1975) # Make sure response chunks fit inside a discord message (max 2k characters)
            for chunk in chunks:
                await message.reply(chunk)

        except Exception as e:
            print("Something went wrong!")
            error=(str(e))
            #if error == "'NoneType' object is not subscriptable":
            #if error == "('Response code error: ', 429)":
            #    error+='\nPlease wait for your previous response to be answered before asking another'
            if error == "('Response code error: ', 403)":
                error+='\n403 forbidden response from api server'
            if error == "('Response code error: ', 524)":
                error+='\nHTTP response status code 524 A timeout occurred is an unofficial server error that is specific to Cloudflare. This HTTP status code occurs when a successful HTTP connection was made to the origin server but the HTTP Connection timed out before the HTTP request was complete'
            if error == "('Response code error: ', 502)":
                error+='\nHTTP response status code 502 Bad Gateway server error response code indicates that the server, while acting as a gateway or proxy, received an invalid response from the upstream server.'
            errorembed=discord.Embed(description=':warning: '+error, color=0xFF5733)
            await message.reply(embed=errorembed)
            await message.add_reaction("💩")
    client.run(config["discord_bot_token"])
