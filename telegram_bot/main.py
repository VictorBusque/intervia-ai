import logging
import requests
import telegram
from telegram import Update, File
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
from os import getenv

load_dotenv()

# Enable logging (optional, but helpful)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def stt(file: File) -> str:
    file_binary = file.download_as_bytearray()
    response = requests.post(f"{getenv('BACKEND_API_URL')}/speech/stt", files={"audio_file": file_binary})
    response.raise_for_status()
    voice_note = response.json()
    voice_note_text = voice_note.get("text")
    return voice_note_text


def tts(text: str) -> bytes:
    text = text.replace("Score", "")
    url = f"{getenv('BACKEND_API_URL')}/speech/tts?text={text}"
    response = requests.get(url)
    response.raise_for_status()
    file = bytes(response.content)
    return file


def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! I will redirect all your messages to a specified URL.')


def clear(update: Update, _: CallbackContext) -> None:
    user_id = update.effective_user.id
    response = requests.delete(f"{getenv('BACKEND_API_URL')}/conversation/{user_id}")
    response.raise_for_status()
    update.message.reply_text('Conversation has been restarted.')


def save_voice_note(update, context):
    voice_note = update.message.voice
    file_id = voice_note.file_id

    context.bot.send_chat_action(update.effective_user.id, 'typing')
    # Download the voice note
    file = context.bot.get_file(file_id)
    transcription = stt(file)

    update.message.reply_text("*Transcription* :\n" + transcription, parse_mode='Markdown')
    new_updt = update
    new_updt.message.text = transcription
    return process_message(new_updt, context)


def process_message(update: Update, context: CallbackContext) -> None:
    """Redirect incoming messages to the specified URL."""
    user_id = update.effective_user.id
    message_text = update.message.text
    context.bot.send_chat_action(user_id, 'typing')
    payload = {
        "text": message_text
    }

    try:
        response = requests.post(f"{getenv('BACKEND_API_URL')}/conversation/{user_id}/message", json=payload)
        response.raise_for_status()
        logger.info(f"Message sent successfully to API: {response.json()}")

        response_json = response.json()
        api_response_content = response_json.get("response").get("content")
        if api_response_content:
            # Send the API response back to the user as a message
            update.message.reply_text(api_response_content)

            voice_note = tts(api_response_content)
            file = telegram.InputFile(obj=voice_note)
            context.bot.send_voice(user_id, voice=file)

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
    dispatcher.add_handler(MessageHandler(Filters.voice, save_voice_note))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process_message))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
