# ChatGPT
A discord bot using openAI's revChatGPT api to act as a smart chat assistant.

Currently setup for a single channel, and a single conversational thread. Will allow user to DM as well, but conversational context is shared with the public channel.

Accepts discord file upload of text based files (analyse code or essays!)

Originally forked from https://github.com/acheong08/ChatGPT

Use a version of it live at https://discord.gg/WBKG7VS8Cx

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
