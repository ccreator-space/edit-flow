#!/usr/bin/env python3
"""Local transcription, no upload; optional VAD preserves original source timestamps."""
import argparse
import json
import os
from pathlib import Path
from reel_tools import sha256


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    parser.add_argument('--output', required=True)
    parser.add_argument('--language', default='tr')
    parser.add_argument('--model', default='large-v3')
    parser.add_argument('--prompt', default='')
    parser.add_argument('--threads', type=int, default=8)
    parser.add_argument('--vad', action='store_true', help='For raw takes with long silence; faster-whisper restores original media timestamps.')
    parser.add_argument('--no-condition-previous-text', action='store_true', help='Reduce repeated hallucinations in raw takes and pauses.')
    parser.add_argument('--allow-download', action='store_true')
    args = parser.parse_args()
    source = Path(args.input).resolve(strict=True)
    target = Path(args.output).resolve()
    if target.exists():
        parser.error('Output already exists; keep raw ASR and use a new filename.')
    if not target.parent.is_dir():
        parser.error('Create the project assets directory first.')
    if not args.allow_download:
        os.environ['HF_HUB_OFFLINE'] = '1'
    from faster_whisper import WhisperModel
    model = WhisperModel(args.model, device='cpu', compute_type='int8',
                         cpu_threads=args.threads, local_files_only=not args.allow_download)
    segments, info = model.transcribe(str(source), language=args.language, beam_size=5,
                                     word_timestamps=True, vad_filter=args.vad,
                                     condition_on_previous_text=not args.no_condition_previous_text,
                                     initial_prompt=args.prompt or None)
    result = {'sourceSha256': sha256(source), 'sourcePath': str(source),
              'language': info.language, 'provider': f'faster-whisper {args.model} local CPU int8',
              'vad': args.vad, 'conditionOnPreviousText': not args.no_condition_previous_text,
              'segments': [], 'words': []}
    for segment in segments:
        row = {'start': segment.start, 'end': segment.end, 'text': segment.text.strip()}
        result['segments'].append(row)
        result['words'].extend({'text': w.word.strip(), 'start': w.start, 'end': w.end,
                                'probability': w.probability} for w in (segment.words or []))
        print(json.dumps(row, ensure_ascii=False), flush=True)
    with target.open('x') as out:
        json.dump(result, out, ensure_ascii=False, indent=2)
        out.write('\n')


if __name__ == '__main__':
    main()
