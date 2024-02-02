import requests

def upload_image_to_fileio(image_path):
    api_url = "https://file.io"
    
    with open(image_path, "rb") as file:
        files = {"file": file}
        response = requests.post(api_url, files=files)
    
    if response.status_code == 200:
        result = response.json()
        return result["link"]
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# Replace 'your_image_path.jpg' with the path to your image file
image_path = "/home/amirjon/Telegram_Channels_Bot/Qrcode-generator-Telegram-Bot/photo.png"

image_link = upload_image_to_fileio(image_path)

if image_link:
    print(f"Image uploaded successfully. Image Link: {image_link}")
else:
    print("Failed to upload image.")
