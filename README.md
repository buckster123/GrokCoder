# GrokCoder: Streamlit-Powered Coding Agent for xAI Models on Raspberry Pi 🚀

![Version](https://img.shields.io/badge/Version-1.0-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![GitHub Stars](https://img.shields.io/github/stars/buckster123/GrokCoder?style=social)
![Powered by xAI](https://img.shields.io/badge/Powered%20by-xAI-FF69B4.svg)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%205-red.svg)

![GrokCoder Banner](https://github.com/buckster123/GrokCoder/blob/main/screenshot.png)

A standalone coding agent that leverages xAI models like grok-4-0709, grok-3-mini, and grok-code-fast-1 for agentic workflows. Use grok-4-0709 for strategic planning in one session, then switch to grok-code-fast-1 in another to execute tasks in the sandbox. Grok-3-mini can handle quick adjustments. It's like having a team of specialized agents on your Raspberry Pi 5—optimized for planning, code execution, and refinements—transforming compact hardware into an efficient software development environment.

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

GrokCoder is a streamlined, Streamlit-based coding agent optimized for the Raspberry Pi 5, integrating xAI's API into an interactive chat system. It supports compatible xAI models—such as grok-4-0709 for advanced planning, grok-3-mini for lightweight tasks, and grok-code-fast-1 for rapid code execution—enabling seamless switching between models for different workflow phases.

Running in a Python virtual environment (venv), it provides streaming responses, customizable system prompts, and sandboxed tools, all within a modern, user-friendly UI with neon-gradient accents.

Focusing on the Raspberry Pi emphasizes efficiency: Deploy AI agents on affordable hardware for desktop or embedded use. GrokCoder facilitates collaboration with AI to produce clean, deployable code, with low power consumption. For intermediate developers, responses include clear explanations, step-by-step breakdowns, and learning resources.

[![GitHub issues](https://img.shields.io/github/issues/buckster123/GrokCoder)](https://github.com/buckster123/GrokCoder/issues)
[![GitHub forks](https://img.shields.io/github/forks/buckster123/GrokCoder)](https://github.com/buckster123/GrokCoder/network)
[![GitHub license](https://img.shields.io/github/license/buckster123/GrokCoder)](https://github.com/buckster123/GrokCoder/blob/main/LICENSE)

## Features

- **Interactive Chat with Streaming**: Real-time responses in a conversational format, with human and AI avatars (🧑 vs. 🤖), expandable messages, and automatic syntax highlighting for code blocks.
- **Model Flexibility**: Switch between xAI models like grok-4-0709 for deep reasoning, grok-3-mini for efficient tasks, and grok-code-fast-1 for specialized code generation to match project stages.
- **Prompt Engineering Hub**: Load, edit, and save system prompts from `./prompts/`. Defaults include coding-focused, creative, and tool-enabled workflows tailored for GrokCoder.
- **Secure Authentication**: Uses hashed passwords via passlib for robust security.
- **History Management**: SQLite-backed chat histories that are searchable, user-specific, and auto-titled.
- **Vision Mode**: Upload images for AI analysis, such as describing diagrams or code screenshots.
- **Sandboxed Tools**: Toggleable support for file operations (read/write/list in `./sandbox/`) and time queries. AI invokes tools via structured calls for secure, controlled execution.
- **Agentic Memory Module**: A persistent, hierarchical memory system integrated into the sandbox for enhanced agentic workflows. Tracks user preferences (e.g., preferred languages or styles), projects (e.g., code structures and iterations), progress markers (e.g., successes, failures, bug fixes), and session notes. Stores data as JSON files in the sandbox root (e.g., `memory_projects_webapp.json`). Features include:
  - **Triggers**: Save via phrases like "remember this preference [details]" or "save progress on [topic]"; retrieve with "recall [category/key]" or "search memories for [keyword]"; update/delete with "update memory [key] with [new_details]" or "forget [key]".
  - **Hierarchy and Searchability**: Nested JSON structures for depth (e.g., projects with sub-elements like iterations and code snippets). Master index (`memory_index.json`) enables keyword-based searches and relational linking.
  - **Caching and Efficiency**: In-memory session cache for quick access; auto-prunes at 30 entries to prevent bloat. Confirms actions for safety and limits file sizes (<2KB).
  - **Integration**: Proactively retrieves relevant memories in responses (e.g., apply user preferences to code suggestions) and supports deep reasoning by storing plans, drafts, or analyses.
- **UI Enhancements**: Neon gradients, dark mode toggle, and wrapped code to prevent horizontal scrolling.
- **Performance Optimizations**: Message truncation, API retries, and iteration limits (max 2 tool cycles). Optimized for low CPU/RAM on Raspberry Pi hardware.

All features are designed for a responsive, portable experience.

## Installation

### Prerequisites

- Raspberry Pi 5 with Raspberry Pi OS (or compatible Linux distribution).
- Python 3.8+ (install via `sudo apt install python3-venv` if needed).
- xAI API Key ([obtain yours here](https://x.ai/api)).
- Optional: `ntplib` for accurate time queries (`pip install ntplib`).

### Steps

1. **Clone the Repository**:
   ```
   git clone https://github.com/buckster123/GrokCoder.git
   cd GrokCoder
   ```

2. **Set Up Virtual Environment** (Recommended for dependency isolation):
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
   [Learn more about virtual environments](https://docs.python.org/3/library/venv.html).

3. **Install Dependencies** (from `requirements.txt`):
   ```
   pip install -r requirements.txt
   ```
   (Includes Streamlit, OpenAI, passlib, python-dotenv, and ntplib.)

4. **Configure**:
   - Create a `.env` file with `XAI_API_KEY=your-key-here`.
   - Directories `./prompts/` and `./sandbox/` are created automatically.

5. **Launch**:
   ```
   streamlit run GrokCoder.py
   ```
   Access via `http://localhost:8501` or your Pi's IP (e.g., `http://raspberrypi.local:8501`). For headless operation, use `screen -S grokcoder`.

### Docker Option (For Containerized Deployments)
```
docker build -t grokcoder .
docker run -p 8501:8501 --network=host grokcoder
```

## Usage

1. **Login/Register**: Secure access with hashed passwords.
2. **Sidebar Configuration**: Select models (e.g., grok-4-0709, grok-3-mini, grok-code-fast-1), adjust prompts, toggle "Enable Tools," and upload images.
3. **Chat Interface**: Submit queries and view streaming responses.
4. **Tools and Memory**: With tools enabled, request file operations or use memory triggers (e.g., "remember this preference: Use Python for scripting"). The agent will confirm actions and store/retrieve data from the sandbox.
5. **History**: Search, load, or delete past sessions. Use the clear chat option for new conversations.

Refer to Streamlit [documentation](https://docs.streamlit.io/) for app basics, and monitor Pi resources with `htop`.

## Example Use Case: Agent-Style Coding Workflow 🧠💻

**Scenario**: Develop a weather scraper on your Raspberry Pi using a multi-model approach with memory persistence.

1. **Plan with grok-4-0709**: Select the model and query: "Outline a Python scraper: steps, libraries (requests, BeautifulSoup), error handling." Save the plan: "Save progress on weather-scraper project."
   - AI provides a blueprint; memory module stores it hierarchically for later retrieval.

2. **Execute with grok-code-fast-1**: Switch models, recall: "Recall project weather-scraper." Then: "Implement this plan in PEP 8 style."
   - AI generates code, self-verifies, and suggests sandbox writes. Track failures: "Log failure: API rate limit issue."

3. **Refine with grok-3-mini**: Switch models, search memories: "Search memories for weather-scraper progress." Query: "Optimize this code for efficiency."
   - Use stored progress markers to iterate quickly.

4. **Verify**: Enable tools, "Read scraper.py from sandbox," and test. Memory ensures continuity across sessions.

This workflow leverages model switching and the memory module for persistent, agentic development—efficient even on Pi hardware.

## Customization

- **Model Integration**: Modify `st.selectbox` in `GrokCoder.py` to add or reorder xAI models.
- **New Tools or Memory Extensions**: Expand the `TOOLS` array or memory triggers; add custom categories via prompt edits.
- **Prompts**: Add `.txt` files to `./prompts/` for specialized workflows.
- **Themes**: Adjust CSS for UI tweaks, optimized for Pi touchscreens.

Fork the repository to customize—it's fully open-source.

## Troubleshooting

- **API Issues**: Confirm `.env` setup and network connectivity. Retries are built-in.
- **Tool or Memory Failures**: Verify `./sandbox/` permissions and "Enable Tools" toggle. Check `app.log` for details.
- **Pi Performance**: Limit image uploads and truncate long histories. Use a heatsink or fan for sustained use.
- **Errors**: Submit issues with logs and reproductions—we appreciate community input.

## Contributing

Contributions are encouraged! Fork the repository, create a feature branch (e.g., `feature/memory-enhancements`), commit changes, and submit a pull request. Adhere to PEP 8 standards.

- Report bugs or suggest features: [Issues](https://github.com/buckster123/GrokCoder/issues).

Special thanks to xAI for the foundational models.

## License

MIT License. See [LICENSE](LICENSE) for details. (In summary: Use, modify, and distribute with attribution.)

Built by the GrokCoder community. Star the repo if it enhances your development workflow!
