from pypdf import PdfReader

# PDF dosyasını aç
reader = PdfReader("SOS113U_Unite1_UniteOzeti0_12V1S1.pdf")

print(f"Toplam sayfa sayısı: {len(reader.pages)}")
print()

# Tüm sayfalardaki metni tek bir değişkende topla
tum_metin = ""
for sayfa in reader.pages:
    tum_metin += sayfa.extract_text()

print("--- Çıkarılan Metnin İlk 500 Karakteri ---")
print(tum_metin[:500])

print()
print(f"Toplam karakter sayısı: {len(tum_metin)}")

def metni_parcala(metin, parca_boyutu=500):
    parcalar = []
    for i in range(0, len(metin), parca_boyutu):
        parca = metin[i:i + parca_boyutu]
        parcalar.append(parca)
    return parcalar

parcalar = metni_parcala(tum_metin, parca_boyutu=500)

print(f"\nToplam parça sayısı: {len(parcalar)}")
print("\n--- İlk Parça ---")
print(parcalar[0])
print("\n--- İkinci Parça ---")
print(parcalar[1])

import re

def cumlelere_bol(metin):
    # Nokta, ünlem veya soru işaretinden sonra gelen boşluğa göre böl
    cumleler = re.split(r'(?<=[.!?])\s+', metin)
    return cumleler

def cumle_bazli_parcala(metin, hedef_boyut=500):
    cumleler = cumlelere_bol(metin)
    parcalar = []
    mevcut_parca = ""

    for cumle in cumleler:
        # Eğer bu cümleyi eklemek parçayı çok büyütecekse, mevcut parçayı kapat
        if len(mevcut_parca) + len(cumle) > hedef_boyut and mevcut_parca != "":
            parcalar.append(mevcut_parca.strip())
            mevcut_parca = cumle
        else:
            mevcut_parca += " " + cumle

    # Son kalan parçayı da ekle
    if mevcut_parca.strip() != "":
        parcalar.append(mevcut_parca.strip())

    return parcalar

# Yeni yöntemle parçala
yeni_parcalar = cumle_bazli_parcala(tum_metin, hedef_boyut=500)

print(f"\n--- Yeni Yöntem: Cümle Bazlı Parçalama ---")
print(f"Toplam parça sayısı: {len(yeni_parcalar)}")
print("\n--- İlk Parça ---")
print(yeni_parcalar[0])
print("\n--- İkinci Parça ---")
print(yeni_parcalar[1])