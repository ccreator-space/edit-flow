# Onaylı yerel örnek

Referans proje bu skill oluşturulurken şurada bulunuyordu:
`video-projects/watchman-monitoring/` (repo köküne göre)

Referans final: `renders/watchman-monitoring-beyaz-final.mp4`
SHA-256: `b9e8541d7e9f573289c7fe0402e27c5a3050a9735083d05efed3ff3090b38f02`
1080×1920 / 30fps / 80,633333s, son 2s kullanıcı kapağı.

Bu makinedeki yeniden kullanılabilir yerel ASR ortamı:
`~/.cache/video-editor/whisperx-venv/bin/python`.
Varsayılan `python3` bu paketi içermeyebilir. Yol/bağımlılık varlığını kontrol
et; başka makinede bu yolu zorunlu kabul etme. Kurulu large-v3 modeli varsa
skill'in transcribe_local.py script'i aynı ortamda indirimsiz çalışır.

İlk kez bu stile geçerken paketli `assets/approved-style.jpg` incelenir.
Hareketi daha ayrıntılı çözmek gerekirse ve proje varsa `index.html`, `scene.js`,
`frame.md`, `VERIFY.md` ve `qa/white-encoded-*-return.jpg` incelenir. Proje yoksa
yeniden indirmeye/upload'a gerek yok; bu skill'in stil ve motion tanımı yeterli.

## Kullanıcı onayından çıkan kararlar

1. İlk nesneler küçüktü: yalnız açılış grubu %28 büyüdü; nihai grup ölçeği
   .9'dan 1.152'ye geçti. Her yeni çalışmada tekrar %28 eklenmez.
2. Alt dünya siyah değil beyaz. Açık ince çizgiler grafit; gövdeler gümüş;
   koyu ekran üzerindeki metrik çizgileri açık kaldı. Yüz ve altyazı değişmedi.
3. Kişi .65s'de büyürken objeler .30s bekleyip .35s'de küçülüyordu. Objelerin
   çıkışı da aynı .65s cubic/power2.inOut eğrisine eşitlendi. İki encoded
   dönüş 24'er karede incelendi. Gelecek videolarda aynı regresyon engellenir.
4. Kullanıcının kendi CTA animasyonları, konuşmanın bütünlüğü, müzik/SFX miksi
   ve kapak korundu. Bu kişisel format için otomatik recut varsayımı yanlıştır.

Bu örnekteki teknoloji nesneleri (laptop, server, threshold/phone, globe,
CPU/RAM/SSD) konuya bağlıdır. Yeni video başka konudaysa farklı görsel metafor
kur; Watchman sponsorluğunu, kapak yazısını veya transcriptini taşımak yasaktır.

## Beceri keşfi notu

Skill authoring/discovery rehberi:
[OpenAI — Build skills](https://learn.chatgpt.com/docs/build-skills).
Yerel skill klasörü ve symlink'ler desteklenir; bu paket özel kullanıcı
medyası içeren yerel bir beceridir, yayın veya plugin marketplace yüklemesi değildir.
