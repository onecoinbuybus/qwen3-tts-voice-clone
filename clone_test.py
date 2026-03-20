#!/usr/bin/env python3
"""Voice Cloning test: clone a voice from a reference audio file."""
import os
import shutil
import subprocess
import warnings

os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

from mlx_audio.tts.utils import load_model
from mlx_audio.tts.generate import generate_audio

script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "models", "Qwen3-TTS-12Hz-1.7B-Base-8bit")

print("Loading Base model...")
model = load_model(model_path)

ref_audio = os.path.join(script_dir, "voices", "reference.wav")
ref_text = "这里填写参考音频对应的文本内容"

text = "你好，这是一个语音克隆的测试！"
output_path = os.path.join(script_dir, "clone_output")

print(f"Generating: {text}")
generate_audio(
    model=model,
    text=text,
    ref_audio=ref_audio,
    ref_text=ref_text,
    lang_code="zh",
    output_path=output_path,
)

result_file = os.path.join(output_path, "audio_000.wav")
if os.path.exists(result_file):
    final = os.path.join(script_dir, "outputs", "clone_test.wav")
    os.makedirs(os.path.join(script_dir, "outputs"), exist_ok=True)
    shutil.copy(result_file, final)
    print(f"Saved to: {final}")
    print("Playing...")
    subprocess.run(["afplay", final])
    shutil.rmtree(output_path, ignore_errors=True)
else:
    print("Error: no audio generated")
