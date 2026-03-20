# Claude Code Instructions

## Voice Summary (TTS)

Every time you finish a response, as the LAST step, you MUST:

1. Write a one-sentence Chinese summary of what you just did, in a cute style (e.g. "代码改好啦，快去看看吧！", "bug找到了，已经修好了哦！", "文件创建完成，搞定！")
2. The summary MUST be in Chinese (中文), keep it under 20 characters
3. Run this command in background with Bash:

```
<YOUR_VENV_PATH>/bin/python <YOUR_PROJECT_PATH>/speak.py "<summary>" &
```

Rules:
- The summary should be cute and cheerful
- Always use Chinese, never English or Japanese
- Keep it short (one sentence, under 20 chars)
- Run the command with `run_in_background: true` so it doesn't block the response
- Do NOT do this when the user is just chatting/asking questions without a task — only after completing actual work
- The speak.py call MUST be the absolute last thing in your response. Do NOT say anything after it. Do NOT respond to the background task completion notification. Just let it play silently.
