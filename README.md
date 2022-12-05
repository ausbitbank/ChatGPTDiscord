# ChatGPT
Reverse Engineered ChatGPT by OpenAI. Extensible for chatbots etc. Forked from https://github.com/acheong08/ChatGPT

# Setup
## Install
`pip3 install revChatGPT --upgrade`
`pip3 install discord json`

## Get your session token
Go to https://chat.openai.com/chat and log in or sign up
1. Open console with `F12`
2. Open `Application` tab > Cookies
![image](https://user-images.githubusercontent.com/36258159/205494773-32ef651a-994d-435a-9f76-a26699935dac.png)
3. Copy the value for `__Secure-next-auth.session-token` and paste it into `config.json.example` under `session_token`. You do not need to fill out `Authorization`
![image](https://user-images.githubusercontent.com/36258159/205495076-664a8113-eda5-4d1e-84d3-6fad3614cfd8.png)
4. Save your discord api key, and the discord channel id where you would like to interact with the bot in the config file.
5. Save the modified file to `config.json` (In the current working directory)

## Create a discord bot

1. Go to https://discord.com/developers/applications create an application.
2. And build a bot under the application.
3. Get the token from Bot setting.


   ![1670143818339](image/README/1670143818339.png)
4. Store the token to `config.json` under the `discord_bot_token`

   ![1670176461891](image/README/1670176461891.png)
5. Turn MESSAGE CONTENT INTENT `ON`

   ![1670176647431](image/README/1670176647431.png)
6. Invite your bot through OAuth2 URL Generator

   ![1670176722801](image/README/1670176722801.png)



# Running
```
 $ python3 ChatGPTDiscord.py            
