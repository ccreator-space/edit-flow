# Reels editing workspace

Bu klasör 1080 × 1920 dikey HyperFrames projeleri için hazırlandı.

## Her yeni Reels için

Onaylı kişisel format için kesilmiş videoyu ve kapağı gönderip `$poyraz-reels`
yazman yeterli. Kaynak skill: `skill-packages/poyraz-reels/SKILL.md`.

1. Kaynak ve kapak doğrulanır; konuşmanın kelime zamanlı ve cümle cümle transkripti alınır.
2. Her cümle için nesne, hareket, yerleşim, güvenli alan ve ses planı dosyaya yazılır.
3. Mevcut kesmeler, altyazı ve CTA korunarak minimal 3D edit uygulanır.
4. İlk bölüm tam konuşmacı; açıklamalarda beyaz zemin, üst konuşmacı ve altta ilgili objeler.
5. Ses ve sonda 2 saniyelik kapak tamamlanır; teknik ve encoded kare kontrollerinden
   sonra final MP4 teslim edilir. Kullanıcı ayrıca istemedikçe plan onayı için beklenmez.

Farklı bir edit tarzı veya yalnız plan istenirse o talimat önceliklidir.

## Yararlı komutlar

```bash
npm run dev
npm run check
npm run render -- --quality high --output renders/final.mp4
npm run validate:short-form -- <project-directory>
npm run validate:footage -- <project-directory>
npm run validate:beats -- <project-directory>
npm run preflight -- <project-directory>
```

## Student Kit eklentileri

Student Kit'ten yalnızca güncel resmi HyperFrames kurulumu ile çakışmayan
editoryal parçalar alınmıştır. Reels için `short-form-edit`; tam konuşmacı
kurgusu için `edit-video`; tek işlem için `cut-silences` veya `cut-mistakes`
kullanılır. `style-library/registry.json` içinde 406 taslak kart vardır.
Kartların metinleri ve örnek marka öğeleri yayın öncesinde değiştirilir;
seçilen kart güncel HyperFrames kontrolünden geçirilmeden teslim edilmez.

HeyGen’in ücretsiz medya/TTS kataloğu için bir defalık kullanıcı girişi gerekir:

```bash
heygen auth login --oauth
```

Türkçe transkripsiyonda dil açıkça seçilmelidir; İngilizceye özel `.en` modelleri kullanılmaz.
