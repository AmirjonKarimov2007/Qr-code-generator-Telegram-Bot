from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Command
import asyncio
from loader import dp,bot
import qrcode
import requests
from io import BytesIO
from aiogram.types import InputFile

def upload_image_to_fileio(image_bytes):
    api_url = "https://file.io"
    
    files = {"file": ("image.jpg", image_bytes)}
    response = requests.post(api_url, files=files)
    
    if response.status_code == 200:
        result = response.json()
        return result["link"]
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

@dp.message_handler(content_types=types.ContentType.TEXT)
async def send_text_based_qr(message: types.Message):
    qr = qrcode.QRCode(version=1,
                       error_correction = qrcode.constants.ERROR_CORRECT_L,
                       box_size = 20, 
                       border = 2)

    qr.add_data(message.text)
    qr.make(fit = True)  

    img = qr.make_image(fill_color = 'black', back_color = 'white')
    img.save('photo.png')
    img = InputFile('photo.png')

    await message.reply_photo(img, caption = f'<b>✅ Qr code Tayyor \n\n👉@generate_qr_codes_bot</b>', parse_mode = 'HTML')


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def send_photo_qr(message: types.Message):
    # Get the photo file_id
    file_id = message.photo[-1].file_id

    # Download the photo
    photo = await bot.download_file_by_id(file_id)

    # Convert the photo to a link
    image_link = upload_image_to_fileio(photo.getvalue())

    if image_link:
        # Upload the image and get the link
        with open('photo.png', 'rb') as image_file:
            qr_image_link = upload_image_to_fileio(image_file.read())

        if qr_image_link:
            qr = qrcode.QRCode(version=1,
                       error_correction = qrcode.constants.ERROR_CORRECT_L,
                       box_size = 20, 
                       border = 2)

            qr.add_data(qr_image_link)
            qr.make(fit = True)  

            img = qr.make_image(fill_color = 'black', back_color = 'white')
            img.save('photo.png')
            img = InputFile('photo.png')
            await message.reply_photo(img, caption = f'<b>✅ Qr code Tayyor \n\n👉@generate_qr_codes_bot</b>', parse_mode = 'HTML')


        else:
            await message.reply("❌ QR-Codeni qilishda muammo yuz berdi")
    else:
        await message.reply("❌ Rasmni qrcodega aylantirirshda muammo bo'ldi buning uchun uzr so'raymiz")