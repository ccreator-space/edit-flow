# 16:9 teknoloji videosu — yalnız giriş ve çıkış

## Kapsam ve süre

Kullanıcı cut edilmiş giriş/çıkışları tek dosyada veya ayrı dosyalarda verir.
Yeniden cut, retake temizliği, hız veya cümle sırası değişikliği yapma. Tek dosya
yalnız giriş/çıkış içeriyorsa tamamı bu kapsamdır; aradaki öğretici bölümü üretme,
hayali içerik/geçiş ekleme. Giriş–çıkış sınırını transkript + gerçek source kareleriyle
bul ve kaydet. Ayrı dosyaların sırasını doğrula, araya istenmeyen boşluk koyma.

Tam uzun video gelmişse izinli intro/outro aralıklarını kullan. Sınırlar gerçekten
belirsizse tek kısa soru sor; gövdeyi otomatik editleme. Korunan gövde ses/görüntüsü
kesintisiz ve ek müzik/grafik olmadan kalır. Yalnız giriş/çıkış mı, tüm dosya mı
çıktı istendiğini görevden çöz; önemli belirsizliği tahmin ederek geçme.

Hedef 16:9; 1920×1080/30fps iyi varsayılan, kaynak/teslim talebi üstün gelir.
4K kaynak → 1080p seçimi planda/teslimde görünür olsun. Dikey kırpma yok.
45–65s sınırı yok, kaynak ses ve video sonunu kapsayan kareye kadar koru.
**Kapak varsayılan değil:** sorma, bekleme, Reel kapağı ekleme.
`coverFrames: 0, coverMode: "not-applicable", coverReason: "Yatay intro/outro; kapak istenmedi."`
Yalnız açık kapak isteğinde verilen oranı koru, süreyi planla.

## Transkript ve plan

Ortak planning.md akışını uygula: tam yerel ASR, kelime zamanları, ham/düzeltilmiş
metin ve her cümle için ayrıntılı plan. Konuşmacının gramerini yeniden yazma.
İntro/outro ayrımını, sponsor/kupon/URL/ad doğruluğunu ve CTA zamanlarını kaydet.
Sponsor adından emin değilsen kısa aralığı tekrar çöz; sahte logo, adres veya
kampanya şartı üretme. Orijinal kaynakta bulunmayan ticari iddia ekleme.

`mode: "landscape-intro-outro"`, `contentScope: "intro-outro-only"` veya
`"full-video-with-protected-body"` ve `editWindows` kaydet. Pencereler sıralı,
çakışmasız ve content süresi içinde; her biri role `intro` veya `outro` taşır.
Gövde varsa pencerelerin dışındaki sahneler `full`, actions boş kalır; miksin de
orada devre dışı olduğunu ayrıca doğrula. Şema layout'ları `full` ve `takeover`;
Reels `splitWindows` boş. Her takeover içinde gerekçe ve ses sürekliliği açıkça yazılır.

## Yerleşim — insan ana odak

Konuşmacının sürekli tam boy ve ortada kalması zorunlu değildir. Her zaman sağ/sol da zorunlu
değildir: beyaz sayfa + sağ üst küçük PIP, kısa tam beyaz sayfa ve tam kadraj + kenar objeler
düzenleri hikâyeye göre karıştırılır (story-flow.md). **Poyraz'ın
uzun-video standardı (24 Eylül 2026):** kısa tam-kadraj anlarını, beyaz sahnede
akıcı sağ/sol veya gerektiğinde yukarı/aşağı kamera yerleşimiyle birleştir.
Reels'teki `.8 scale`, `y=-340` geometrisini yataya kopyalama. Önce bütün dosyadan temas
şeridi incele; yüz/saç, eller ve altyazılar için zamanla değişen koruma bölgeleri
tanımla. Sadece sabit merkez kutusu veya ilk kare yeterli değildir.

1920×1080 için başlangıç: sol x=70..530, sağ x=1450..1850, ekran kenarı ≥60px.
Bunlar vaat değil kalibrasyon; kişi/eller farklıysa nesneyi kenara veya başka
zamana taşı. Ölçeği gerçek siluetten seç: yan panel %60–80 dolu olmalı; 2–4 büyük, oklarla bağlı
obje (tek obje ≥ ~380px) ile adım adım kurulan bir akış diyagramı (story-flow.md).
Güvenliği büyüklüğe feda etme; küçük kopuk ikon yağmuru da tek başına beliren
kelime-ikon eşlemesi de olmaz. Konuşmayı tekrar eden chip/pill/rozet, üst başlık,
alt başlık, paragraf, sürekli altyazı ekleme.

Sol/sağ nesneler 0.4–0.7s kontrollü yerleşir, kelimede durum değiştirir, yaklaşık
0.35–0.6s'de geldikleri boşluğa çekilir. Objeler giriş/çıkış yolunda da yüze
uğramaz. Hafif 3D kalınlık, yuvarlak kenar, yumuşak key/fill, gümüş/beyaz/grafit
ve kırmızı vurgu; konuya özgü gerçek logolar özgün renklerinde kalır.

## Zorunlu anlamsal hareket ve kamera standardı

- Hook ve çıkışta hedef, yaklaşık her 3–4 saniyede veya bağlam değiştiğinde
  anlamlı yeni eylem/durumdur. Bu mekanik kesme saati değil üst düzey ritim
  kontrolüdür. Bir graph büyüyebilir, dallanabilir, projelere bağlanabilir; her
  seferinde yeni slide/kart açmak gerekmez. Sabit üç kağıt, rastgele float veya
  aynı nesneyi sağdan sola kopyalamak yeni anlamsal beat değildir.
- Tam boy konuşmacıda güvenli yan bölgeler aktif olsun. İlişki/demonstrasyon
  için alan gerektiğinde **aynı kesintisiz video wrapper'ını** beyaz zeminde
  küçültüp yana taşı. Kaynak görüntünün doğal arka planını koru, otomatik
  segmentasyon yapma. Kamera geçişleri genellikle .65–.85s; sahne değişimi,
  crop, scale ve grafik çıkışı aynı deterministik progress'e bağlı olsun.
- Yeni kadraj bir anlatım ihtiyacını çözmeli; sırf hareket olsun diye her
  cümlede yön değiştirme. Geçiş boyunca yüz, ağız, saç ve gömülü altyazı açık
  kalır. Konuşmacının önünden grafik geçirmek yerine z-order/yolları düzelt.
- Konuşulan sayıları tam niteleyicileriyle göster: “2–3 ay”, “3 ya da 4 proje”.
  Bunları kesin “3 ay”, “4 proje” yapma; tasarruf cümlesine sahte yüzde/para
  ekleme. Sayısal vurgu büyük ve kısa; tekrarlanan başlık/paragraf değildir.
- Gerçek teknoloji logoları zorunludur; `../SKILL.md` üzerinden
  `poyraz-tech-logos` modülünü uygula. İlgisiz markaları süs olarak ekleme.
- Planın kapsam tablosunda start/end, söz/kelime onset, nesne, önceki→yeni
  anlam, kamera pozu, gerçek logo ve sayı, giriş/çıkış ile güvenli alan bulunur.
  4s'den uzun durağan/grafiksiz aralıkları ayrıca gerekçelendir (korunmuş CTA,
  son veda, duygusal vurgu vb.). Amaç bütün ekranı kalabalıklaştırmak değil,
  anlamı görünür ve sürekli tutmaktır.
- Revizyonda kullanıcının onayladığı sponsor/gövdeyi kilitle. Önce önceki
  kaynak/kurgunun hash ve dosya yedeğini al; yalnız izinli pencereleri değiştir.
  Korunmuş sahne kaynakları, kamera pozları, zamanlar ve audio etiketlerini
  karşılaştır; finalde aynı zamanlardaki kareleri de kontrol et.

## Giriş/çıkış ayracı — siyah boşluk (Poyraz standardı, 3 Ekim 2026)

Tek dosyada giriş ve çıkış birlikte geliyorsa, ikisinin arasındaki **gerçek cut noktasına
0.5s sessiz siyah boşluk** ekle. Amaç: kullanıcı uzun videoyu montajlarken giriş ile çıkışı
timeline'da tek bakışta ayırabilsin.

- Cut noktasını transkript (son giriş kelimesi / ilk çıkış kelimesi) + kare farkı + ses
  zarfıyla bul; sessiz kareye, kareye hizalı koy. Heceyi kesme.
- Boşluk tam siyah (#000) ve tam sessiz: konuşma, müzik ve SFX yok. Müziği iki klibe böl,
  her biri kendi fade'iyle bitsin/başlasın. Grafik ve kamera geçişi boşluğa taşmaz:
  giriş sahnesi cut'ta sert biter, çıkış tam kadrajla açılır.
- Video/ses iki klip olarak `data-media-start` ile aynı kaynaktan çalınır; kaynak zamanı
  ve çıktı zamanı ayrı tutulur (çıktı = kaynak + boşluk, cut sonrası). Plan kaynak zamanında
  yazılır, `sectionGap` alanına kaydedilir; SFX/CTA zamanları çıktıya eşlenir.
- Encoded MP4'te blackdetect ile boşluğun tam başlangıç/süresini ve volumedetect ile
  sessizliğini doğrula; VERIFY.md'ye yaz.
- Ayrı dosyalarda gelen giriş ve çıkış için gerekmez; tam uzun videoda (gövde dahil) yalnız
  kullanıcı isterse.

## Kısa tam ekran görsel ara sahne (`takeover`)

Birden çok şeyin ilişkisini göstermek yüz yanında zorlaşınca kullanılabilir.
Genellikle 3–6s ve seyrek; konuşmacının önemli kişisel/sponsor/veda anını örtme.
Konuşma kesintisiz sürerken kişi tamamen gizlenir, beyaz zeminli tek açıklama
dünyası gelir. Tek ana fikir: ör. seçilen içerik → öneri zincirinde kaybolma.
Başlık kartı değil; nesneler bir eylem ve sonuç gösterir. Temsili arayüz gerçek
ürün ekran görüntüsü diye sunulmaz. Metinsiz anlatım yeterliyse metin ekleme.

Zemin ve grafik tek deterministik zaman fonksiyonuyla yönetilir. Kişi geri
görünürken merkezdeki nesneler çoktan çekilmiş olmalı. Giriş/çıkışı `.5–.65s`
yumuşak curve ile bağla; çıkışın sonunda gecikmiş ikinci shrink, clip reset veya
flash olmasın. Her iki sınırın tamamını encoded ardışık karelerle incele.

## CTA ve sponsor

Kaynakta gömülü CTA varsa koru, üstüne ikinci CTA koyma. Kullanıcı CTA istediyse
ve kaynakta yoksa sözle eşleşen yeni CTA yapılabilir; bunu protectedIntervals
ile karıştırma. Beğen/abone sözlerinde alt-sol veya güvenli alt bantta tek sade
beyaz panel, kırmızı buton, küçük basılma/geri gelme hareketi. Kafayı/altyazıyı
örtmesin, gövdenin ortasını büyük panelle kapatmasın. En geç vedanın içinde çıkar;
son dostça bakışı temiz bırak. Zil, konfeti veya sayaç yağmuru varsayılan değil.
Çıkış özeti ve fayda anlatımı boyunca graph/ürün/sonuç dünyası gelişmeye devam
eder. “CTA bölümü” diye tüm çıkışı tek abone paneliyle veya boş bırakma.
Kupon, yüzde ve link yalnız konuşmada doğrulanmış bilgiden gelir; gerçek URL yoksa
URL uydurmak yerine gerekirse küçük aşağı yön işaretiyle yetin.

## Ses ve teslim

delivery.md'nin ses/miks/encoded QA kuralları aynıdır. İntro/outro için daha sakin
ritim; her harekete ses koyma. Kullanıcının müzik/SFX klasörünü kullan, müziği
ölçerek konuşmanın arkasına yerleştir, voice carve uygula. İlk giriş ve son veda
fade'leri; tek dosyada birbirine değen intro/outro için kesintisiz bed olabilir.
Tam videonun gövdesine müzik taşırma. İki bağımsız teslim istenmişse her parçanın
kendi başlangıç/bitiş fade'i olmalı.

Kontroller: bütün kelimeler/süre korunmuş; side objeler peak pozunda yüz/elleri
örtmüyor; takeover sırasında kaynak sesi sürüyor; geri dönüşte merkez temiz;
CTA gerçekten söylenen anda; müzik/SFX duyulur ama baskın değil; siyah/boş frame
yok. Strict HyperFrames check, gerçek MP4 hero/transition kareleri, kaynakla final
ASR karşılaştırması, loudness/true peak, SHA256 ve VERIFY.md. Final MP4'ü sun;
proje/transkript/plan yerelde kalsın. Kapaksız yatay çıktı eksik teslim değildir.
