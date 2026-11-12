# Poyraz Reels skill doğrulaması — 12 Eylül 2026

- Paket: `skill-packages/poyraz-reels/`; kişisel kayıt
  `~/.codex/skills/poyraz-reels` aynı pakete symlink.
- Creator `quick_validate.py`: paket ve kişisel kayıt üzerinde geçti.
- `test_reel_tools.py`: dört test grubu geçti. 15 bozuk plan, üç bozuk
  transkript ve üç yanlış çıktı parametresi negatif kontrolü reddedildi.
  Gerçek 3s H.264/AAC fixture probe ve stream doğrulaması geçti.
- `test_motion.mjs`: iki .65s dönüşte 2.002 örnekte ortak eğri eşleşmesi,
  monotonic çıkış, uç pozlar, geçersiz window ve eski gecikmeli çıkış negatif kontrolü geçti.
- `transcribe_local.py`: mevcut large-v3 modeliyle kullanıcı videosunun
  76,18s'den başlayan 1,9s ses türevini yerelde çözümledi. Çıktı:
  “O zaman görüşmek üzere.”; dört kelimenin zamanları ham JSON'da.
  Yeni model indirilmedi, API veya cloud upload kullanılmadı.
- Genel çıktı verifier'ı daha önce teslim edilen finalde de geçti:
  1080×1920,30fps,2419 kare,80,633333s; hash mevcut final ile aynı.
- Referans stil görseli onaylı contact sheet'in kopyası; mevcut videonun
  görüntüsü, sesi veya kaynak kompozisyonu bu skill görevinde değiştirilmedi.
- Bu testler yardımcıların yapısını/işleyişini doğrular. Yeni bir farklı
  videonun uçtan uca yaratıcı editi bu görevde yapılmadı. Skill her gerçek
  editte görsel/encoded geçiş/ses incelemesini yeniden zorunlu tutar.
