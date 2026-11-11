"""Transcription helper tests. Stub modules stand in for the ASR dependencies."""
import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/transcribe.py"

CTRANSLATE2_STUB = """
import os
def get_cuda_device_count():
    return int(os.environ.get("STUB_CUDA_COUNT", "0"))
"""

FASTER_WHISPER_STUB = """
import os
from types import SimpleNamespace

class WhisperModel:
    def __init__(self, path, device, compute_type, local_files_only):
        assert local_files_only is True
        self.device = device

    def transcribe(self, media, language, **kwargs):
        def segments():
            if self.device == "cuda" and os.environ.get("STUB_CUDA_FAIL"):
                raise RuntimeError("libcudnn not found")
            yield SimpleNamespace(start=0.0, end=1.5, text=" hello ")
        return segments(), SimpleNamespace(language=language or "en")
"""


class InputTest(unittest.TestCase):
    def test_rejects_missing_media_and_uncached_model(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            media = root / "sample.wav"
            for expected in ("existing local file", "cached model directory"):
                result = subprocess.run(
                    [sys.executable, "-S", str(SCRIPT), str(media), "--model", str(root)],
                    capture_output=True, text=True,
                )
                self.assertEqual(result.returncode, 2)
                self.assertIn(expected, result.stderr)
                self.assertEqual(result.stdout, "")
                media.touch()


class StubbedRunTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        stubs = root / "stubs"
        (stubs / "faster_whisper").mkdir(parents=True)
        (stubs / "ctranslate2").mkdir()
        (stubs / "ctranslate2/__init__.py").write_text(textwrap.dedent(CTRANSLATE2_STUB))
        (stubs / "faster_whisper/__init__.py").write_text(textwrap.dedent(FASTER_WHISPER_STUB))
        self.model = root / "model"
        self.model.mkdir()
        (self.model / "model.bin").touch()
        self.media = root / "sample.wav"
        self.media.touch()
        self.stubs = stubs

    def tearDown(self):
        self.tmp.cleanup()

    def run_helper(self, *extra, **env):
        environment = {**os.environ, "PYTHONPATH": str(self.stubs), **env}
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(self.media), "--model", str(self.model), *extra],
            capture_output=True, text=True, env=environment,
        )

    def test_cpu_output_shape_and_language(self):
        result = self.run_helper("--language", "th")
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output["device"], "cpu")
        self.assertEqual(output["compute_type"], "int8")
        self.assertEqual(output["language"], "th")
        self.assertEqual(output["segments"], [{"start": 0.0, "end": 1.5, "text": "hello"}])

    def test_auto_uses_cuda_when_available(self):
        result = self.run_helper(STUB_CUDA_COUNT="1")
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual((output["device"], output["compute_type"]), ("cuda", "float16"))

    def test_auto_falls_back_when_cuda_fails_during_decode(self):
        result = self.run_helper(STUB_CUDA_COUNT="1", STUB_CUDA_FAIL="1")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("falling back to CPU", result.stderr)
        self.assertEqual(json.loads(result.stdout)["device"], "cpu")

    def test_explicit_cuda_does_not_fall_back(self):
        result = self.run_helper("--device", "cuda", STUB_CUDA_COUNT="1", STUB_CUDA_FAIL="1")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("libcudnn", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_explicit_cpu_with_compute_type(self):
        result = self.run_helper("--device", "cpu", "--compute-type", "float32", STUB_CUDA_COUNT="1")
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual((output["device"], output["compute_type"]), ("cpu", "float32"))


if __name__ == "__main__":
    unittest.main()
