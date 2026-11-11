# Local transcription setup

The helper uses [Faster Whisper](https://github.com/SYSTRAN/faster-whisper).
Use an isolated Python environment. Install dependencies only when setup is
within the user's authorization:

```bash
python -m venv "<environment-directory>"
"<environment-python>" -m pip install faster-whisper
```

Download a model separately, before processing private media. This fetches
model files; it does not upload a recording:

```bash
"<environment-python>" -c "from faster_whisper.utils import download_model; download_model('tiny', output_dir='<model-directory>')"
```

Choose a model appropriate to the language and accuracy needed. `tiny` is a
small multilingual smoke-test model. Larger models can improve quality and use
more memory and time. Model downloads need network access and disk space; do
not start them silently when the task forbids network access or installation.

Then run the helper with that environment's Python and the cached directory:

```bash
"<environment-python>" scripts/transcribe.py "<local-media>" --model "<model-directory>" --language en > "<temporary-directory>/transcript.json"
```

With `--device auto` (default) the helper uses CUDA float16 when a GPU is
visible. If loading or decoding on CUDA fails, for example on missing cuDNN or
cuBLAS libraries, it warns on stderr and reruns on CPU INT8. `--device cuda`
fails instead of falling back. `--compute-type` overrides the precision for the
selected device. The helper passes `local_files_only=True`.
It does not use an API key, select a cloud backend, download a model during
transcription, or open a player. It is not a network sandbox for arbitrary media
or dependencies. Process only authorized files with current decoder packages.
