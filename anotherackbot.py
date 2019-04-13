from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os

def ack(bot, update):
  #Takes in the command /ack with a message after a space. Will ask for a proper message if none is provided
  #Responds with a message containing the message, a header "names" and an inline keyboard
  #This message will be updated with new names every time the button is pressed

  info = update.message.text.partition(' ')
  
  if info[2] == "":
    update.message.reply_text(text="Please add a message after /ack!")
  else:
    new_message = info[2] + "\n \n" + "Names:"
  
    keyboard = [InlineKeyboardButton("Yes sir", callback_data=1)],
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(text=new_message,reply_markup=reply_markup)

def button(bot, update):
  #The button creates an updated message and recreates the same inline keyboard
  #The username of the respondent is extracted and compared against the existing message
  #If the username is already there, a notification is sent saying the response is already recorded
  #Else, the message is updated with a new name and a notification is sent out
  
  query = update.callback_query
  og_message = query.message.text
  
  keyboard = [InlineKeyboardButton("Yes sir", callback_data=1)],
  same_markup = InlineKeyboardMarkup(keyboard)
  
  new_name = query.from_user['username']
  
  if new_name in og_message:
    query.answer(text="Response already recorded!")
  else:
    new_message = og_message + "\n" + new_name 
    query.edit_message_text(reply_markup=same_markup, text=new_message)
    query.answer(text="Thank you for your response!")

def start(bot, update):
  update.message.reply_text(text="Hello! This is AnotherAckBot, a hobbyist recreation of acknowledgedbot, but with notifcations after a response.")

def helpfunc(bot, update):
  the_message = """Available commands:
/start - welcome messafe
/help - this command
/ack - starts a new acknowledgement list"""
  update.message.reply_text(text=the_message)

def main():
  TOKEN = "889614406:AAHNg6ZfWsew8QCPyUoHwxlUYcQKGOfdwSY"
  NAME = "jpanotherackbot"
  PORT = os.environ.get('PORT')
  
  updater = Updater(token=TOKEN)
  dp = updater.dispatcher

  dp.add_handler(CommandHandler("ack",ack))
  dp.add_handler(CallbackQueryHandler(button))
  dp.add_handler(CommandHandler("start",start))
  dp.add_handler(CommandHandler("help",helpfunc))

  #updater.start_polling()
  updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
  updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
  
if __name__ == "__main__":
  main()