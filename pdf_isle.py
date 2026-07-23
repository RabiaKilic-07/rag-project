from pypdf import PdfReader
import re
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer

# 1. PDF'i oku ve metni çıkar
reader = PdfReader("SOS113U_Unite1_UniteOzeti0_12V1S1.pdf")

print(f"Toplam sayfa sayısı: {len(reader.pages)}")

tum_metin = ""
for sayfa in reader.pages:
    tum_metin += sayfa.extract_text()

print(f"Toplam karakter sayısı: {len(tum_metin)}")

# 2. Cümle bazlı parçalama fonksiyonları
def cumlelere_bol(metin):
    cumleler = re.split(r'(?<=[.!?])\s+', metin)
    return cumleler

def cumle_bazli_parcala(metin, hedef_boyut=500):
    cumleler = cumlelere_bol(metin)
    parcalar = []
    mevcut_parca = ""

    for cumle in cumleler:
        if len(mevcut_parca) + len(cumle) > hedef_boyut and mevcut_parca != "":
            parcalar.append(mevcut_parca.strip())
            mevcut_parca = cumle
        else:
            mevcut_parca += " " + cumle

    if mevcut_parca.strip() != "":
        parcalar.append(mevcut_parca.strip())

    return parcalar

# 3. Metni parçala
yeni_parcalar = cumle_bazli_parcala(tum_metin, hedef_boyut=500)
print(f"Toplam parça sayısı: {len(yeni_parcalar)}")

# 4. Embedding modelini yükle
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 5. Veritabanına bağlan
baglanti = sqlite3.connect("belgeler.db")
cursor = baglanti.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS belgeler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        metin TEXT,
        embedding BLOB
    )
""")

# 6. Eski (test) verilerini temizle
cursor.execute("DELETE FROM belgeler")

# 7. Parçaları toplu halde embedding'e çevir
embeddingler = model.encode(yeni_parcalar)

# 8. Her parçayı + embedding'ini kaydet
for parca, embedding in zip(yeni_parcalar, embeddingler):
    embedding_bytes = embedding.astype(np.float32).tobytes()
    cursor.execute("INSERT INTO belgeler (metin, embedding) VALUES (?, ?)", (parca, embedding_bytes))

baglanti.commit()

print(f"\n{len(yeni_parcalar)} parça, embedding'e çevrilip veritabanına kaydedildi.")

# 9. Doğrulama
cursor.execute("SELECT COUNT(*) FROM belgeler")
toplam_kayit = cursor.fetchone()[0]
print(f"Veritabanındaki toplam kayıt sayısı: {toplam_kayit}")

baglanti.close()