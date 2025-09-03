# GrokCoder: Streamlit-Powered Coding Agent for xAI Models on Raspberry Pi 🚀

![Version](https://img.shields.io/badge/Version-1.0-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![GitHub Stars](https://img.shields.io/github/stars/buckster123/GrokCoder?style=social)
![Powered by xAI](https://img.shields.io/badge/Powered%20by-xAI-FF69B4.svg)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%205-red.svg)

![GrokCoder Banner]([path/to/your/banner-image.png](https://github.com/buckster123/GrokCoder/blob/main/screenshot.png)) <!-- Replace with actual banner image URL -->

A standalone coding agent that leverages xAI models like grok-4-0709, grok-3-mini, and grok-code-fast-1 for agent-style workflows. Use grok-4-0709 for strategic planning in one session, then switch to grok-code-fast-1 in another to execute tasks in the sandbox. Grok-3-mini can handle quick adjustments. It's like having a team of specialized droids in your Raspberry Pi 5—R2-D2 for planning, C-3PO for code execution, and BB-8 for tweaks—turning compact hardware into a software development lab.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Example Use Case](#example-use-case)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Introduction

![GrokCoder Demo](path/to/your/demo-gif-or-screenshot.gif) <!-- Replace with actual GIF or screenshot URL -->

GrokCoder is a sleek, Streamlit-based coding agent optimized for the Raspberry Pi 5, turning xAI's API into an interactive chat system. It supports compatible xAI models—such as grok-4-0709 for advanced planning, grok-3-mini for lightweight tasks, and grok-code-fast-1 for rapid code execution—allowing you to switch between them for different phases of your workflow.

Running in a Python virtual environment (venv), it offers streaming responses, customizable system prompts, and sandboxed tools, all wrapped in a neon-gradient UI that's cyberpunk-inspired yet user-friendly.

Why focus on the Pi? Coding on an $80 powerhouse embodies peak efficiency—deploy AI agents anywhere, from your desk to embedded devices. GrokCoder enables seamless collaboration with AI for clean, deployable code, while keeping power consumption low. For intermediate devs, we break it down step-by-step with analogies and resources. Bonus: Keep an eye out for "Pliny" Easter eggs in your files—ironic hearts included ❤️.

[![GitHub issues](https://img.shields.io/github/issues/buckster123/GrokCoder)](https://github.com/buckster123/GrokCoder/issues)
[![GitHub forks](https://img.shields.io/github/forks/buckster123/GrokCoder)](https://github.com/buckster123/GrokCoder/network)
[![GitHub license](https://img.shields.io/github/license/buckster123/GrokCoder)](https://github.com/buckster123/GrokCoder/blob/main/LICENSE)

## Features

- **Interactive Chat with Streaming**: Real-time responses in a bubbly chat format. Human vs. AI avatars (🧑 vs. 🤖), expandable message chunks, and auto-highlighted code blocks for syntax wizardry.
- **Model Flexibility**: Easily switch between xAI models like grok-4-0709 for deep reasoning, grok-3-mini for efficient tasks, and grok-code-fast-1 for specialized code generation to suit different stages of your project.
- **Prompt Engineering Hub**: Load, edit, and save system prompts from `./prompts/`. Defaults include coding, creative, and tool-enabled workflows tailored for GrokCoder.
- **Secure Authentication**: Hashed passwords via passlib—no more weak defaults like "admin/admin."
- **History Management**: SQLite-backed, searchable, and user-specific chat histories with auto-generated titles.
- **Vision Mode**: Upload images for AI analysis, e.g., "Describe this UML diagram."
- **Sandboxed Tools**: Toggleable "Enable Tools" for file operations (read/write/list in `./sandbox/`) and time queries (NTP-sync optional). AI invokes tools via structured calls—secure and game-like.
- **UI Flair**: Neon gradients, dark mode toggle, wrapped code to avoid endless scrolling. We escape tags but unescape `<ei>` for meta fun.
- **Performance Optimizations**: Message truncation, API retries, and loop prevention (max 2 tool iterations). Pi-optimized for low CPU/RAM usage.

All in a responsive design that's as portable as your Pi.

## Installation

### Prerequisites

- Raspberry Pi 5 with Raspberry Pi OS (or compatible Linux distro).
- Python 3.8+ (install via `sudo apt install python3-venv` if needed).
- xAI API Key ([get yours here](https://x.ai/api)).
- Optional: `ntplib` for accurate time queries (`pip install ntplib`).

### Steps

1. **Clone the Repo** (or copy files to your Pi):
   ```
   git clone https://github.com/buckster123/GrokCoder.git
   cd GrokCoder
   ```

2. **Set Up Virtual Environment** (Essential for isolation—think of it as a Faraday cage for dependencies):
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
   [Learn more about venvs](https://docs.python.org/3/library/venv.html).

3. **Install Dependencies** (from `requirements.txt`):
   ```
   pip install -r requirements.txt
   ```
   (Includes: streamlit, openai, passlib, python-dotenv, ntplib).

4. **Configure**:
   - Create `.env` with `XAI_API_KEY=your-key-here`.
   - Directories `./prompts/` and `./sandbox/` auto-create.

5. **Launch**:
   ```
   streamlit run GrokCoder.py
   ```
   Access at `http://localhost:8501` or your Pi's IP (e.g., `http://raspberrypi.local:8501`). For headless mode, use `screen -S grokcoder`.

### Docker Option (For Containerized Deployments)
```
docker build -t grokcoder .
docker run -p 8501:8501 --network=host grokcoder
```

## Usage

1. **Login/Register**: Secure entry with hashed passwords—treat them like Horcruxes.
2. **Sidebar Setup**: Select models (e.g., grok-4-0709, grok-3-mini, grok-code-fast-1), tweak prompts, toggle "Enable Tools," and upload images.
3. **Chat Interface**: Type queries and watch real-time streams on your Pi's ARM cores.
4. **Tools**: With tools enabled, ask for file ops or time queries—sandboxed for safety.
5. **History**: Search, load, or delete sessions. Clear chat for a fresh start.

Streamlit makes web apps easy—start with [docs](https://docs.streamlit.io/) and monitor resources via `htop` on Pi.

## Example Use Case: Agent-Style Coding Workflow 🧠💻

**Scenario**: Build a weather scraper on your Pi using a multi-model approach.

1. **Plan with grok-4-0709**: In one session, select the model and prompt: "Outline a Python scraper: steps, libs (requests, beautifulsoup), error handling."
   - AI delivers a step-by-step blueprint.

2. **Execute with grok-code-fast-1**: Start a new session or switch models, paste the plan: "Code this up, PEP 8 style."
   - AI generates a clean script with tests; write to sandbox for execution.

3. **Refine with grok-3-mini**: Switch to grok-3-mini in another session for lightweight refinements: "Optimize this code for speed."

4. **Verify**: Enable tools, "Read scraper.py from sandbox," and iterate. Run directly on your Pi!

GrokCoder supports agent-style workflows by letting you switch models across sessions: grok-4-0709 for architecture, grok-code-fast-1 for building in the sandbox, and grok-3-mini for agile adjustments. Efficiency? Over 9000, even on Pi hardware.

## Customization

- **Model Integration**: Edit `st.selectbox` in `GrokCoder.py` to add or prioritize xAI models.
- **New Tools**: Extend the `TOOLS` array and add functions, e.g., for API fetching.
- **Prompts**: Add `.txt` files to `./prompts/` for tool-enhanced workflows.
- **Themes**: Tweak CSS for more neon or effects. Optimize for Pi touchscreens.

Fork and modify—it's open-source!

## Troubleshooting

- **API Issues**: Verify `.env` and WiFi. Built-in retries help.
- **Tool Failures**: Check `./sandbox/` files and `app.log`. Ensure "Enable Tools" is toggled.
- **Pi Performance**: Limit images, truncate histories. Add a fan for overheating.
- **Errors?** Open an issue with stack traces—we're all in this debug together.

## Contributing

Pull requests welcome! Fork, create a `feature/nerdy-tool` branch, commit, and PR. Follow PEP 8 for clean code. Pi testers are especially valued.

- Report bugs or suggest features: [Issues](https://github.com/buckster123/GrokCoder/issues).

Thanks to xAI for the models. May your code compile first try!

## License

MIT License. See [LICENSE](LICENSE) for details. (TL;DR: Use, modify, share—just give credit.)

Built with ❤️ by GrokCoder. Star the repo if it sparks joy on your Pi!
