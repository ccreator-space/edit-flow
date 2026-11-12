#!/usr/bin/env python3
"""Local, read-only media/plan checks. These do not certify taste or ASR accuracy."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def probe(path):
    path = Path(path).resolve(strict=True)
    info = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)
    ]))
    return {'path': str(path), 'sha256': sha256(path), **info}


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def validate_plan(plan, transcript):
    errors = []
    def require(ok, message):
        if not ok:
            errors.append(message)
    fps = plan.get('fps')
    if not number(fps) or fps <= 0:
        return ['fps must be positive']
    for key in ('contentEndFrame', 'width', 'height'):
        require(type(plan.get(key)) is int and plan[key] > 0, f'{key} must be a positive integer')
    cover_frames = plan.get('coverFrames')
    landscape = plan.get('mode') == 'landscape-intro-outro'
    cover_modes = ('not-provided', 'user-opt-out', 'not-applicable') if landscape else ('not-provided', 'user-opt-out')
    coverless = (type(cover_frames) is int and cover_frames == 0
                 and plan.get('coverMode') in cover_modes
                 and bool(plan.get('coverReason')))
    require((type(cover_frames) is int and cover_frames > 0) or coverless,
            'coverFrames must be positive, or zero with explicit coverMode and coverReason')
    if errors:
        return errors
    content_end = plan['contentEndFrame'] / fps
    end = (plan['contentEndFrame'] + plan['coverFrames']) / fps
    edit_windows = []
    if landscape:
        require(abs(plan['width']/plan['height']-16/9) < .01, 'Landscape mode requires 16:9 canvas')
        require(plan.get('contentScope') in ('intro-outro-only', 'full-video-with-protected-body'), 'Missing landscape contentScope')
        require(not plan.get('splitWindows'), 'Landscape mode does not use Reel split windows')
        last = 0
        for window in plan.get('editWindows', []):
            a, b = window.get('start'), window.get('end')
            valid = number(a) and number(b) and 0 <= a < b <= content_end
            require(valid and window.get('role') in ('intro', 'outro'), 'Invalid intro/outro edit window')
            if valid:
                require(a >= last, 'Edit windows overlap or are unordered')
                edit_windows.append((a, b)); last = b
        require(bool(edit_windows), 'Landscape edit windows missing')
        if plan.get('contentScope') == 'intro-outro-only':
            require(abs(sum(b-a for a,b in edit_windows)-content_end)<1e-5, 'Intro/outro-only windows must cover source')
    require(plan.get('sourceSha256') == transcript.get('sourceSha256') and bool(plan.get('sourceSha256')), 'Source hash mismatch/missing')
    require(plan.get('captionMode') in ('embedded', 'none', 'added'), 'Unknown captionMode')
    scenes, words = plan.get('scenes', []), transcript.get('words', [])
    require(bool(scenes), 'No scenes')
    require(bool(words), 'No transcript words')
    previous_word = -1
    for i, word in enumerate(words):
        a, b = word.get('start'), word.get('end')
        valid = number(a) and number(b) and 0 <= a <= b <= content_end + .001
        require(valid, f'Invalid word interval {i}')
        if valid:
            require(a >= previous_word, f'Unordered word {i}')
            previous_word = a
        require(bool(word.get('text', '').strip()), f'Empty word {i}')
    cursor, ids, cover_count = 0, set(), 0
    for i, scene in enumerate(scenes):
        sid = scene.get('id')
        require(bool(sid) and sid not in ids, f'Missing/duplicate scene id at {i}')
        ids.add(sid)
        a, b = scene.get('start'), scene.get('end')
        if not (number(a) and number(b) and 0 <= a < b <= end + 1e-5):
            errors.append(f'Invalid scene interval {sid}')
            continue
        require(abs(a-cursor) < 1e-5, f'Scene gap/overlap before {sid}')
        cursor = b
        layout = scene.get('layout')
        layouts = ('full', 'takeover', 'cover') if landscape else ('full', 'split', 'cover')
        require(layout in layouts, f'Unknown layout {sid}')
        if landscape and layout != 'cover' and (layout != 'full' or scene.get('actions')):
            covered = sum(max(0, min(b,y)-max(a,x)) for x,y in edit_windows)
            require(abs(covered-(b-a))<1e-5, f'Edited scene outside intro/outro: {sid}')
        require(bool(scene.get('reason')), f'Missing editorial reason {sid}')
        if layout == 'cover':
            cover_count += 1
            require(i == len(scenes)-1 and abs(a-content_end)<1e-5 and abs(b-end)<1e-5, 'Cover must be the final complete segment')
            require(not scene.get('actions'), 'No new graphic actions on cover')
        else:
            require(b <= content_end + 1e-5, f'Footage after content end: {sid}')
        for action in scene.get('actions', []):
            wi, at = action.get('wordIndex'), action.get('at')
            valid = type(wi) is int and 0 <= wi < len(words) and number(at)
            require(valid, f'Invalid word anchor {sid}')
            if valid:
                require(a <= at < b, f'Action outside scene {sid}')
                onset = words[wi].get('start')
                if number(onset):
                    require(-.15 <= at-onset <= .2 or bool(action.get('timingReason')), f'Unexplained timing offset {sid}')
            for key in ('object', 'motion', 'outcome'):
                require(bool(action.get(key)), f'Missing action {key}: {sid}')
    require(abs(cursor-end)<1e-5, 'Plan does not cover full delivery duration')
    require(cover_count == (0 if coverless else 1),
            'Closing cover count must match documented cover mode')
    valid_windows = []
    last_end = 0
    for window in plan.get('splitWindows', []):
        a, b, d = window.get('start'), window.get('end'), window.get('transition', .65)
        valid = all(number(v) for v in (a, b, d)) and 0 <= a < b <= content_end and d > 0 and b-a >= 2*d
        require(valid, 'Invalid split window')
        if valid:
            require(a >= last_end, 'Split windows overlap or are unordered')
            last_end = b
            valid_windows.append((a, b))
    for scene in scenes:
        a, b = scene.get('start'), scene.get('end')
        if not (number(a) and number(b)):
            continue
        covered = sum(max(0, min(b,y)-max(a,x)) for x,y in valid_windows)
        require(abs(covered-(b-a if scene.get('layout')=='split' else 0))<1e-5, f'Split window/layout mismatch: {scene.get("id")}')
    for interval in plan.get('protectedIntervals', []):
        a, b = interval.get('start'), interval.get('end')
        valid = number(a) and number(b) and 0 <= a < b <= content_end
        require(valid and bool(interval.get('reason')), 'Invalid protected interval')
        if valid:
            for scene in scenes:
                x, y = scene.get('start'), scene.get('end')
                if number(x) and number(y) and max(a,x) < min(b,y):
                    require(scene.get('layout')=='full' and not scene.get('actions'), 'Protected CTA must stay full and graphics-free')
    return errors


def verify_output(path, plan):
    info = probe(path)
    video = next((s for s in info['streams'] if s['codec_type']=='video'), None)
    audio = next((s for s in info['streams'] if s['codec_type']=='audio'), None)
    errors = []
    if video is None:
        return {'ok': False, 'errors': ['No video stream']}
    frames = plan['contentEndFrame'] + plan['coverFrames']
    fps = plan['fps']
    def rate(value):
        a, b = map(float, value.split('/'))
        return a/b if b else 0
    for key in ('width', 'height'):
        if video.get(key) != plan[key]:
            errors.append(f'{key} mismatch')
    if abs(rate(video['avg_frame_rate'])-fps)>1e-6 or abs(rate(video['r_frame_rate'])-fps)>1e-6:
        errors.append('FPS mismatch')
    if int(video.get('nb_frames', -1)) != frames:
        errors.append('Frame count missing/mismatch')
    if abs(float(video.get('duration', 0))-frames/fps)>1/fps/2:
        errors.append('Duration mismatch')
    if audio is None:
        errors.append('No audio stream')
    return {'ok': not errors, 'errors': errors, 'path': info['path'], 'sha256': info['sha256'],
            'frames': video.get('nb_frames'), 'duration': video.get('duration'),
            'limits': 'Technical stream checks only; inspect encoded cover, safe zones, motion and sound separately.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command', required=True)
    p = subs.add_parser('probe'); p.add_argument('input'); p.add_argument('--output')
    p = subs.add_parser('validate-plan'); p.add_argument('plan'); p.add_argument('transcript')
    p = subs.add_parser('verify-output'); p.add_argument('video'); p.add_argument('plan')
    args = parser.parse_args()
    try:
        if args.command == 'probe':
            result = probe(args.input)
            if args.output:
                with Path(args.output).open('x') as out:
                    json.dump(result, out, ensure_ascii=False, indent=2)
        elif args.command == 'validate-plan':
            errors = validate_plan(json.loads(Path(args.plan).read_text()), json.loads(Path(args.transcript).read_text()))
            result = {'ok': not errors, 'errors': errors}
        else:
            result = verify_output(args.video, json.loads(Path(args.plan).read_text()))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get('ok', True) else 1
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        print(json.dumps({'ok': False, 'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    sys.exit(main())
