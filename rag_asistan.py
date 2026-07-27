import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer, util
from foundry_local_sdk import Configuration, FoundryLocalManager

# --- 1. Kurulum: Embedding modeli ---
print("Embedding modeli yükleniyor...")
embed_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# --- 2. Kurulum: Foundry Local ---
print("Foundry Local başlatılıyor...")
config = Configuration(app_name="rag_projesi")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

llm_model = manager.catalog.get_model("phi-4-mini")
llm_model.download(lambda progress: None)
llm_model.load()
client = llm_model.get_chat_client()
print("Hazır!\n")

# --- 3. Veritabanından tüm parçaları oku (bir kere, program başlarken) ---
baglanti = sqlite3.connect("belgeler.db")
cursor = baglanti.cursor()
cursor.execute("SELECT metin, embedding FROM belgeler")
sonuclar = cursor.fetchall()
baglanti.close()

metinler = []
embeddingler = []
for metin, embedding_blob in sonuclar:
    embeddingler.append(np.frombuffer(embedding_blob, dtype=np.float32))
    metinler.append(metin)

# --- 4. Retrieval fonksiyonu ---
def en_alakali_parcalari_bul(soru, top_k=3):
    soru_embedding = embed_model.encode(soru)
    benzerlikler = util.cos_sim(soru_embedding, embeddingler)[0]
    en_iyi_indeksler = np.argsort(-benzerlikler)[:top_k]
    return [metinler[i] for i in en_iyi_indeksler]

# --- 5. Prompt oluşturma fonksiyonu ---
def prompt_olustur(soru, bulunan_parcalar):
    baglam = "\n".join(bulunan_parcalar)
    return f"""Aşağıdaki bağlamı kullanarak soruyu cevapla. Eğer bağlamda cevap yoksa "Bilmiyorum" de.

Bağlam: {baglam}

Soru: {soru}

Cevap:"""

# --- 6. İnteraktif döngü ---
print("=== RAG Asistanı Hazır ===")
print("Çıkmak için 'çıkış' yazın.\n")

while True:
    soru = input("Sorunuz: ")
    if soru.strip().lower() == "çıkış":
        break
    if soru.strip() == "":
        print("Lütfen bir soru yazın.\n")
        continue

    bulunan_parcalar = en_alakali_parcalari_bul(soru)
    prompt = prompt_olustur(soru, bulunan_parcalar)

    messages = [{"role": "user", "content": prompt}]

    print("Cevap: ", end="", flush=True)
    for chunk in client.complete_streaming_chat(messages):
        if not chunk.choices:
            continue
        icerik = chunk.choices[0].delta.content
        if icerik:
            print(icerik, end="", flush=True)
    print("\n")

llm_model.unload()
print("Görüşürüz!")