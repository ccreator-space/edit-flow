#!/usr/bin/env python3
import copy
from pathlib import Path
import subprocess
import tempfile
import unittest
from reel_tools import probe, validate_plan, verify_output


def fixture():
    transcript = {'sourceSha256': 'a'*64, 'words': [{'text': 'örnek', 'start': 0, 'end': .4}]}
    plan = {'fps': 30, 'width': 1080, 'height': 1920, 'sourceSha256': 'a'*64,
            'contentEndFrame': 1500, 'coverFrames': 60, 'captionMode': 'embedded',
            'protectedIntervals': [{'start': 44, 'end': 50, 'reason': 'CTA'}],
            'splitWindows': [{'start': 12, 'end': 42, 'transition': .65}],
            'scenes': [
                {'id': 'opening', 'start': 0, 'end': 12, 'layout': 'full', 'reason': 'Context',
                 'actions': [{'wordIndex': 0, 'at': 0, 'object': 'object', 'motion': 'connect', 'outcome': 'connection'}]},
                {'id': 'explanation', 'start': 12, 'end': 42, 'layout': 'split', 'reason': 'Explain', 'actions': []},
                {'id': 'cta', 'start': 42, 'end': 50, 'layout': 'full', 'reason': 'CTA', 'actions': []},
                {'id': 'cover', 'start': 50, 'end': 52, 'layout': 'cover', 'reason': 'Cover', 'actions': []}]}
    return plan, transcript


class PlanTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(validate_plan(*fixture()), [])

    def test_coverless_requires_documented_reason(self):
        plan, transcript = fixture()
        plan['coverFrames'] = 0
        plan['scenes'].pop()
        self.assertTrue(validate_plan(plan, transcript))
        plan.update(coverMode='not-provided', coverReason='No image supplied; coverless output disclosed.')
        self.assertEqual(validate_plan(plan, transcript), [])
        plan['coverMode'] = 'invented-cover'
        self.assertTrue(validate_plan(plan, transcript))

    def test_negative_controls(self):
        mutations = [
            lambda p: p.update(sourceSha256='b'*64),
            lambda p: p['scenes'][1].update(start=12+1/30),
            lambda p: p['scenes'][1].update(start=11.9),
            lambda p: p['scenes'][0]['actions'][0].update(wordIndex=9),
            lambda p: p['scenes'][0]['actions'][0].update(at=2),
            lambda p: p['scenes'][0]['actions'][0].update(outcome=''),
            lambda p: p['scenes'][-1].update(end=51.9),
            lambda p: p['scenes'].pop(),
            lambda p: p['splitWindows'][0].update(end=45),
            lambda p: p['splitWindows'][0].update(transition=20),
            lambda p: p['protectedIntervals'][0].update(start=40),
            lambda p: p['scenes'][2].update(actions=[{'at': 45}]),
            lambda p: p.update(fps=float('nan')),
            lambda p: p.update(coverFrames=-1),
            lambda p: p.update(captionMode='duplicate'),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(index=index):
                plan, transcript = fixture(); mutate(plan)
                self.assertTrue(validate_plan(plan, transcript))

    def test_transcript_boundaries(self):
        for word in [{'text': 'x', 'start': -.1, 'end': .4},
                     {'text': 'x', 'start': 49, 'end': 51},
                     {'text': '', 'start': 0, 'end': .4}]:
            plan, transcript = fixture(); transcript['words'] = [word]
            self.assertTrue(validate_plan(plan, transcript))

    def test_landscape_mode(self):
        plan, transcript = fixture()
        plan.update(mode='landscape-intro-outro', width=1920, height=1080,
                    contentScope='intro-outro-only', coverFrames=0,
                    coverMode='not-applicable', coverReason='Landscape, no cover requested',
                    splitWindows=[], protectedIntervals=[],
                    editWindows=[{'start':0,'end':24,'role':'intro'}, {'start':24,'end':50,'role':'outro'}])
        plan['scenes'].pop()
        plan['scenes'][1]['layout']='takeover'
        self.assertEqual(validate_plan(plan, transcript), [])
        for mutate in [lambda p: p.update(width=1080),
                       lambda p: p.update(editWindows=[]),
                       lambda p: p['editWindows'][0].update(end=20),
                       lambda p: p['editWindows'][1].update(start=23),
                       lambda p: p['scenes'][1].update(layout='split'),
                       lambda p: p.update(contentScope='all')]:
            wrong=copy.deepcopy(plan); mutate(wrong)
            self.assertTrue(validate_plan(wrong, transcript))
        plan['contentScope']='full-video-with-protected-body'
        plan['editWindows']=[{'start':0,'end':12,'role':'intro'}, {'start':42,'end':50,'role':'outro'}]
        self.assertTrue(validate_plan(plan, transcript))
        plan['scenes'][1]['layout']='full'
        self.assertEqual(validate_plan(plan, transcript), [])

    def test_real_encoded_media(self):
        with tempfile.TemporaryDirectory(prefix='poyraz-reels-test-') as folder:
            video = Path(folder)/'fixture.mp4'
            subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', 'color=white:s=108x192:r=30:d=3',
                            '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-t', '3',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                            '-movflags', '+faststart', str(video)], check=True)
            info = probe(video)
            self.assertEqual(len(info['sha256']), 64)
            plan = {'width': 108, 'height': 192, 'fps': 30, 'contentEndFrame': 30, 'coverFrames': 60}
            self.assertTrue(verify_output(video, plan)['ok'])
            for key, value in [('width', 110), ('fps', 24), ('coverFrames', 59)]:
                wrong = copy.deepcopy(plan); wrong[key] = value
                self.assertFalse(verify_output(video, wrong)['ok'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
