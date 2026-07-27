from foundry_local_sdk import Configuration, FoundryLocalManager

# 1. SDK'yı başlat (uygulamana bir isim veriyorsun, herhangi bir isim olabilir)
config = Configuration(app_name="rag_projesi")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

# 2. Modeli seç (Gün 1'de zaten indirmiştik, tekrar indirmeyecek)
model = manager.catalog.get_model("qwen2.5-0.5b")
model.download(lambda progress: print(f"\rİndiriliyor: {progress:.1f}%", end=""))
print()
model.load()
print("Model yüklendi.\n")

# 3. Sohbet istemcisi (chat client) al
client = model.get_chat_client()

# 4. Basit bir test sorusu gönder (cevap parça parça / streaming gelir)
messages = [{"role": "user", "content": "Merhaba, sen kimsin?"}]

print("Cevap: ", end="", flush=True)
for chunk in client.complete_streaming_chat(messages):
    if not chunk.choices:
        continue
    icerik = chunk.choices[0].delta.content
    if icerik:
        print(icerik, end="", flush=True)
print()

# 5. Modeli bellekten kaldır
model.unload()