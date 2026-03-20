#!/usr/bin/env python3
"""CustomVoice test: generate speech with a preset voice and style instructions."""
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
model_path = os.path.join(script_dir, "models", "Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit")

print("Loading CustomVoice model...")
model = load_model(model_path)

text = "你好，这是自定义语音测试！"
output_path = os.path.join(script_dir, "custom_output")

print(f"Generating: {text}")
generate_audio(
    model=model,
    text=text,
    voice="Ono_Anna",
    instruct="元気で明るい女の子、少し甘えた声で話す",
    speed=1.0,
    lang_code="ja",
    output_path=output_path,
)

result_file = os.path.join(output_path, "audio_000.wav")
if os.path.exists(result_file):
    final = os.path.join(script_dir, "outputs", "custom_test.wav")
    os.makedirs(os.path.join(script_dir, "outputs"), exist_ok=True)
    shutil.copy(result_file, final)
    print(f"Saved to: {final}")
    print("Playing...")
    subprocess.run(["afplay", final])
    shutil.rmtree(output_path, ignore_errors=True)
else:
    print("Error: no audio generated")
