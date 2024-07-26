from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

TOKEN = '7470575442:AAGyyKbX00JmPrVs1S01UeSSjREUH_YRziU'
WATERMARK_TEXT = 'Your Watermark'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send me an image and I will add a watermark to it.')

def add_watermark(image_path: BytesIO) -> BytesIO:
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    width, height = image.size
    textwidth, textheight = draw.textsize(WATERMARK_TEXT, font)
    x = width - textwidth - 10
    y = height - textheight - 10

    draw.text((x, y), WATERMARK_TEXT, font=font)

    output = BytesIO()
    output.name = 'watermarked_image.png'
    image.save(output, format='PNG')
    output.seek(0)
    
    return output

def handle_photo(update: Update, context: CallbackContext) -> None:
    photo = update.message.photo[-1]
    photo_file = context.bot.get_file(photo.file_id)
    photo_bytes = BytesIO(requests.get(photo_file.file_path).content)

    watermarked_image = add_watermark(photo_bytes)
    
    update.message.reply_photo(photo=InputFile(watermarked_image))

def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
