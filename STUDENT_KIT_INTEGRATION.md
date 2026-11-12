# HyperFrames Student Kit integration

Source: `https://github.com/nateherkai/hyperframes-student-kit`

Reviewed commit: `b1afdb1dcbcad39dd27638ea699f132fe44ce6df`

## Included

- Seven project-local skills: `short-form-edit`, `edit-video`, `cut-silences`,
  `cut-mistakes`, `hyperframes-video-beats`, `video-storytelling`, and
  `style-library`.
- Short-form validators, preflight and beat-sync utilities.
- The 406-card style registry and two scene templates.
- Student Kit workflow documentation, motion philosophy, license, and notices.
- Local GSAP 3.14.2 package for dependency localization.

## Deliberately excluded

- The Student Kit's older `hyperframes@0.7.109` dependency and its bundled
  `hyperframes`, `hyperframes-cli`, and `hyperframes-registry` skill copies.
  This workspace remains pinned to the newer official `hyperframes@0.8.35`.
- Its standalone GSAP skill, because the current official
  `hyperframes-animation` contract is stricter about deterministic seek-safe
  timelines.
- Legacy `short-form-video`, `make-a-video`, and `website-to-hyperframes`
  workflows that overlap current official HyperFrames workflows.
- Approximately 385 MB of teaching/demo video projects and showcase media.
- AIS example brand assets, which are not licensed for reuse in personal work.

The integrated resources are reference and draft material. Current official
HyperFrames validation and review rules always win.
