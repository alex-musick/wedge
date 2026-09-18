# Wedge - Minimal, Local-first Coding Agent Repository

## Overview
Wedge is a lightweight Python-based coding agent harness designed for local use with self-hosted LLMs. It provides safety controls, context management, and file system tools for supervised coding tasks.

---

## Project Structure

### Root Files
| File | Purpose |
|------|---------|
| `main.py` | CLI entry point; parses `/model`, `/danger`, `/compact`, etc. commands and runs the work loop |
| `ai_interface.py` | Core interface to the LLM proxy (llama-swap); manages messages, context, and tool calls |
| `settings.py` | Loads configuration from `settings.json`; provides compact threshold logic |
| `tool_safety_wrapper.py` | Implements safety checks for destructive operations (`update`, `append`, `shell`) based on mode |
| `compact.py` | Triggers context compaction via a system prompt and resets messages |

### Prompts
- `prompts/main.md` — System prompt defining the agent's role, rules, and tool usage constraints
- `prompts/compact.md` — Compact instruction telling the model to summarize context before resetting

### Tools (`tools/`)
All tools are registered in `tools/tool.py`. Individual implementations:

| Tool | File | Description |
|------|------|-------------|
| `append` | `append.py` | Appends text after the last line of a file; creates file if missing |
| `count_lines` | `count_lines.py` | Returns number of lines in a file |
| `list_dir` | `listdir.py` | Lists files and directories in a path (`.` = current directory) |
| `read` | `read.py` | Reads a range of lines from a file (1-indexed, `end` optional) |
| `shell` | `shell.py` | Runs arbitrary shell commands; denies `echo`, `cat`, `ls`, `dir` |
| `update` | `update.py` | Replaces lines in a file; `end` omitted → single line replace |

### Configuration
- `settings.json` — LLM proxy URL, default model ID, compact thresholds (value/percent), and fallback defaults
- `.gitignore` — Standard Python ignore plus `testfile`

---

## Safety Modes

Controlled by `safety_mode` in `main.py` and enforced by `tool_safety_wrapper.py`:

| Mode | Behavior |
|------|----------|
| **0** (default) | All destructive edits (`update`, `append`) and shell commands require explicit user approval via prompt |
| **1** | Edits are auto-approved only if the target file is within the current working directory; shell still needs approval |
| **2** (YOLO) | Every tool call is auto-approved; use only in a trusted sandbox/container |

---

## Commands (sent to `main.py`)

- `/model {id}` — Change the LLM model ID without clearing context
- `/danger {0,1,2}` / `/safety {0,1,2}` — Set safety mode
- `/compact` — Invoke compaction; will summarize current context and reset messages
- `/clear` — Discard all messages, returning to just the system prompt
- `/exit` or `/quit` — Terminate the session

---

## Usage Workflow

1. Ensure `llama-swap` is running with your preferred model at the base URL configured in `settings.json`.
2. Adjust `settings.json` if you need a different proxy URL, model, or compact thresholds.
3. Launch: `python main.py <model-id>` (or omit to use default).
4. Interact via natural language prompts; destructive edits will prompt for approval unless you've raised the safety mode.

---

## Dependencies

- `requests` / `httpx` — HTTP client for proxy communication
- `colorama` — Colored console output
