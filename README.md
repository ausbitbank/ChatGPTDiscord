# ChatGPTDiscord
A discord bot using openAI's ChatGPT api to act as a smart chat assistant allowing for natural, conversational interactions between users and the language model. This can be a great way to generate creative ideas, have engaging discussions, or even just pass the time with some entertaining banter.

Currently setup for a single channel, and a single conversational thread.

Accepts discord file upload of text based files (analyse code or essays!)

Splits output from chatgpt into multiple messages to get around discord message size limits.

Removes common limitation phrases from output, and rebrands OpenAI to EvilCorp.

Originally forked from https://github.com/acheong08/ChatGPT

Use a version of it (named "wiseguy") live in this discord https://discord.gg/WBKG7VS8Cx in the #chatgpt channel

# Setup
## Install
`git clone https://github.com/ausbitbank/ChatGPTDiscord`

`cd ChatGPTDiscord`

`pip3 install requests discord asyncio typing`

`pip3 install revChatGPT --upgrade`

Setup config file with the steps in https://github.com/acheong08/ChatGPT/wiki/Setup
Be sure to add in your "discord_bot_token" (api key), "discord_channel" (channel id for where you want it to response) and "discord_admin_id": (numeric admin account id)

# Running
```
 $ python3 ChatGPTDiscord.py            
```

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=ausbitbank/ChatGPTDiscord&type=Date)](https://star-history.com/#/ausbitbank/ChatGPTDiscord&Date)
