from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Sahte bir "belge" - birkaç ayrı bilgi cümlesi
belge_parcalari = [
    "Yıllık izin süresi 14 gündür.",
    "Şirket çalışma saatleri 09:00 - 18:00 arasındadır.",
    "Uzaktan çalışma haftada 2 gün ile sınırlıdır.",
    "Öğle yemeği molası 1 saattir.",
    "Yeni çalışanlar için deneme süresi 2 aydır."
]

# Belge parçalarının embedding'lerini önceden hesapla
belge_embeddingleri = model.encode(belge_parcalari)

# Kullanıcı sorusu
soru = "Kaç gün izin hakkım var?"
soru_embedding = model.encode(soru)

# Soru embeddingini TÜM belge parçalarıyla karşılaştır
benzerlikler = util.cos_sim(soru_embedding, belge_embeddingleri)[0]

print(f"Soru: {soru}\n")
print("--- Tüm Parçalarla Benzerlik Skorları ---")
for i, parca in enumerate(belge_parcalari):
    print(f"{benzerlikler[i]:.3f}  -  {parca}")

# En yüksek skora sahip parçayı bul
en_iyi_index = benzerlikler.argmax()
print(f"\n>>> EN ALAKALI PARÇA: {belge_parcalari[en_iyi_index]}")