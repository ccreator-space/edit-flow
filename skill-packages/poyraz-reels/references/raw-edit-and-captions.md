# Ham kayıt → temiz cut → altyazı

Yalnız tamamen ham kaynak veya açık cut/altyazı talebinde oku. Pre-cut girdinin
zaman çizgisini değiştirme. Kullanıcının sesini yeniden üretme, hızlandırma veya
uzun bir anlatımı süre kotasına göre kısaltma bu modun varsayılanı değildir.

## Gerçek transkript ve take seçimi

1. Kaynağı hash/probe ile kilitle, tamamının görüntü temas şeridini incele.
2. Yerel ASR ile segment + kelime zamanlarını çıkar; script yalnız kapsam ve
   teknik terim kontrolüdür, söylenmeyen cümleleri altyazıya ekleme.
3. Uzun sessizliklerde ASR önceki cümleyi uydurabilir. Sıfır süreli kelimeler,
   saniyelerce uzayan tek kelime, sessizlikte sıkışmış uzun cümle ve “Altyazı M.K.”
   gibi kuyruklar kontrol işaretidir. `transcribe_local.py --vad
   --no-condition-previous-text` ikinci geçiş seçeneğidir; faster-whisper VAD
   zamanlarını kaynak saatine geri eşler. Ham çıktıları silme/değiştirme.
4. Şüpheli aralığı kısa bağımsız ASR, ses zarfı ve görüntüyle tekrar incele;
   aynı hatalı zamanları düzgün görünen cümlelere dağıtma.
5. `cut-silences` ve `cut-mistakes` skill'lerini oku. Araçları öneri üretmek
   için çalıştır, sonra **tüm** transkripti bağlamda gözden geçir. Boş aday
   listesi tekrar olmadığı anlamına gelmez. Kullanıcı temiz final için kesimleri
   zaten yetkilendirdiyse açık tekrar/bozuk take seçimlerini kaydedip uygula;
   içerik/niyet belirsizse koru veya yalnız o kararı sor.

## Tek kaynak-zaman haritası

`assets/edit-decisions.json`: fps, sourceSha256, duration, keeps
`{sourceStart,sourceEnd,start,end}` ve gerekçeli removals. Keep sınırları kareye
hizalı, artan, çakışmasız; her tutulan sözcük tam bir keep içine sığmalı.
Sonraki görsel/ses/altyazı zamanları **aynı EDL** üzerinden türetilir. Sessizlik
ve yanlış take geçişlerini birleştirip temiz kaynağı bir kez encode et; iki
ayrı kayıplı video üretme. Orijinal dokunulmaz, temiz çıktı türevdir.

Temiz türevi encode ederken Studio'nun rastgele seek işlemleri için yaklaşık
1 saniyelik GOP kullan (`-g FPS -keyint_min FPS`, sabit FPS). Uzun GOP uyarısı
varsa preview ile finali karıştırma: finalin tüm kareleri çıkarılmış olmalı;
encoded MP4'te görüntü donması ayrıca incelenir. Gereksiz ikinci encode yerine
ilk kaynaktan tekrar üretirken bu ayarı uygula.

**Poyraz'ın ham Reels varsayılanı sıkı hard cut'tır.** Cümle aralarına alışkanlıkla
0.18–0.30s nefes payı bırakma: konuşma biter bitmez sonraki söze geç. Yalnız cümle
sonlarını değil, cümle içinde kelime söyleyip düşünürken oluşan boşlukları da tara.
Konuşma hızını değiştirme. Gerçek hece/kuyruk ile nefes/oda sesini ayır; ses
seviyesi tek başına hangi take'in doğru olduğunu belirlemez.

- Önce konuşma kanalında `silencedetect` ve kısa RMS/peak pencereleri kullan;
  müzikli final miksinden sessizlik arama. -35/-32/-30 dB karşılaştırması ve
  yaklaşık 0.16s minimum aday süresi başlangıç noktasıdır, her kayıt için kalibre et.
- Adayın içinden kes; ünsüzleri koruyan yaklaşık 10–30ms kenar ve içe kare hizası
  uygula. Doğrulanmış boşlukta kalan pay çoğunlukla 1–3 kareyi geçmesin. Kısa
  fonetik kapanmaları, düşük sesli heceyi veya anlamlı dramatik susuşu körlemesine kesme.
- ASR tek sözcüğe uzun sessizlik yükleyebilir. Bağımsız kısa ASR/ses zarfıyla
  başlangıcı düzelt; kelime aralığı boşluğu kapsıyor diye onu koruma veya kelimeyi silme.
- Kesim sınırlarında gerekirse 3–5ms anti-click ses kenarı; görüntü hard cut.
  Yeni dijital sessizlik, uzun crossfade veya her kelimeye gate/denoise ekleme.
- Temiz sesin kalan sessizliklerini yeniden ölç, aday aralıklarını/gerekçelerini
  QA'ya yaz. İnceleme sırasında yeni kesim eklenirse ham kaynaktan EDL'yi yeniden
  türet; eski finali yeniden tekrar encode etme. Sözcük sırası/anlamı değişmesin.

Temiz cut kilitlenmeden animasyonları parlatma. Değişen EDL, altyazı/SFX/kamera/
kapak başlangıcını birlikte yeniden üretir. Raw, corrected ve retimed transkript
ayrı dosyalarda; kelimeler hem sourceStart/sourceEnd hem start/end taşır.
Mevcut animasyonu retime ederken yalnız olay başlangıçlarını yeni saate eşle;
animasyon progress'ini kesikli eski saate göre sürme. Özellikle .65s kamera/obje
çıkışını aynı sürekli yeni saat ve aynı eğri üzerinde koru.

## Hareketli ama okunur altyazı

- 2–5 kelimelik doğal gruplar, en fazla iki satır. Kesilen take'i veya scriptte
  olup söylenmeyen sonraki bölüm cümlesini ekleme. Teknik ad yazımını düzelt,
  konuşmacının anlamını yeniden yazma.
- Ana Türkçe sans + teknik terimler için mono; anlamlı vurgu için en çok bir
  ek display stil. Her kelimede rastgele font/dekor değişimi yok. Tüm fontlar
  yerel ve Türkçe karakterleri destekliyor olmalı.
- Kelime vurgusu gerçek onset'e bağlı; kısa giriş 0.12–0.22s, küçük yerleşme.
  Kısacık kelimelerde süreyi kısalt, önceki grubun son kelimesini kesme.
- Tam kadrajda varsayılan gri/füme kutu veya tüm cümleyi kaplayan panel **yok**.
  Kalın açık metin + ince koyu kontur/yumuşak gölge, az sayıda marka/konu renkli
  vurgu kullan. Beyaz split'te koyu metne geç; gerçek video kareleri üzerinde
  kontrastı denetle. Okunurluk sorunu varsa önce konum/kalınlık/konturu düzelt.
  Kadraj geçişinde koyu/açık temayı kamera tween'inin yarısında değiştirme:
  altyazının gerçek piksel alanı hâlâ görüntü üstündeyse açık konturlu yazıyı koru;
  beyaz banda ulaştığında koyult. Giriş ve çıkışın ara karelerini ayrı incele.
- Sözcüklerde `scale`, font boyu veya satır genişliği değiştirip reflow üretme.
  Bütün gruba 6–12px sakin giriş; vurgu renk gibi yerleşimi değiştirmeyen özellikte.
  Tamamlanan kelimelerin vurgusunu grup bitene kadar korumak uygun bir varsayılandır.
  Aktif-tek-kelime tasarımında son onset'i seç ve en çok bir kelimeyi etkin tut;
  önceki kelimenin `end + tolerans` aralığına geri dönme.
- Tek zaman otoritesi, yarı-açık `[start,end)` aralıkları; clip görünürlüğü ile
  JS tween'leri aynı opacity/transform'u yarışarak sürmesin. Sözcük zamanları
  artan ve çakışmasız olsun. İleri tarama + rastgele geri/ileri seek + aynı t'ye
  dönüş testinde aynı poz/vurgu çıkmalı; görünür grup indeksi ileri oynarken düşmesin.
- Tam kadrajda yüz/ağızdan aşağı; beyaz split'te konuşmacı altı ve kod üstü
  arasında ayrılmış sabit okunur bant. Kadraj değişiminde altyazı tek eğriyle
  taşınır. Telefonun sağ UI ve alt açıklama bölgelerinden uzak durur.
- SFX yalnız seçilmiş kavram, sonuç veya vurguya; her sözcüğe pop ekleme.
  Müzik/SFX ölçülen seviyeye göre konuşmanın altında ama duyulur kalır.
  Resmi audio carve aracı kullanılıyorsa JSON attribute'larını HTML-escape
  edilmiş çift tırnakla yaz; tek tırnaklı mevcut fade'i araç görmeyebilir.
  Her audio elementinde yalnız bir `data-automation` bulunmalı; ducking ve
  fade aynı lane kümesinde birleşmeli. Kaynak müzik seviyesini değil, final
  miksin konuşmayla ilişkisini ölç ve son kapağın gerçekten sessizliğini denetle.
- Ayrı SRT + kelime JSON'u sakla. Altyazı track'i tek mantıksal kanalda;
  sözleri raster grafik içine gömme. Kod animasyonu ve altyazı aynı cümleyi
  üçüncü defa büyük başlıkla tekrarlamasın.

## Kapılar

`node scripts/validate_raw_edit.mjs EDL TRANSCRIPT CAPTIONS` kaynak hash'i,
kare hizası, kesintisiz keep haritası, sözcük retime ve altyazı kapsamını denetler.
`node scripts/test_raw_edit.mjs` pozitif ve negatif kontrolleri çalıştırır.
Bu yapısal denetim yanlış take seçimini veya ASR doğruluğunu tek başına kanıtlamaz.

EDL kapsam/süre/kelime koruması; negatif kontroller (eksik kelime, 0.3s kaymış
caption, bir kare boşluk); her join'de ses zarfı ve ardışık video kareleri;
temiz ses veya final miksinden bağımsız ASR; ilk/son hece, çifte take ve
altyazı taşması. Gerçek dinleme yoksa bunu rapora yaz; ASR/ölçümü dinleme diye
sunma. Kaynak süresi ile final süresinin farkını ve nedenini teslimde belirt.
