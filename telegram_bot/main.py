import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
from os import getenv

load_dotenv()

# Enable logging (optional, but helpful)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! I will redirect all your messages to a specified URL.')


def clear(update: Update, _: CallbackContext) -> None:
    user_id = update.effective_user.id
    response = requests.delete(f"{getenv('BACKEND_API_URL')}/conversation/{user_id}")
    response.raise_for_status()
    update.message.reply_text('Conversation has been restarted.')


def redirect_message(update: Update, _: CallbackContext) -> None:
    """Redirect incoming messages to the specified URL."""
    user_id = update.effective_user.id
    message_text = update.message.text

    payload = {
        "text": message_text
    }

    try:
        response = requests.post(f"{getenv('BACKEND_API_URL')}/conversation/{user_id}/message", json=payload)
        response.raise_for_status()
        logger.info(f"Message sent successfully to API: {response.json()}")

        response_json = response.json()
        api_response_content = response_json.get("response").get("content")
        job_post = response_json.get("job_post")
        if api_response_content:
            # Send the API response back to the user as a message
            job_post_msg = f" **{job_post.get('title')}** \n __{job_post.get('company')}__ "
            update.message.reply_text(job_post_msg, parse_mode="Markdown")
            update.message.reply_text(api_response_content)
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send message to API: {e}")


def main() -> None:
    """Run the bot."""
    # Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual bot token
    updater = Updater(getenv('TELEGRAM_TOKEN'))
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("clear", clear))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, redirect_message))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
