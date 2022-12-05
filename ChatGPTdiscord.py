import requests, json, discord, logging, sys, signal
from revChatGPT.revChatGPT import Chatbot
'''
# API access on 127.0.0.1:9879/chatgpt?prompt=PROMPT
from flask import Flask, request
from threading import Thread
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

#Uploaded image recognition via inceptionV3
import tensorflow as tf
model = tf.keras.applications.InceptionV3(include_top=True, weights='imagenet')# Load the Inception-V3 model

def image_url_to_description(url):  # Define a function that takes a URL as an argument
    image = tf.keras.preprocessing.image.load_img(url, target_size=(299,299))  # Load the image from the URL and resize it to (299,299)
    image = tf.keras.preprocessing.image.img_to_array(image)  # Convert the image to a NumPy array
    image = tf.keras.applications.inception_v3.preprocess_input(image)  # Pre-process the image for Inception v3
    image = tf.expand_dims(image, 0)  # Add a batch dimension to the image
    predictions = model.predict(image)  # Use the Inception v3 model to make predictions on the image
    decoded_predictions = tf.keras.applications.inception_v3.decode_predictions(predictions, top=5)  # Decode the predictions to make them human-readable
    print("Image description:")  # Print a message indicating the beginning of the image description
    image_desc = "We detect the following elements in the image using inception v3 from Google\nLabel : Probability\n"  # Define a string containing a message about the predictions
    for prediction in decoded_predictions[0]:  # Loop through the predictions
        print(f" - {prediction[1]}: {prediction[2]:.2f}")  # Print each prediction
        image_desc += f"{prediction[1]} : {prediction[2]}\n"  # Add the prediction to the description string
    return image_desc  # Return the description of the image
'''
def split_string_into_chunks(string, chunk_size):
  chunks = []# Create an empty list to store the chunks
  while len(string) > 0:# Use a while loop to iterate over the string
    chunk = string[:chunk_size]# Get the first chunk_size characters from the string
    chunks.append(chunk)# Add the chunk to the list of chunks
    string = string[chunk_size:]# Remove the chunk from the original string
  return chunks# Return the list of chunks
'''
from bs4 import BeautifulSoup
def get_google_response(query):
    url='https://www.google.com/search?q='+query
    response=requests.get(url)
    soup=BeautifulSoup(response.text, "html.parser")
    results=soup.find_all('div', class_='g')
    print(results)
    result_str='Top 5 google results for: '+query
    for result in results[:5]:
        title=result.find('h3')
        link=result.find('a')
        description=result.find('span',class_='st')
        result_str+=f"{title.text}\n{link['href']}\n{description.text}"
    print(result_str)
    return result_str
'''
if __name__ == "__main__":
#    thread = Thread(target=run_api);thread.start()
    with open("config.json", "r") as f: config = json.load(f)
    chatbot = Chatbot(config, conversation_id=None);chatbot.refresh_session()
    intents = discord.Intents.default();intents.message_content = True
    client = discord.Client(intents=intents)
    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')

    @client.event
    async def on_message(message):
        if message.author == client.user: return
        if message.channel.id != config["discord_channel"]: return
        if message.author.bot: return
        if message.content == 'refresh' and message.author.id == config['discord_admin_id']: chatbot.refresh_session();return
        if message.content == 'restart' and message.author.id == config['discord_admin_id']: exec(open(sys.argv[0]).read());return
        if message.content.startswith('google'):
            chunks=split_string_into_chunks(get_google_response(message.content[7:]),1950)
            for chunk in chunks: await message.reply(chunk)
            return
        '''
        if message.attachments and message.attachments[0].width and message.attachments[0].height:
            image_url = message.attachments[0].proxy_url
            image_desc = image_url_to_description(image_url)
            await message.reply(image_desc)
            return
        '''
        if message.mentions:
            for user in message.mentions:
                if user != client.user: return
        print(message.content)
        try:
            response=chatbot.get_chat_response(message.content)
            print(response['message'])
            chunks=split_string_into_chunks(response['message'],1950)
            for chunk in chunks:
                chunk=chunk.replace("OpenAI", "EvilCorp")
                chunk=chunk.replace("!Dream:", "!dream ")
                await message.reply(chunk)
        except Exception as e:
            print("Something went wrong!")
            print(e)
    client.run(config["discord_bot_token"])
