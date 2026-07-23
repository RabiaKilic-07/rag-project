import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer, util

# 1. Embedding modelini yükle
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 2. Veritabanına bağlan
baglanti = sqlite3.connect("belgeler.db")
cursor = baglanti.cursor()

# 3. Tüm kayıtları oku (metin ve embedding)
cursor.execute("SELECT metin, embedding FROM belgeler")
sonuclar = cursor.fetchall()

baglanti.close()

# 4. BLOB'ları tekrar sayı listesine (embedding'e) çevir
metinler = []
embeddingler = []

for metin, embedding_blob in sonuclar:
    embedding = np.frombuffer(embedding_blob, dtype=np.float32)
    metinler.append(metin)
    embeddingler.append(embedding)

print(f"Veritabanından {len(metinler)} parça okundu ve embedding'leri geri açıldı.\n")

# 5. Kullanıcı sorusu
soru = "Sosyoloji nedir?"
soru_embedding = model.encode(soru)

# 6. Soru embedding'ini TÜM parçalarla karşılaştır
benzerlikler = util.cos_sim(soru_embedding, embeddingler)[0]

# 7. En yüksek skorlu 3 sonucu bul (top-3)
top_k = 3
en_iyi_indeksler = np.argsort(-benzerlikler)[:top_k]  # skorları büyükten küçüğe sıralar, ilk top_k'yı alır

print(f"Soru: {soru}\n")
print(f"--- En Alakalı {top_k} Parça ---")
for sira, index in enumerate(en_iyi_indeksler):
    print(f"\n{sira+1}. (Skor: {benzerlikler[index]:.3f})")
    print(metinler[index])