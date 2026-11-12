# Ses, kapak, kalite kapıları ve teslim

## Sessizce kaliteli miks

Önce kaynak sesi incele: önceden müzik/SFX varsa ikinci katman ekleme. Yalnız
konuşma varsa kullanıcı `Ses Efektleri/` dosyalarından sade hareket/temas/bildirim
sesleri seç. Temas, yerleşme, hata ve çözülmeyi duyulur SFX ile destekle;
sırf az olsun diye neredeyse hepsini sessiz bırakma. Her hareketin whoosh'a
ihtiyacı yok. Leading silence veya geç
impact varsa sesi kırpılmış türevden hizala; orijinali değiştirme. Önemli sesin
gerçek duyulur darbesi görsel temasla yaklaşık ±2 karede eşleşsin.

Yerel, uygun hakla kullanılabilir enstrümantal müzik varsa düşük bir bed ekle.
Son revizyon: eski miksin müzik/SFX'i kullanıcıya fazla kısık geldi. Ses baskın
kalırken müzik belirgin bir atmosfer taşımalı; ilk mix için konuşmanın yaklaşık
10–14dB altında dene. Önceki sabit düşük gain'i kopyalama. Gain ayarı
tek başına duyulan fark değildir: kaydın/master'ın seviyesi değişir. Kısa giriş,
konuşmanın son 2–3 saniyesinde çıkış, ihtiyaçta duck/voice carve. Referans final
yaklaşık −17,3 LUFS / −1,6dBTP idi; hedef olarak ~−16..−18 LUFS ve ≤−1dBTP
uygundur, fakat bunu tutturmak için konuşmayı sıkıştırıp bozma. Son miks ölçülür.

Ses ve grafik olaylarını ayrı timeline track'lerinde düzenlenebilir bırak.
Kaynak yeterliyse normalize dışında işlem yapma; güçlü denoise/reverb/ses
karakteri değişimi varsayılan değil. Sadece görsel revizyonda ses paket hash'ini
önceki doğru çıktıyla karşılaştır; miksi sebepsiz yeniden tasarlama.

## Kapak ve süre

Bu bölümdeki kapak isteme/2s ekleme varsayılanı yalnız Reels içindir. 16:9
giriş–çıkışta landscape-intro-outro.md geçerlidir: kapak istenmediyse uygulanmaz.

Yeni istek yalnız video içeriyorsa kapağı bir kez sor, diğer işi ilerlet. Görsel
gelmediyse kullanılabilir kapaksız editi açıkça böyle etiketleyerek teslim
edebilirsin; kapaklı final tamamlandı deme. Kullanıcı bu görevde özellikle kapak
eklenmesini şart koştuysa kapak eksikliği kalan iştir. Plan: `coverFrames: 0`,
`coverMode: "not-provided"` veya `"user-opt-out"`, açıklayıcı `coverReason`;
cover sahnesi bulunmaz. Varsayılan, görsel sağlandığında hâlâ 2s kapaktır.

Görseli önce aç; dosya adından tahmin etme. Kullanıcının kapağını sona 2s
still olarak yerleştir, crop yapmadan contain ile orantılı sığdır. Dikey orana
uymazsa kalan alan beyaz olur; metin/baş/kritik obje kesilmez. Kullanıcı açıkça
istemeden resmi AI ile değiştirme, yeni başlık ya da watermark bindirme.
Fotoğrafın ayrı kopyasını da proje assets içinde koru. MP4'te sona eklemek,
Instagram/TikTok kapak metadata'sının otomatik seçilmesi demek değildir; bunu
vaat etme. Kullanıcı platformda son kareyi veya ayrı resmi seçebilir.

Çıkış süresi = bütün korunmuş kaynak ses/görüntü + 2s kapak. 30fps'de son
60 kare gerçek cover'dır, son hece kapakla örtülmez. Kapak boyunca varsayılan
sessizlik. Son gerçek kaynak frame'iyle kapak arasında siyah boşluk yok.

## Sıralı kalite kapıları

1. **Plan:** source hash aynı; bütün cümleler okundu; sahneler tam süreyi
   kesintisiz kapsıyor; CTA korumaları; kelime onset'ine bağlı olaylar.
2. **Kaynak/güvenli alan:** baş/yüz/ağız ve gömülü altyazı her layout'ta açık;
   objeler tam büyüklükte ve hareket uçlarında kontrol edildi. Intro okunur
   büyüklükte; beyaz sahnede ince bağlantılar kaybolmuyor.
3. **HyperFrames:** mevcut CLI komut sözleşmesini oku. `check --strict`
   gerçek sample sayısıyla geçmeli; lint error nedeniyle 0 sample bir geçiş
   değildir. Canvas içerikleri/embedded captions DOM kontrast audit'i dışında.
4. **Hareket:** her split giriş/çıkışın öncesi, bütün hareketi ve sonrası.
   En az çıkış duration'ını örten ardışık kareler, mümkünse gerçek oynatma.
   Keyframes selector statik çözülemiyorsa canvas `--ghost` veya snapshot
   şeridi kullan; CLI exit0 tek başına hareket kanıtı değil.
5. **Render:** onaylı iş akışı içinde sıradan yerel render'a devam et.
   Varsayılan 1080×1920,30fps,H.264/AAC, high quality; CRF18 iyi başlangıçtır.
   Yerel başarılı referans: 1 worker + `--browser-gpu`; yeni ortamı kontrol et.
   Kaynağı ve cover'ı bundle dışına kaçıran path veya gizli remote asset olmasın.
6. **Encoded sonuç:** FFprobe stream/fps/frame/duration; ilk ve son frame;
   her sahnenin hero karesi; bütün kadraj geçişlerinin şeridi; boş/siyah
   kare taraması. Kaynakta mevcut kararma ile yeni bug'ı ayır. Yeni 3D sahne
   donuk veya eksik görünüyorsa render tamamlandı diye teslim etme.
7. **Ses:** final MP4'ünden ölçüm; ilk/son söz ve zor teknik bölüm. Orijinal
   mikse ses eklenmişse finalden bağımsız ASR ile karşılaştır; fark çıkınca
   ses aralığını tekrar incele, beklenen metni ASR sonucu diye yapıştırma.
   Dinleme destekleniyorsa dinle. Desteklenmiyorsa ölçüm/ASR sınırını yaz.
8. **Final:** `VERIFY.md` = dosya/hash, gerçek testler, incelenen zamanlar,
   baş/kafa/altyazı, motion, kapak ve ses bulguları. Otomatik estetik puanı
   veya izlenme başarısı uydurma. Final linki/oynatıcı ve kısa Türkçe özet.

Örnek komutlar; CLI yolunu ortamdan çöz, sürümün help'ini doğrula:

```sh
hyperframes check PROJECT --strict --at FIRST,HERO,TRANSITIONS,COVER
hyperframes render PROJECT --fps 30 --quality high --crf 18 --workers 1 --browser-gpu --output FINAL.mp4
python SKILL/scripts/reel_tools.py verify-output FINAL.mp4 PROJECT/assets/edit-plan.json
```

Komuttaki büyük harfli isimler gerçek argümanlarla değiştirilir. Çıktı önce
benzersiz yeni dosyaya yazılır; doğrulanmadan eski final üzerine yazılmaz.
Sırf render'a erişim/araç/model engeli varsa güvenli alternatifi dene. Buluta
yüklemek, ücretli işe geçmek veya kaynak kesmek için görevin kapsamını genişletme.
