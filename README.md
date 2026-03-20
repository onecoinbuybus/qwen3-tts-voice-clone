# Qwen3-TTS Voice Clone

基于 [Qwen3-TTS](https://huggingface.co/Qwen/Qwen3-TTS) + [MLX](https://github.com/ml-explore/mlx) 的本地语音克隆工具，专为 Apple Silicon Mac 优化。

用一段参考音频克隆任意声音，生成中文语音。支持与 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 集成，实现任务完成后自动语音播报。

## 功能

- **Voice Cloning** — 用参考音频克隆声音，生成任意中文文本的语音
- **CustomVoice** — 用预设声音 + 风格指令生成语音（无需参考音频）
- **Claude Code 集成** — 任务完成自动语音播报 + 权限确认提示音

## 硬件要求

- Apple Silicon Mac（M1/M2/M3/M4）
- 建议 16GB+ 内存（8bit 量化模型约需 2-3GB）
- 测试环境：M4 MacBook Air 32GB

## 安装

### 1. 克隆仓库

```bash
git clone https://github.com/<YOUR_USERNAME>/qwen3-tts-voice-clone.git
cd qwen3-tts-voice-clone
```

### 2. 创建虚拟环境

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 安装 ffmpeg

```bash
brew install ffmpeg
```

### 5. 下载模型

```bash
mkdir -p models
# Voice Cloning（Base 模型）
huggingface-cli download Qwen/Qwen3-TTS-12Hz-1.7B-Base-8bit --local-dir models/Qwen3-TTS-12Hz-1.7B-Base-8bit

# CustomVoice（可选）
huggingface-cli download Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit --local-dir models/Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit
```

## 参考音频准备

Voice Cloning 需要一段参考音频（`.wav`），建议：

1. 从 Bilibili / YouTube 下载含目标声音的视频
2. 用 `ffmpeg` 提取并裁剪音频（5-15 秒，纯语音，无背景音乐）：

```bash
# 下载（用 yt-dlp）
yt-dlp -x --audio-format wav -o "raw.wav" "https://www.bilibili.com/video/..."

# 裁剪（例如取 1:30 到 1:45）
ffmpeg -i raw.wav -ss 00:01:30 -to 00:01:45 -ac 1 -ar 24000 voices/reference.wav
```

3. 将处理好的音频放到 `voices/reference.wav`

> 音频质量直接影响克隆效果。选择清晰、无噪音、无 BGM 的片段。

## 使用

### Voice Cloning

修改 `speak.py` 或 `clone_test.py` 中的 `ref_text` 为参考音频的实际文本内容，然后：

```bash
# 快速生成并播放
python speak.py "你好，这是语音克隆测试！"

# 生成并保存到 outputs/
python clone_test.py
```

### CustomVoice

不需要参考音频，使用预设声音：

```bash
python custom_test.py
```

可在脚本中修改 `voice`（预设声音）、`instruct`（风格指令）、`lang_code`（语言）等参数。

## Claude Code 集成

将 TTS 集成到 Claude Code，实现：
- 每次任务完成后，Claude 自动用克隆的声音播报摘要
- 权限确认时播放提示音
- 通知时播放提示音

### 配置步骤

1. **生成提示音频**：先用 `clone_test.py` 生成需要的提示音（修改 `text` 内容），保存到 `outputs/`

2. **配置 `~/.claude/settings.json`**：参考 `claude-code/settings.json`，将 `<YOUR_VENV_PATH>` 和 `<YOUR_PROJECT_PATH>` 替换为实际路径

3. **配置 `~/.claude/CLAUDE.md`**：参考 `claude-code/CLAUDE.md`，同样替换路径占位符

### 示例配置

```json
{
  "permissions": {
    "allow": [
      "Bash(/path/to/qwen3-tts-voice-clone/.venv/bin/python /path/to/qwen3-tts-voice-clone/speak.py:*)"
    ]
  },
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "afplay /path/to/qwen3-tts-voice-clone/outputs/notification.wav &",
            "async": true
          }
        ]
      }
    ]
  }
}
```

## 项目结构

```
qwen3-tts-voice-clone/
├── speak.py            # 核心 TTS 脚本（Claude Code 调用）
├── clone_test.py       # Voice Cloning 测试
├── custom_test.py      # CustomVoice 测试
├── requirements.txt    # Python 依赖
├── voices/             # 参考音频（.wav，不含在仓库中）
├── outputs/            # 生成的音频（不含在仓库中）
├── models/             # 模型文件（不含在仓库中）
└── claude-code/        # Claude Code 配置示例
    ├── settings.json
    └── CLAUDE.md
```

## 致谢

- [kapi2800/qwen3-tts-apple-silicon](https://github.com/kapi2800/qwen3-tts-apple-silicon) — 本项目基于此项目
- [Qwen/Qwen3-TTS](https://huggingface.co/Qwen/Qwen3-TTS) — 阿里通义千问 TTS 模型
- [Blaizzy/mlx-audio](https://github.com/Blaizzy/mlx-audio) — MLX 音频框架
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — Anthropic CLI 工具
