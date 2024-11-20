import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def add_and_save_reviews(url, class_name, csv_filename):
    # Chrome ayarlarını yapın
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Tarayıcıyı arka planda çalıştırın
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # WebDriver'ı başlatın
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Sayfayı açın
    driver.get(url)

    # Yorumları bul
    yorumlar = driver.find_elements(By.CLASS_NAME, class_name)  # Doğru sabit `By.CLASS_NAME`

    # Yorumların bulunduğundan emin olun
    if not yorumlar:
        print("Yorum bulunamadı, sınıf adı kontrol edin.")
        driver.quit()
        return
    else:
        print(f"Bulunan yorum sayısı: {len(yorumlar)}")

    # Yorumları saklamak için bir liste oluştur
    yorum_listesi = []

    # Yorumları listeye ekle
    for yorum in yorumlar:
        yorum_text = yorum.text.strip()  # Yorumun sadece metnini al
        yorum_listesi.append(yorum_text)

    # DataFrame'e çevirin
    df = pd.DataFrame(yorum_listesi, columns=['Yorum'])

    # CSV dosyasını kaydet
    df.to_csv(csv_filename, index=False)
    print("Yorumlar başarıyla kaydedildi:", csv_filename)

    # Tarayıcıyı kapat
    driver.quit()

# Kullanım
url = 'https://www.trendyol.com/dyson/cinetic-big-ball-absolute-2-kablolu-supurge-p-7054572/yorumlar?boutiqueId=61&merchantId=117947'
class_name = 'reviews'  # Yorum metni için sınıf adı
csv_filename = 'trendyol_urun_yorumlari.csv'

add_and_save_reviews(url, class_name, csv_filename)
