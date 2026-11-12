# Hikâye akışlı kurgu (Poyraz standardı, 2026-10-19)

Kanonik ve ayrıntılı not: `Vault/07 Edit System/Poyraz Edit Rehberi.md`
(Vault: `$POYRAZ_VAULT` ortam değişkeninin gösterdiği klasör; Drive'da `KişiselMarka/Thumbnails/Vault`).
Referans kareler `Vault/07 Edit System/Referanslar/akis-ornek-1..5.png`; kaçınılacak durum `anti-ornek-dokploy-2026-10-19.png`.
Bu dosya o notun operasyonel özetidir. Her 16:9 giriş/çıkış ve 9:16 Reels editinde, plan yazmadan önce ikisini de oku.

## Sıra

1. Transkript → **STORY.md** (şablon `Vault/04 Templates/Hikâye Planı.md`): 3–6 bölümlük omurga, her bölüm için
   girdi → eylem → sonuç akışı, adım tablosu (tetik kelime, obje, hareket, önceki→yeni durum, SFX), bölümler arası geçiş.
2. **Materyal İhtiyaç Listesi:** videoda geçen ama elde olmayan gerçek çıktılar (kullanıcının ürettiği reklamlar, ekran
   kayıtları, ürün/panel görüntüleri) ve hook için gereken ek çekimler (ör. siyah-beyaz flash-forward). Kullanıcıya **tek
   mesajda** iste: her maddede neden, hangi saniye, yoksa yedek plan. Beklerken transkript/plan/görsel/başlık/açıklama sürer;
   materyale bağlı sahneler en son biter. “Devam et” cevabında yedek plan uygulanır ve raporlanır. Bu, “ara onay isteme”
   kuralının tek istisnasıdır.
3. Görsel üretimi (stil ailesi tek), sonra EDIT-PLAN.md + build.

## Kurallar

- **Tekrar metni yasak:** konuşmayı yazan chip/pill/rozet/başlık/alt başlık/paragraf yok; “X'i inceliyorum” etiketi yok.
  Reels'te altyazı varken başka tekrar metni yok. İzinli: diyagramın parçası olan 1–3 kelimelik etiketler (klasör adı,
  ok altı durum), konuşmada geçen gerçek sayı/fiyat, kod, gerçek UI metni, konuşma balonunda tek replik.
- **Panel doluluğu:** konuşmacı yandayken karşı panelin %60–80'i dolu; 2–4 büyük, oklarla/çizgilerle bağlı obje.
  Tek obje ≥ panel genişliğinin ~%35'i (1920'de ≥ 380px). Boş panel en fazla ~1s (geçişte).
- **Adım adım inşa:** ana obje → ok çizilir (SVG draw-on) → ucunda yeni obje → kısa etiket → durum değişimi
  (hata→çözüm, kapalı→açık, gri→renkli, pin seçer). Bölüm biterken diyagram aşağı/yana kayar ya da bir objeye zoom
  yapılır; sıradaki akış o objeden doğar. Kesik kesik pop-in + kaybolma yerine sürekli kamera/sahne hareketi.
- **Kod:** kod örneği konuşulursa gerçek kod HTML'de (renkli, monospace) satır satır gelir, konuşulan satır büyür/
  vurgulanır. Yazılım konusu kodsuz anlatılsa bile uygun yerde kısa kod/terminal/gerçek UI akışı kullanılabilir.
- **Sahne düzenleri karışık:** yan panel (sağ/sol dikdörtgen) · beyaz sayfa + sağ üst küçük PIP (büyük diyagram) ·
  kısa tam beyaz sayfa (konuşmacı gizli, 3–6s) · tam kadraj + kenarlardan objeler · Reels üst/alt. Her zaman sağ/sol değil.
- **Stil:** videoda tek aile. Akış diyagramı varsayılanı referanslardaki temiz flat illüstrasyon/sticker objeler + el
  çizimi siyah oklar (oklar SVG ile kodda çizilir). 3D clay yalnız tek başına sahne taşıyan hero anlarında, flat ile
  aynı sahnede karışmaz. Gerçek logo/UI üretilmez.
- **Ses:** müzik ~−31 LUFS, carve ≥ .5, duck tabanı −6 dB; finalde konuşma müziğin ≥ ~13 dB üstünde (ölç, VERIFY.md).
  SFX hikâye olayına bağlı: ok çizimi swish, yerleşme/klasör açılma pop, doğru seçim ding, hata error.

## QA eklemeleri

- Her bölümün tam kurulu hâli ve her geçiş için encoded kare şeridi.
- Panel doluluk kontrolü (kurulu hâlde boş alan oranı).
- Tekrar metni taraması: ekrandaki metinleri transkriptle karşılaştır; konuşmayı yazan rozet kalmasın.

## Arayüz kullanılırken arayüz hep görünür (kullanıcı kuralı, 2026-11-09)

- Ekran kaydında Poyraz bir arayüzde (Higgsfield vb.) iş yapıyorsa (prompt, sol panel ayarları, model/süre/oran, Generate, sonuç) ekran kaydı tam kadraj, kırpılmadan, kalıcı zoom olmadan ana görüntüdür; sol panel ve ayarlar her an görünür.
- Bu anlara beyaz sayfa/diyagram/yan panel konmaz; kamera yalnız kullanılan bölgeyi örtmeyen küçük PIP. İzinli: seyrek kırmızı işaret, 2–3 s'de tam kadraja dönen kısa zoom.
- Beyaz sayfa/diyagram yalnız ekran kaydı boştayken (senaryo sayfası, değişmeyen ekran). Edit öncesi her saniye "aktif arayüz / boşta" diye sınıflanır; QA'da aktif aralıklardan kareler arayüzün tamamını göstermeli.
