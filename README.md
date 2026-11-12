# edit-flow

> Ham video → yayına hazır edit. Claude Code + HyperFrames ile çalışan, yapay zekâ destekli kişisel video edit akışım.

Bu repo, YouTube videolarımı ve Reels'lerimi editlediğim çalışma alanının kendisi. Ham kaydı veriyorum; transkript, sessizlik/hata kesimi, hikâye akışı, kelime senkronlu altyazı, 3D objeli yan paneller, ses miksi ve render adımları skill'ler üzerinden yürüyor. Kod yerine **HTML + GSAP** ile kompozisyon yazılıyor, [HyperFrames](https://github.com/heygen-com/hyperframes) bunu kare kare MP4'e çeviriyor.

Videoda anlattığım akışın tamamı burada. Kendi kanalına uyarlamak için fork'layabilirsin.

---

## Akış

```
 ham video ──► transkript ──► sessizlik + hata kesimi ──► STORY.md (hikâye omurgası)
                                                              │
     render ◄── check (lint/layout/kontrast) ◄── HyperFrames kompozisyonu ◄┘
       │
       └──► kapaklar · başlıklar · açıklama (yayın paketi)
```

1. **Transkript** — kelime zamanlı (yerel faster-whisper ya da ElevenLabs).
2. **Temizlik** — ölü boşluklar ve tekrar çekimler transkriptten bulunup kesilir.
3. **Hikâye** — `STORY.md`: videonun omurgası ve her bölümün görsel akışı. Konuşmayı tekrar eden chip/başlık yok; anlatılanı adım adım kuran, oklarla bağlı büyük objeler var.
4. **Kompozisyon** — HyperFrames HTML: yan panel, beyaz sayfa + PIP, tam kadraj gibi karışık sahne düzenleri.
5. **Ses** — müzik konuşmanın en az 13 dB altında, konuşmada ducking.
6. **Kontrol + render** — `npm run check` ile lint, layout, hareket ve kontrast kontrolü; ardından MP4.

## Klasörler

| Klasör | Ne var |
|---|---|
| `skill-packages/poyraz-reels/` | Ana edit skill'i: Reels (9:16) ve 16:9 giriş/çıkış editleri, altyazı, hikâye akışı, teslim kuralları |
| `skill-packages/poyraz-tech-logos/` | Konuşmada geçen teknolojilerin gerçek logolarını bulup zamanlayan skill |
| `.agents/skills/` | Genel edit skill'leri: sessizlik kesme, hata kesme, short-form, storytelling, beat senkron |
| `style-library/` | Hazır görsel stiller (token + kart bileşenleri) |
| `style-templates/` | Başlangıç kompozisyon şablonları |
| `scripts/` | Transkript dönüştürme, preflight, beat doğrulama, EDL inceleme araçları |
| `docs/` | Kurulum, iş akışı, API anahtarları, short-form ve doğrulama rehberleri |
| `CLAUDE.md` / `AGENTS.md` | Ajanın kuralları: hangi skill ne zaman, kapak ve edit standartları |
| `MOTION_PHILOSOPHY.md` | Hareket tasarımı ilkeleri |

## Repoda olmayanlar (bilerek)

Bu repo public; kişisel dosyalar `.gitignore` ile dışarıda tutuluyor ve her makinede ayrıca konuyor:

- `assets/input/` — ham çekimler
- `assets/identity/` — kapak üretimi için yüz referans fotoğrafları
- `video-projects/` — her videonun proje klasörü ve render çıktıları
- `Ses Efektleri/` — müzik ve efektler (lisansları kişisel)
- `.claude/skills/` — Higgsfield skill'leri ([higgsfield-ai/skills](https://github.com/higgsfield-ai/skills) üzerinden kurulur, sürümler `skills-lock.json`'da)
- `.env*`, `node_modules/`, cache'ler

## Kurulum

Gerekenler: Node.js 22+, FFmpeg, Python 3.11+ (yerel transkript için), [Claude Code](https://claude.com/claude-code).

```bash
git clone https://github.com/ccreator-space/edit-flow.git
cd edit-flow
npm install
npx hyperframes skills update
```

Kişisel skill'leri Claude Code'a bağla:

```bash
mkdir -p ~/.claude/skills
ln -s "$PWD/skill-packages/poyraz-reels" ~/.claude/skills/poyraz-reels
ln -s "$PWD/skill-packages/poyraz-tech-logos" ~/.claude/skills/poyraz-tech-logos
```

API anahtarları ve Vault klasörü için `.env.example`'ı `.env` olarak kopyala ve doldur (`.env` repoya girmez). Ayrıntılar: [docs/TOOLS-AND-API-KEYS.md](docs/TOOLS-AND-API-KEYS.md).

Yeni bir makinede son adım: ham videoyu `assets/input/` içine, yüz referanslarını `assets/identity/` içine, müzikleri `Ses Efektleri/` içine kopyala (ben Drive'dan çekiyorum).

## Kullanım

Claude Code'u klasörde aç ve videoyu ver:

```
assets/input/VideoAdi.mp4 bu videoyu editle
```

Reels için `/poyraz-reels`, genel HyperFrames işleri için `/hyperframes` ile başlanır.

```bash
npx hyperframes preview --background   # Studio önizleme
npm run check                          # lint + layout + kontrast
npm run render                         # MP4
```

## Teşekkür ve lisanslar

- [HyperFrames](https://github.com/heygen-com/hyperframes) (Apache-2.0) — HTML'den video render motoru
- [GSAP](https://gsap.com) — animasyon
- Başlangıç kiti ve stil kütüphanesi: [STUDENT_KIT_THIRD_PARTY_NOTICES.md](STUDENT_KIT_THIRD_PARTY_NOTICES.md), [licenses/](licenses/)

Benim yüzüm, sesim ve görüntülerim bu repodaki örnek görsellerde yer alabilir; bunlar yalnızca referanstır, yeniden kullanım izni vermez.

---

[Poyraz Avsever](https://github.com/poyrazavsever)
