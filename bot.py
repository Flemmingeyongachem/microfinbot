from telegram.ext import MessageHandler, CommandHandler, ContextTypes, Application, filters
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, WebAppInfo
import json
from dotenv import find_dotenv,dotenv_values
from typing import Final

settings = dotenv_values(find_dotenv('.env'))
BOT_USERNAME : Final = settings.get("BOT_USERNAME")


# Define a `/start` command handler.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with a button that opens a the web app."""
    await update.message.reply_text(
        "Please press the button below to choose a color via the WebApp.",
        reply_markup=ReplyKeyboardMarkup.from_button(
            KeyboardButton(
                text="Open the color picker!",
                web_app=WebAppInfo(url="https://f9d1-102-244-223-238.ngrok-free.app/"),
                # web_app=WebAppInfo(url="https://python-telegram-bot.org/static/webappbot"),
            )
        ),
    )


# Handle incoming WebAppData
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Print the received data and remove the button."""
    # Here we use `json.loads`, since the WebApp sends the data JSON serialized string
    # (see webappbot.html)
    data = json.loads(update.effective_message.web_app_data.data)
    await update.message.reply_html(
        text=(
            f"You selected the color with the HEX value <code>{data['hex']}</code>. The "
            f"corresponding RGB value is <code>{tuple(data['rgb'].values())}</code>."
        ),
        reply_markup=ReplyKeyboardRemove(),
    )


#commands
async def start_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # print(update.message.chat)
    await update.message.reply_text(f"Welcome { ' ' + update.message.chat.first_name if update.message.chat.first_name else ' ' + update.message.chat.last_name }")
    
async def help_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome!!")
    
async def check_accountbalance_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome!!")
    
async def cashin_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Proceed in webapp!!")
    
async def cashout_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome!!")
    
async def transaction_history_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome!!")
    
async def transfer_funds_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome!!")
    

#response
def handle_response(text:str)->str:
    processed_text: str = text.lower()
    
    if "hello" in processed_text:
        return "hey there"
    return "Invalid command"

async def handle_message(update:Update, context:ContextTypes.DEFAULT_TYPE):
    #determine if chat is group chat or private chat
    message_type: str = update.message.chat.type
    text: str = update.message.text
    
    print(f'User ({update.message.chat.id}) in {message_type}:"{text}"')
    
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
        
    print(f"BOT: {response}")
    await update.message.reply_text(response)
    

#for logging
async def errors(update:Update, context:ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused the error {context.error}')
    
    

    
    
    
    
    
    
            
    
    
    
    
    
    
    
    