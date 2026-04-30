# AI Media Renamer

A terminal app for renaming media files using AI.
Intended for use cases where you'd rather eat rocks than rename hundreds of files.

## Requirements

- Python 3.10 or newer
- FFmpeg for video support
- OpenRouter API key, or Ollama running locally (LOCAL MODE NOT IMPLEMENTED YET)

Go to `openrouter.ai` and create an account, then you can create an API key to use with the tool.
You need to add credits to use the `ECO`/`BALANCED`/`EXPENSIVE` modes. `FREE` uses `google/gemma-4-31b-it:free` and can work, however it can get rate-limited and cause the program to crash.

## Windows

Download the project, unzip it, then double-click:

```text
run.bat
```

## Linux/MacOS

Same as windows, after installing and unzipping, run:

```text
chmod +x run.sh
./run.sh
```

or double click run.sh.
