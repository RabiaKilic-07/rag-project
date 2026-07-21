import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer

# 1. Embedding modelini yükle
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 2. Veritabanına bağlan (dosya yoksa otomatik oluşturulur)
baglanti = sqlite3.connect("belgeler.db")
cursor = baglanti.cursor()

# 3. Tablo oluştur (varsa tekrar oluşturmaya çalışmasın diye IF NOT EXISTS ekledik)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS belgeler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        metin TEXT,
        embedding BLOB
    )
""")

# 4. Kaydedeceğimiz örnek belge parçaları
belge_parcalari = [
    "Yıllık izin süresi 14 gündür.",
    "Şirket çalışma saatleri 09:00 - 18:00 arasındadır.",
    "Uzaktan çalışma haftada 2 gün ile sınırlıdır.",
    "Öğle yemeği molası 1 saattir.",
    "Yeni çalışanlar için deneme süresi 2 aydır."
]

# 5. Her parçayı embedding'e çevirip veritabanına kaydet
for parca in belge_parcalari:
    embedding = model.encode(parca)
    embedding_bytes = embedding.astype(np.float32).tobytes()  # embedding'i BLOB formatına çeviriyoruz
    cursor.execute("INSERT INTO belgeler (metin, embedding) VALUES (?, ?)", (parca, embedding_bytes))

# 6. Değişiklikleri kalıcı hale getir
baglanti.commit()

print("5 belge parçası veritabanına kaydedildi.\n")

# 7. Veritabanından oku ve doğrula
cursor.execute("SELECT id, metin FROM belgeler")
sonuclar = cursor.fetchall()

print("--- Veritabanındaki Kayıtlar ---")
for satir in sonuclar:
    print(f"id: {satir[0]}  -  metin: {satir[1]}")

baglanti.close()