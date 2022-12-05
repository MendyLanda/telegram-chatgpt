import json

import telebot
from telebot import util

from revChatGPT.revChatGPT import Chatbot


# read config json file
with open('config.json') as config_file:
    config = json.load(config_file)
5
# initialize chatbot
chatbot = Chatbot(config["openAI"], conversation_id=None,)
chatbot.refresh_session()

# initialize telegram bot
bot = telebot.TeleBot(config["telegram"]["token"])

# Handle '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """
Hi there, I am a (unofficial) portal to OpenAI's ChatGPT model.
    
This bot was built is built with the ChatGPT API library by acheong08 and the Telegram bot library by eternnoir.

Send /help to see what I can do.
""")
    
# Handle '/help'
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, """
Here are the commands I can understand:

    /start - Start the bot
    /stop - Stop the bot
    
    /help - Show this message
    /reset - Reset the conversation
    /refresh - Refresh the session token

To start a conversation, just send me a message. I will reply with a message from the model.
""")

# Handle '/reset'
@bot.message_handler(commands=['reset'])
def reset_conversation(message):
    chatbot.reset_chat()
    bot.reply_to(message, "Conversation reseted.")
    
# Handle '/refresh'
@bot.message_handler(commands=['refresh'])
def refresh_session(message):
    chatbot.refresh_session()
    bot.reply_to(message, "Session refreshed.")

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def responde(message):
    # get openAI response
    resp = chatbot.get_chat_response(message.text, output="text")
    
    # check for telegram message length limit (5000 chars)
    if len(resp['message']) < 5000:
        bot.reply_to(message, resp['message'])
    else:
        splitted_text = util.smart_split(resp['message'], chars_per_string=5000)
        for text in splitted_text:
            bot.reply_to(message, text)
            
bot.infinity_polling()