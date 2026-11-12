# Transkript ve kurgu planı

## Kaynak doğruluğu

`assets/source-manifest.json` içinde kaynak/kapak yolu, SHA-256, FFprobe çıktısı,
seçilen ses stream'i, kaynak ve çıkış FPS'i bulunur. Video/ses süreleri birkaç
milisaniye farklı olabilir. İçerik bitişi iki stream'in de sonunu kapsayan çıkış
karesidir: `ceil(max(videoEnd, audioEnd) * fps)`; sonda gerekirse kaynak son
karesini çok kısa tut. Son sesi sırf video track'i daha kısa diye kesme.
Kaynak anlamlı gecikmeli başlangıç, VFR veya rotation içeriyorsa normalize
edilmiş çalışma kopyası üret; kaynak-zaman eşlemesini sakla ve A/V sync kontrol et.

Yerel ASR tercih edilir. Bu workspace'te faster-whisper large-v3 CPU/int8 daha
önce kullanıldı; ortam/model hala mevcut mu kontrol et. Örnek:

```sh
python scripts/transcribe_local.py /absolute/source.mp4 --output /absolute/project/assets/transcript.raw.json --language tr --prompt 'Bu videoda gerçekten geçen teknik terimler'
```

Bu örnekte `scripts/` skill klasörüdür, cwd değildir. ASR script'i `--allow-download`
verilmedikçe yalnız yerel model arar. Model yoksa mevcut diğer yerel ASR yolunu
dene veya model indirmesini gereken izinle yap; videoyu buluta otomatik taşıma.
Kaynak birden çok ses stream'i içeriyorsa doğru konuşma stream'ini açıkça seç;
yardımcı doğrudan video verildiğinde ilk ses stream'ini okur. Seçili stream'den
WAV çıkardıysan raw dosyada WAV hash'i kalır, düzeltilmiş transkriptte asıl video
hash'ini ve audio-to-source identity mapping'i ayrıca kaydet. Zaman offset'i
uygulandıysa bunu açıkça dönüştür; yalnız hash değiştirerek başka take'i eşleme.
ASR prompt'una eski Watchman cümlelerini yapıştırma. Prompt kelime sözlüğüdür,
transkript üretme talimatı değildir. Kesilmiş videoda VAD ile zaman aralıklarını
atlamadan bütün sesi geçir. Özellikle ilk/son kelimeyi ve teknik terimleri incele.

Ham `transcript.raw.json` değişmeden kalır. Düzeltmeleri `transcript.json` ve
`TRANSCRIPT.md` içine yaz; raw → corrected nedenlerini kaydet. Konuşmacının
gramerini yeniden yazma, farklı bir cümleyle akıcılaştırma. Her cümlede id,
başlangıç, bitiş, metin; her kelimede text/start/end bulunur. ASR tahminlerini
kesin kare hassasiyeti diye sunma. Şüpheli kısmı kısa ses aralığında yeniden çöz.

## Detaylı planın içeriği

Yatay 16:9 modunda yerleşim/erken küçültme varsayılanları yerine
landscape-intro-outro.md kullanılır; transkript ve cümle/kelime eşleme aynı kalır.

`EDIT-PLAN.md` başında süre, CTA korumaları, yüz/altyazı gözlemleri, izleyicinin
kazanımı ve görsel dil yazılır. Ardından **her cümle için** bir satır veya bölüm:

| Alan | Beklenen karar |
|---|---|
| Cümle / zaman | Transkriptteki id ve birebir sözler |
| Görsel görev | Sözü tekrar yazmak yerine örnek, neden-sonuç veya ilişki |
| Yerleşim | Tam ekran konuşmacı / üst konuşmacı + alt 3D / korumalı CTA |
| Nesne | Konuya özgü, bir bakışta anlaşılan siluet; medya kaynağı |
| Hareket | Başlangıç pozu → eylem → sonuç → okunur tutuş → çıkış |
| Tetik | Kelime indeksi, gerçek onset, görsel zamanı, kasıtlı lead varsa nedeni |
| Güvenlik | Yüz ve altyazı kutuları; hareketin en geniş halinde kalan boşluk |
| Ses | SFX varsa anlamı, gerçek duyulur atak anı ve seviyelendirme |
| Süreklilik | Önceki nesneyle bağlantı, sonraki sahneye geçiş ve kapanış |

Her cümleye zorla yeni nesne koyma. Bir nesne birkaç cümlede gelişebilir; boş
bir konuşmacı anı duyguyu/CTA'yı taşıyabilir. Bunları planla; rastgele boşluk
bırakma. İlk doğal kavramda, genellikle 3–6 saniyede küçült; beyaz alandaki
anlamlı anlatımı erken başlat. Her cümlede kadrajı değiştirerek yorma.
CTA araya girerse tam ekrana dön, açıklama sürerse ikinci beyaz panel açılabilir.
13,1 / 42,3 / 49,7 / 66 eski videonun zamanlarıdır, yenisine yapıştırılmaz.

Sponsor adını, kişiyi, gerçek ürün arayüzünü doğrula. Genel temsili geometri
gerçek ürün ekranı veya ürün başarısının kanıtı değildir. Sahte istatistik yok.

## Makine planı: assets/edit-plan.json

Bu kişisel şema generic Student Kit plan şeması değildir. İki validator'ü
karıştırma; dönüşüm gerekiyorsa açık adapter yaz. Zamanlar saniye, son kareler
integer'dır. `sourceSha256` transkript kaynağıyla eşleşir.

Kapaksız teslim istisnası için delivery.md: `coverFrames: 0` yalnız açıklayıcı
`coverMode` ve `coverReason` ile geçerlidir; cover sahnesi bu durumda eklenmez.

```json
{
  "fps": 30,
  "width": 1080,
  "height": 1920,
  "sourceSha256": "actual-source-sha256",
  "contentEndFrame": 1500,
  "coverFrames": 60,
  "captionMode": "embedded",
  "protectedIntervals": [{"start": 44, "end": 50, "reason": "Kaynak takip CTA"}],
  "splitWindows": [{"start": 12, "end": 42, "transition": 0.65}],
  "scenes": [
    {"id": "opening", "start": 0, "end": 12, "layout": "full", "reason": "Konuşmacı + altta ilgili nesne", "actions": [{"wordIndex": 0, "at": 0, "object": "konuya özgü nesne", "motion": "eylem", "outcome": "anlamlı sonuç"}]},
    {"id": "explanation", "start": 12, "end": 42, "layout": "split", "reason": "Mekanizmayı göster", "actions": []},
    {"id": "cta", "start": 42, "end": 50, "layout": "full", "reason": "Kaynak CTA korunur", "actions": []},
    {"id": "cover", "start": 50, "end": 52, "layout": "cover", "reason": "Kullanıcının kapağı", "actions": []}
  ]
}
```

Örnek sayılar yalnız şema örneğidir. Gerçek tasarımda uzun açıklama sahnesini
anlamsal alt sahnelere ayır ve gerekli hareketleri yaz; actions boş olması kalite
onayı değildir. Aynı splitWindow birden çok bitişik split sahneyi kapsayabilir.
Korumalı interval'e giren sahne tamamen full ve ek objesiz olmalıdır; gerekirse
bu bölümün sınırında sahneyi böl. Her action kelime onset'ine bağlanır; önden
hazırlama en çok ~0,15s, geç kalma ~0,2s üstündeyse `timingReason` zorunludur.
Kesin nesne çıkış zamanı ve 0,65s dönüş planın Markdown kısmında da yazılır.
Yeni altyazı açıkça istendiğinde captionMode `added`, altyazısız bırakıldığında
`none`; embedded varken ikinci katman yok.
