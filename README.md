# Yerel RAG Yapay Zeka Asistanı (Microsoft Foundry Local)

İnternetsiz (offline) çalışan, PDF belgelerinden bilgi getirerek (retrieval) doğal dilde cevap üreten bir RAG (Retrieval-Augmented Generation) Soru-Cevap asistanı. Microsoft Foundry Local yaz eğitimi kapsamında, 15 günlük bir program dahilinde geliştirilmiştir.

## Proje Ne Yapar?

1. Bir PDF belgesini okur, metnini çıkarır ve anlamlı parçalara (chunk) böler
2. Her parçayı embedding'e çevirip yerel bir SQLite veritabanına kaydeder
3. Kullanıcı bir soru sorduğunda, soruya anlamca en yakın belge parçalarını bulur
4. Bulunan parçaları, yerel olarak (Foundry Local üzerinden) çalışan bir dil modeline göndererek doğal, akıcı bir cevap ürettirir
5. Belgede olmayan konularda "Bilmiyorum" diyerek uydurma (hallucination) riskini azaltır

Tüm süreç **tamamen çevrimdışı** çalışır — belge de, model de, veritabanı da kullanıcının kendi bilgisayarında durur.

## Mimari

```
PDF → metin çıkarma → cümle bazlı parçalama → embedding → SQLite (belgeler.db)
                                                                      │
Kullanıcı sorusu → embedding → en yakın parçaları bulma (cosine similarity) 
                                                                      │
                              prompt oluşturma → Foundry Local (phi-4-mini) → cevap
```

## Kurulum

1. **Foundry Local'i kur** (Windows):
   ```
   winget install Microsoft.FoundryLocal
   ```

2. **Python kütüphanelerini kur:**
   ```
   pip install pypdf sentence-transformers foundry-local-sdk openai
   ```

3. **Bir PDF belgesi ekle**: Kullanmak istediğin PDF dosyasını proje klasörüne kopyala ve `pdf_isle.py` içindeki dosya adını güncelle.

## Kullanım

1. **Belgeyi işle** (bir kez, belge değişmediği sürece tekrar gerekmez):
   ```
   python pdf_isle.py
   ```

2. **RAG asistanını başlat:**
   ```
   python rag_asistan.py
   ```

3. Terminaldeki "Sorunuz:" istemine sorunu yaz. Çıkmak için `çıkış` yaz.

## Proje Yapısı

| Dosya | Açıklama |
|---|---|
| `pdf_isle.py` | PDF okuma, parçalama, embedding oluşturma ve SQLite'a kaydetme |
| `rag_asistan.py` | Ana uygulama — retrieval + Foundry Local entegrasyonu + interaktif soru-cevap döngüsü |
| `retrieval_test.py` | Arama (retrieval) mantığının test edildiği dosya |
| `embedding_test.py`, `sqlite_test.py`, `vektor_arama_test.py`, `foundry_baglanti_test.py` | Geliştirme sürecinde kullanılan öğrenme/test scriptleri |
| `belgeler.db` | SQLite veritabanı (gitignore ile hariç tutulmuştur, `pdf_isle.py` çalıştırılınca otomatik oluşur) |

## Kullanılan Model

Foundry Local üzerinden `phi-4-mini` modeli kullanılmaktadır. Daha küçük modeller (örn. `qwen2.5-0.5b`) test edilmiş, ancak talimat takibi ve cevap tutarlılığı konusunda yetersiz bulunmuştur (bkz. proje günlüğü, Gün 10-11).

## Bilinen Sınırlamalar

- Şu an tek bir PDF ile çalışacak şekilde kurulmuştur
- Arayüz terminal tabanlıdır, grafik/web arayüzü yoktur

## Detaylı Geliştirme Günlüğü

Projenin gün gün nasıl geliştirildiği, karşılaşılan sorunlar ve çözümleri, test sonuçları için `proje_gunlugu.docx` dosyasına bakınız.
