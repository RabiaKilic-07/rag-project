from sentence_transformers import SentenceTransformer, util

# Embedding modelini yükle (ilk çalıştırmada internetten indirir)
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Test cümleleri
cumleler = [
    "kedi",
    "kedicik",
    "araba",
    "Yıllık izin süresi 14 gündür.",
    "Kaç gün izin hakkım var?"
]

# Her cümleyi embedding'e çevir
embeddings = model.encode(cumleler)

print("Embedding boyutu (her cümle kaç sayıdan oluşuyor):", embeddings[0].shape)
print()

# Benzerlikleri hesapla ve yazdır
print("--- Benzerlik Testleri ---")
print("kedi <-> kedicik:", util.cos_sim(embeddings[0], embeddings[1]).item())
print("kedi <-> araba:", util.cos_sim(embeddings[0], embeddings[2]).item())
print("izin cümlesi <-> izin sorusu:", util.cos_sim(embeddings[3], embeddings[4]).item())