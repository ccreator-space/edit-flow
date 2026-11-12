# Onaylı stil ve hareket sözleşmesi

## Gözle doğrulanan referans

`assets/approved-style.jpg` son onaylanan videonun dokuz karelik özetidir.
Kıyafet/yüz/konu/sponsor yeniden kullanılacak varlıklar değildir. Yeni girişten
çıkan nesneler konuya göre değişir; burada görülen sadelik, büyüklük, ışık ve
yerleşim dili korunur. Tam boy/transition referansı gerekirse approved-reference.md.

## Açılış: insan ana odak

Kısa açılış genellikle 3–6s: ilk kavramda beyaz alana geç. İlk karede anlamlı
bir eylem başlayabilir; tam ekran 3D bumper varsayılan değildir.
Son kullanıcı revizyonu: monitoring referansındaki objeler hâlâ küçük.
1080px tuvalde açılış ana silueti yaklaşık 550–700px, beyaz alandaki ana nesne
veya bütün ilişkili grup yaklaşık 740–880px genişlikten denenir. Bunlar güvenlik
kontrolünün yerine geçmez: yüz/altyazı veya sağ platform kontrolleriyle çakışırsa
oranlı küçült/yeniden yerleştir. Eski scale değerine her işte tekrar yüzde ekleme;
tam büyüklükteki gerçek piksel sınırına göre kalibre et.

Genellikle göğsün alt tarafındaki güvenli boşluk uygundur. Kafanın üstüne
nesne koymak ancak o anda gerçekten yeterli boşluk varsa mümkündür. Altyazı
kutusuna, yüze, ağıza veya CTA'ya taşma yok. Kağıt üzerinde sabit safe zone'a
güvenme: söz değiştikçe altyazı genişliği ve el hareketleri değişir. Açılışta
küçük punch-in kullanılabilir ama yüz/altyazı güvenliğini bozmaz.

## Beyaz açıklama sahnesi

Onaylı 1080×1920 başlangıç geometrisi:

- Tam boy çalışma videosu 1080×1920, anchor/origin (540,960).
- Üst konuşmacı ölçeği `.8`, düşey translate `-340`, merkez y=620.
- Dış crop penceresi altından 910px kırpar, görünür alt kenar y=1010.
- 2160×3840 kaynakta bu `.4` fiziksel ölçeğe eşdeğerdir; kaynak genişliğini
  dikkate almadan `.4` CSS ölçeği uygulamak kişiyi gereğinden fazla küçültür.
- Grafik alanı yaklaşık x=90..940, y=1100..1730. Telefon arayüzü için özellikle
  en altı ve sağ kenarı rahat bırak. Kafa ve altyazı üst panelde görünür kalır.

Bu değerler **başlangıç kalibrasyonu**; yeni yüz/altyazı farklıysa ayarlanır.
Kaynak yalnız transform nedeniyle kesilmez, zaman akışı değişmez. İlk/son
pozu ve ortadaki kareleri görünce karar ver. Yeni arka plan saf beyaz #ffffff.
Kullanıcı yüzünü arka plandan ayırmayı istemedi: otomatik segmentasyon, blur
dolgusu veya kaynak odanın yerine yapay arka plan ekleme.

## Malzeme ve kontrast

- Ana zemin `#ffffff`; gümüş gövde baz rengi `#7e899b`; grafit çizgi `#253040`;
  koyu ekran `#141820`; vurgu kırmızı `#ef3340`.
- Bunlar Three.js albedo değerleridir, çıktı pikseliyle aynı renk değildir.
  Yumuşak yönlü key/fill/rim ışığı ve ACES altında çıktıyı görerek ayarla.
- Beyaz üstündeki halo, bağlantı, halka/gauge ve ince çizgiler grafit olur.
  Koyu ekranın üzerindeki açık grafik çizgisini koyultma. Aynı material bütün
  nesnelerde paylaşılıyorsa körlemesine mutate etme; tema için clone kullan.
- Gerçek kalınlık, chamfer/yuvarlak kenar, kontrollü metal/roughness, sınırlı
  highlight. Çok parlak plastik oyuncak, neon glow, yoğun cam kart yığını yok.
- Kırmızı hata/eşik/önemli temas/sonuç gibi az sayıdaki vurucu noktada. Her
  yüzeyi kırmızı yapma. Yazıyla anlatmak yerine modelin durumunu değiştir.

## Motion designer gibi düşün

Bir hareketin öznesi, hedefi ve sonucu olsun. Modelin yerleşmesi, parçaların
takılması, bağlantının tamamlanması veya eşik çizgisinin aşılması anlam taşır.
Nesne ekrana gelir, mesaj okunur, başka duruma geçer, uygun anda çekilir.
İlgisiz her objeyi aynı y-sinusuyla yüzdürme. Süreyi dolsun diye hareket ekleme.
Önemli kavramı kelime zamanı tetikler; indeks tabanlı rastgele stagger değil.

Varsayılan girişler .4–.7s, sahneler arası küçük obje çıkışları yaklaşık .35s;
karakter duruşuna uygun sakin ease. İç animasyonlar ve CTA korumaları değişmez.
**Üstten tam ekrana dönüşte** hem kişi hem son alt dünya .65s `power2.inOut`
ile aynı başlangıç/bitişi paylaşır. Grafik .30s bekleyip .35s içinde yok olamaz.
Yanlış desen: video `end-.65`te, objeler `end-.35`te başlıyor. Doğru desen:
aynı progress ile kişinin scale .8→1 / y -340→0, crop 910→0, objeler 1→0.

`assets/motion.mjs` bunun saf-zaman fonksiyonlarını sağlar. Sadece problemin
mekaniğini yeniden kullan; yeni videonun splitWindow'larını plandan belirle.
`splitAmount` hem giriş/çıkış için source wrapper pozunu üretir;
`objectEnvelope(..., {exitDuration: .65, exitEase: power2InOut})` son alt
dünyanın scale'ine uygulanır. Ara nesnelerin onaylı giriş/çıkışları bağımsızdır.

## Teknik uygulama

Bir composition root, tek kayıtlı paused GSAP timeline, açık gerçek duration;
local GSAP/Three.js + importmap, muted video ve ayrı ses katmanları. Root ve
ancestor boyutları açık. Kaynak zamanı HyperFrames'e aittir; `video.currentTime`
elle sürülmez. Clip görünürlüğünü framework yönetir. Nesneler için `renderAt(t)`
her poz/material/visibility değerini t'den hesaplar; önceki kareye bağlı state,
timer, RAF, unseeded random ve biriken delta yok. Three.js hf-seek adapter'ını
kullan; preview ve render yolları aynı renderAt'a ve aynı composition time'a
gitmeli. İki ayrı bağımsız saat veya yarışan transform tween'leri oluşturma.

Scale + crop nested wrapper'larda birlikte kullanılacaksa aynı progress'i kullan
ve gerçek encoded karelerde kanıtla; alternatif mask refactor'ü de pozları
korumalıdır. Seek'leri sıra dışı dene (ileri, geri, aynı zaman): aynı t aynı
kareyi üretmeli. Büyük crop + scale değişimleri sürücü/GPU altında ayrıca sınanır.

Yalnız generic DOM layout check'iyle canvas'ın doğru olduğuna hükmetme. Registry
uygun model sağlamıyorsa yerel procedural Three.js geometri güvenilir fallback.
Final render native kaynak veya yeterli kaliteli türevi kullanır; düşük kalite
önizleme proxy'sini fark etmeden final kaynak yapma. Proxy GOP'u kısa tutulabilir,
ancak source timeline ve A/V eşlemesi yeniden doğrulanır.
