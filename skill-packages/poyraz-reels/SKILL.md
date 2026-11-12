---
name: poyraz-reels
description: "Edit Poyraz's raw or already-cut videos into verified HyperFrames MP4s. Raw mode reviews retakes, trims silence and adds word-synced captions; pre-cut mode preserves edits and embedded captions. Portrait Reels use white upper-speaker/lower-graphics and generated or supplied covers; 16:9 hooks/outros use smooth white-stage reframing. Includes real technology logos and Apple-like motion."
---

# Poyraz Reels ve Yatay Giriş–Çıkış

Ham veya kesilmiş konuşmacı videosu → transkript → gerektiğinde temiz cut ve altyazı → ayrıntılı kurgu planı →
uygulama → görsel/ses kontrolü → oynatılabilir son MP4 ve düzenlenebilir proje.
İletişim Türkçe. Stil referansı, kullanıcının onayladığı beyaz zeminli son
Watchman monitoring kurgusudur; konu, nesneler ve zaman kodları şablon değildir.

## Önce formatı seç

FFprobe ile rotation/SAR dahil **görünen** oranı belirle. 9:16 video için aşağıdaki
Reels akışı geçerlidir. 16:9 giriş/çıkış veya kullanıcının yatay teknoloji-video
isteğinde önce [references/landscape-intro-outro.md](references/landscape-intro-outro.md)
dosyasını tamamen oku: bu mod Reels'in erken küçülme, üst konuşmacı/alt nesne,
kapak ve CTA varsayılanlarını değiştirir. Ortak transkript, kaynak koruma, ses ve
kalite kapıları kalır. Başka oranı izinsiz 9:16 veya 16:9 kırpma. Format tek başına
tam uzun videonun gövdesini editleme yetkisi vermez. Yatay tek dosyada giriş ile çıkış arasına
0.5s sessiz siyah ayraç standarttır (landscape referansı).

## Hikâye akışı — zorunlu (2026-10-19)

Plan yazmadan önce [references/story-flow.md](references/story-flow.md) ve
`Vault/07 Edit System/Poyraz Edit Rehberi.md` notunu tamamen oku. Kısaca: transkriptten sonra STORY.md
(omurga + bölüm akışları), sonra tek mesajda Materyal İhtiyaç Listesi; konuşmayı tekrar eden chip/rozet/başlık
yok; yan panel %60–80 dolu, oklarla bağlı büyük objelerle adım adım kurulan akış; sahne düzenleri karışık
(yan panel, beyaz sayfa + PIP, tam beyaz, tam kadraj + kenar objeler); müzik konuşmayı asla ezmez.
Bu dosyadaki eski “tek hero / 1–2 nesne” ifadeleri bu kuralla çelişirse story-flow geçerlidir.

## Çalışma anlaşması

- **Girdi modu:** Kullanıcı tamamen ham/uncut gönderiyorsa `raw`; cutları ve/veya
  altyazıları kendisinin hazırladığını söylüyorsa `pre-cut`. Dosya adında “raw”
  olması tek başına cut izni değildir. Ham modda
  [references/raw-edit-and-captions.md](references/raw-edit-and-captions.md) dosyasını
  önce oku; kaynak korunarak tekrar/sessizlik temizliği ve eksik altyazı üretimi
  bu kişisel akışa dahildir. Kararsız kesimlerde anlamı koru veya sor.
  Ham Reels'te sıkı hard cut ve cümle içi duraklama temizliği kullan; tam ekran
  altyazıda gri kutu değil, konturlu/gölgeli tipografi ve geri sıçramayan sakin vurgu.

- Bu skill ile editlenecek video (ve varsa kapak) gönderilmesi yerel düzenleme, tasarım kararları,
  düzeltme ve son render için yetkidir. Sadece plan ya da önizleme verip durma;
  planı dosyaya yaz, kısa özetle paylaş, ardından uygulamaya devam et. Kullanıcı
  ayrıca plan onayı isterse o noktada dur. Sıradan render için tekrar onay isteme.
- **Pre-cut modunda** kaynak zaten cut edilmiştir: yeniden kesme, sessizlik/kekeleme temizleme,
  cümle sıralama, hızlandırma, konuşmayı kısaltma veya yeni konuşma üretme yok.
  45–65 saniye tercihidir, süre hedefi için uzun gönderiyi kesme. Gerçek süreyi
  koru; Reels'te sağlanan kapağı sona ekle. Yatay giriş–çıkışta otomatik kapak yok.
  Yalnız açık yeni talimat bunu değiştirir.
- Mevcut altyazı ve CTA animasyonlarını koru. Yeni başlık, üst/alt başlık,
  paragraf veya tekrar altyazısı ekleme. **Pre-cut modunda** altyazısız kaynakta varsayılan olarak
  yeni altyazı üretme; bunu belirt. **Raw modunda** altyazı üret ve kaynakta varsa
  ikinci katman ekleme; konuşulan sözleri, yüzü ve kod okuma alanını koru.
- Videoyu, kapağı, sesi veya projenin kendisini buluta yükleme/yayımlama;
  ücretli medya üretimi, üyelik ya da yeni harcama için bu skill tek başına
  yetki değildir. Önce yerel araçları ve kullanıcının medyasını kullan.
- Girdi eksik/erişilemiyorsa veya aynı isimli birden çok farklı take varsa
  gerekli olan tek soruyu sor; eski videoyu yeni girdi sanma. Kapak eksikse
  transkript/plan gibi güvenli işleri ilerlet ama kapaklı final uydurma.
- Kullanıcının yeni talimatları bu stil varsayılanlarının önündedir. Tek bir
  revizyon istendiyse bütün videoyu yeniden tasarlama veya tekrar transkript etme;
  aynı kaynak hash'ine ait doğrulanmış transkripti kullan, etkilenen testleri yenile.

## 1. Girdiyi tanı ve kilitle

1. Workspace talimatlarını ve resmi `hyperframes` giriş skill'ini oku. Bu kişisel
   skill yaratıcı/iş akışı sözleşmesidir; resmi core/CLI kuralları teknik sözleşmedir.
   Generic `short-form-edit` içindeki cut ve yeni altyazı aşamaları yalnız raw
   modda veya açık taleple uygulanır. Her video için `video-projects/<benzersiz-ad>/` kullan.
2. Video ve varsa kapağı gerçekten aç. FFprobe ile boyut, dönüş metadata'sı, FPS,
   video/ses süreleri ve ses stream'lerini incele. Hash kaydet; orijinallere dokunma.
   `scripts/reel_tools.py probe INPUT --output JSON` bu işlemin teknik kısmıdır.
3. Tam videonun temas şeridini çıkar; yüz/kafa, eller, mikrofon, mevcut altyazı
   ve CTA alanlarının zamanla hareketini incele. Yalnız ilk kareye göre güvenli
   alan seçme. Korumalı CTA aralıklarını başlangıç/bitişleriyle işaretle.
4. Yerel node/FFmpeg/HyperFrames, Three.js/GSAP ve transkripsiyon ortamını kontrol
   et. Çalışan kurulum varsa yeniden kurma. Pinned CLI sürümünü resmi upgrade
   kontrolüyle karşılaştır; sürüm yükseltmek ile yeni kurgu üretmek aynı şey değildir.
   Gereken skill/dependency eksikse güvenli yerel kurulum yolunu kullan; engeli açıkla.

## 2. Tam transkript, sonra ayrıntılı plan

Transkripsiyon ve planlama sırasında [references/planning.md](references/planning.md)
dosyasını tamamen oku. Önce sesin tamamını gerçek bir ASR ile deşifre et:
kelime zamanları + cümle cümle okunur Türkçe transkript. Eski konuşma metnini,
kapaktaki yazıyı veya konu özetini transkript diye kullanma. Teknik terimleri
bağlam/ses ile doğrula; belirsiz kelimeleri uydurma. Ham sonuç ve düzeltmeler kalır.

`TRANSCRIPT.md`, `STORY.md` (story-flow.md), `EDIT-PLAN.md` ve `assets/edit-plan.json` üret. Her cümlede:
söylenen şey, neden bu görüntü, nesne, hareketin başlangıcı/sonucu, yerleşim,
altyazı/yüz güvenliği, kelimeye bağlı zamanlama, çıkış ve varsa SFX yazılı olsun.
Grafiksiz CTA/duygu anlarını da gerekçelendir. Planı yazmadan HTML'e geçme.

Teknoloji/ürün/firma adlarını transkriptten çıkar; her doğrulanmış markanın ilk
anlamlı bahsinde gerçek güncel logosunu göster. Bu zorunlu logo aşaması için
[poyraz-tech-logos](../poyraz-tech-logos/SKILL.md) modülünü oku ve uygula.
Yatay hook/outro için landscape referansındaki anlamsal kapsam tablosunu üret:
3–4 saniyede veya bağlam değişiminde görselin anlamı/durumu ilerlemeli. Sadece
aynı üç kartın yerini değiştirmek veya dekoratif salınım kapsam sayılmaz.

## 3. Onaylı görsel dili uygula

Aşağıdaki küçülme/üst-alt geometri kuralları **yalnız Reels modundadır**.
Yatay modda landscape-intro-outro.md'nin sağ/sol güvenli alan ve takeover kurallarını kullan.

Tasarım ve uygulama öncesinde [references/style-and-motion.md](references/style-and-motion.md)
dosyasını tamamen oku. İlk kullanımda `assets/approved-style.jpg` görselini aç;
bu renk/yoğunluk referansıdır, yeni videonun storyboard'u değildir.

- Kısa açılıştan sonra ilk doğal kavramda, çoğunlukla 3–6 saniyede beyaz alana
  geç. 10–15 saniye beklemeyi varsayma. Tam ekran anlarında büyük, okunur az
  sayıda nesne güvenli boşluklarda; yüzü, kafayı, altyazıyı kapatma.
- Anlamlı açıklama bölümünde konuşmacıyı yumuşakça küçültüp üste taşı; zemin
  **beyaz**, alt alan söylediği şeyi açıklayan gerçek hacimli 3D nesnelere ayrılır.
- Beyaz/gümüş/grafit esas, kırmızı vurgu. Apple hissi = dengeli boşluk, kaliteli
  malzeme, yumuşak ışık, yuvarlatılmış kenar, okunur siluet ve amaçlı hareket.
  Logo taklidi, başlık kartları, gelişigüzel sürekli zıplama veya yoğun efekt değil.
- Birden fazla nesne gerektiğinde ilişki/sonuç göster: bağlanma, yerleşme,
  dolma, eşiği aşma, doğrulanma. Minimal demek boş veya çok küçük demek değildir.
- Kaynakta gömülü CTA'da ek objeler çekilir; mevcut kaynak animasyonu korunur.
  Yatay çıkışın tamamını boş CTA alanı sayma: özet/fayda/sonuç boyunca anlamsal
  hareket sürer, gerçek beğen/abone sözünde istenmiş CTA gelir, son veda temizdir.
  Tam ekrana dönüş
  ve objelerin çıkışı **aynı anda, aynı eğriyle** başlar ve biter. Gecikmeli ikinci
  küçülme, kare atlama, son anda reset veya snap kabul edilmez.

Resmi `hyperframes-core`, `hyperframes-keyframes`, `hyperframes-animation`
(Three.js/GSAP) ve `hyperframes-cli` kurallarını gereken aşamada yükle. Named
efekt/nesne için registry araştır; uygun değilse nedenini kaydet ve sade yerel
geometri kullan. Yeni raster üretimi gerekirse `imagegen`, medya kaynağı için
`media-use` kullan; kullanıcıdan gereksiz varlık seçimi isteme. Hikâye için gerçekten gereken ama elde olmayan
materyali (kullanıcının gerçek çıktıları, ekran kayıtları, hook çekimleri) story-flow.md'deki Materyal İhtiyaç
Listesi ile tek mesajda iste. Özgün logo veya
dış görsel edinirken [references/external-media.md](references/external-media.md) oku.

## 4. Ses, kapak, render

[references/delivery.md](references/delivery.md) dosyasını bu aşamadan önce oku.
Konuşma baskın kalır. Sağlanan `Ses Efektleri/` klasörünü varsa kullan; sakin
enstrümantal müzik ve az sayıda anlamlı SFX ekle. Kaynakta müzik/SFX varsa
üst üste ikinci bir miks ekleme. Erişilebilir lisanslı müzik yoksa bunu belirt;
bilinmeyen müziği lisanslı gibi sunma. `hyperframes-audio` ile gain/duck/fade uygula.

Reels modunda son kelimeyi ve mevcut CTA'yı tamamla; sağlanan kullanıcı kapağını kırpmadan **2 saniye**
sona koy. Varsayılan kapak hareketsiz ve sessizdir; müzik konuşma bölümünün
sonuna doğru söner. Kapak yalnız yan dosya/metadata değil, videonun gerçek son
60 karesidir (30fps). Başlangıca bumper ekleyip ilk sözü geciktirme.

Kapak üretimi kişisel Reels akışının parçasıdır: `poyraz-reels-covers` ile üret,
`poyraz-cover-audit` ile değerlendir. Hazır kapak verilmişse onu koru. Üretim için
temel kapak/kimlik referansı rollerini doğrula; eksik temel tasarımı eski bölümün
başlığıyla kullanma. Yeni temel tasarım gerekiyorsa bunu bir kez netleştir,
transkript ve editi bu sırada ilerlet. Bölüm numarası/konu bu videoyla eşleşmeli.
16:9 videolara bu kapak zorunluluğunu taşıma.

## 5. Kanıtla ve teslim et

- Planı `scripts/reel_tools.py validate-plan assets/edit-plan.json assets/transcript.json`
  ile kontrol et; bu yapısal testtir, görsel kaliteyi veya ASR doğruluğunu onaylamaz.
- Resmi strict check + bütün sahnelerde tam boy/telefon boyu kareler + tüm
  küçülme/büyüme geçişlerinde ardışık kare şeritleri. WebGL için ghost veya
  gerçek kare incelemesi gerekir; DOM kutusu 3D nesneleri doğrulamaz.
- Taslak gerekiyorsa kendin incele ve düzelt, sonra yüksek kaliteli final üret.
  Kaynak süresi/FPS/son hece, kapak, ses baskınlığı, CTA, altyazı çakışması ve
  geçiş akıcılığı **encoded MP4** üzerinde doğrulanır. Sadece önizleme yeterli değil.
- `scripts/reel_tools.py verify-output FINAL PLAN` ile çözünürlük/FPS/süre/kare/ses
  doğrula. `VERIFY.md` içine gerçek kontrolleri, hash'i ve inceleme sınırlarını yaz.
  Dinleme aracı yoksa ölçüm/ASR yaptığını söyle; dinledim/baştan sona izledim deme.
- Kullanıcıya kısa Türkçe özet + oynatılabilir final MP4 sun; proje, transkript,
  detaylı plan, kapak ve QA yerelde kalsın. Otomatik paylaşım/yayın yapma.
  Önceki çıktıyı yalnız kullanıcı istediğinde ve yenisi doğrulandıktan sonra
  hedefi kesinleştirerek tercihen çöp kutusuna taşı; kaynakları asla temizleme.

## Yardımcılar

- `assets/motion.mjs`: ölçek/kadraj ve nesne çıkışına ortak deterministik eğri;
  yeni projeye kopyala, geometriyi yeni yüz/altyazı konumuna göre ayarla.
- `scripts/transcribe_local.py`: yerel faster-whisper, kelime zamanları,
  kaynak hash'i; mevcut model önbelleğini kullanır, gizli upload yapmaz.
- `scripts/test_reel_tools.py`, `scripts/test_motion.mjs`: yardımcıların testleri.
- [references/approved-reference.md](references/approved-reference.md): onaylı
  projenin yerel konumu ve tasarımın hangi kararlarla son haline geldiği.
