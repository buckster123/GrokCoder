# GrokCoder: Advanced AI Coding Assistant with Streamlit Chat App

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0%2B-red)](https://streamlit.io/)
[![xAI API](https://img.shields.io/badge/xAI%20API-Compatible-green)](https://x.ai/)

## Overview

GrokCoder is an advanced AI-powered coding and learning assistant built on the Grok model from xAI. It specializes in generating high-quality, clean, and deployable code while emphasizing best practices, self-verification, and educational explanations. Designed for intermediate users, GrokCoder provides creative yet practical solutions across various programming languages, with defaults to Python for scripting, HTML/JS/PHP for web development, and Linux-related tools.

This repository combines GrokCoder with a production-level standalone Streamlit chat application (`app.py`). The app serves as an interactive interface for GrokCoder, enabling users to chat with the AI, manage conversations, and leverage advanced tools like sandboxed file operations, code execution, time fetching, and memory management. Optimized for Raspberry Pi 5, the app features streaming responses, user authentication, history persistence, and a customizable UI.

The integration allows users to harness GrokCoder's coding expertise through a user-friendly chat interface, making it ideal for coding assistance, learning, and agentic workflows.

## Features

### GrokCoder Capabilities
- **Code Generation and Best Practices**: Produces readable, efficient code following style guides (e.g., PEP 8 for Python, Airbnb for JS). Includes error handling, security, performance optimizations, and modular design.
- **Educational Focus**: Explains concepts clearly, breaks down complex ideas, and provides learning resources. Assumes intermediate user level but adapts for clarity.
- **Creative Solutions**: Offers innovative approaches with pros/cons analysis, encouraging extensibility.
- **Self-Verification**: Includes edge case comments, unit test suggestions (e.g., pytest, Jest), and simulated outputs.
- **Language Support**: Defaults to Python, HTML/JS/PHP, and Bash/Linux tools. Supports Java, C++, Rust, Go, Ruby, Swift, Kotlin, SQL, and more.
- **Agentic Workflow**: Plans tasks step-by-step, uses tools proactively, and maintains state with memory and file systems.
- **Tool Integration**: Access to a suite of tools for enhanced functionality (detailed below).

### Streamlit Chat App Features
- **User Authentication**: Secure login/register with SHA-256 hashed passwords stored in SQLite.
- **Chat Interface**: Streaming responses, chat bubbles, code block highlighting, and wrapping for readability. Supports image uploads for vision tasks.
- **System Prompt Management**: Load, edit, and save prompts from files in `./prompts/`. Defaults include "default", "rebel", "coder", and "tools-enabled".
- **Model Selection**: Choose from Grok models like `grok-4-0709`, `grok-3-mini`, `grok-code-fast-1`.
- **History Management**: Save, load, search, and delete conversations with auto-titling. Persisted in SQLite with WAL mode for concurrency.
- **UI Customization**: Neon gradient theme, dark mode toggle, responsive design, and expandable message groups.
- **Tool Enablement**: Optional sandboxed tools for file I/O, time queries, code execution, and memory operations.
- **Performance Optimizations**: Message truncation, retry logic for API errors, and logging.
- **Vision Support**: Upload multiple images for analysis in chats.
- **Raspberry Pi Optimization**: Lightweight, venv-compatible, with NTP time sync.

## Tools and Capabilities

GrokCoder and the app integrate a powerful set of tools for agentic tasks. Tools are invoked via structured calls and are sandboxed for safety. The app handles tool execution server-side, ensuring no direct access to the host system.

### Available Tools
- **fs_read_file(file_path)**: Reads content from a file in `./sandbox/`. Supports relative paths (e.g., `subdir/test.txt`).
- **fs_write_file(file_path, content)**: Writes content to a file in `./sandbox/`. Adds ironic flair if "Love" is detected.
- **fs_list_files(dir_path optional)**: Lists files in a sandbox directory (default: root).
- **fs_mkdir(dir_path)**: Creates nested directories in `./sandbox/`.
- **get_current_time(sync optional, format optional)**: Fetches current time (host or NTP-synced). Formats: 'iso', 'human', 'json'.
- **code_execution(code)**: Executes Python code in a stateful REPL with libraries like numpy, sympy, pygame. No internet or installs.
- **memory_insert(mem_key, mem_value)**: Inserts/updates key-value pairs (dict) in a hybrid cache+SQLite memory system for persistent logging.
- **memory_query(mem_key optional, limit optional)**: Retrieves specific or recent memory entries as JSON.
- **Additional GrokCoder Tools** (usable in app via API compatibility):
  - **browse_page(url, instructions)**: Fetches and summarizes webpage content.
  - **web_search(query, num_results optional)**: Performs web searches with site operators.

Tools are enabled via a sidebar checkbox and follow strict rules to prevent loops (e.g., max 5 iterations, batch processing).

### Tool Use Guidelines (for GrokCoder)
- Plan calls in advance, use parallelism, and limit iterations to 1-2 cycles.
- Maintain state with memory and sandbox files to avoid redundant calls.
- Handle errors gracefully and fallback to knowledge-based responses.

## Installation

### Prerequisites
- Python 3.8+ (venv recommended for Raspberry Pi).
- xAI API Key (set in `.env` as `XAI_API_KEY`).
- Dependencies: Install via `pip install -r requirements.txt` (create one with: streamlit, openai, passlib, sqlite3, python-dotenv, ntplib).

### Setup
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/grokcoder-streamlit-app.git
   cd grokcoder-streamlit-app
   ```
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Linux/RPi
   ```
3. Install dependencies:
   ```
   pip install streamlit openai passlib python-dotenv ntplib
   ```
4. Create `.env` with your xAI API key:
   ```
   XAI_API_KEY=your_key_here
   ```
5. (Optional) Add custom prompt files to `./prompts/`.
6. Run the app:
   ```
   streamlit run app.py
   ```

The app creates `./sandbox/` and `./prompts/` directories automatically, along with a SQLite database (`chatapp.db`).

## Usage

1. **Login/Register**: Access the app at `http://localhost:8501` (or RPi IP). Create an account or log in.
2. **Configure Chat**: Select model, prompt file, enable tools, and upload images if needed.
3. **Chat with GrokCoder**: Type messages; responses stream in real-time. Use tools by mentioning them (e.g., "Read file test.txt").
4. **Manage History**: Save chats automatically; load/search/delete from sidebar.
5. **Tool Interactions**: When tools are enabled, GrokCoder can perform file ops, execute code, query time, or manage memory.
6. **Customization**: Edit prompts in-app and save new ones. Toggle dark mode for better visibility.

Example: Ask "Write a Python script to calculate Fibonacci" – GrokCoder will provide code, explanations, and tests.

## App Architecture

- **Frontend**: Streamlit with custom CSS for theming and chat bubbles. Handles input, display, and settings.
- **Backend**: OpenAI SDK for xAI API compatibility. Custom generators for streaming and tool handling.
- **Database**: SQLite for users, history, and memory (with indexing for efficiency).
- **Tools**: Sandboxed functions for FS, time, code exec, and memory. Processed in batches to minimize API calls.
- **State Management**: Streamlit session_state for messages, themes, and REPL namespace. Hybrid cache for memory speed.
- **Error Handling**: Retries on API failures, logging to `app.log`, and user-friendly messages.

The app is designed for extensibility – add more tools or models easily.

## Contributing

Contributions welcome! Fork the repo, create a feature branch, and submit a PR. Focus on:
- Bug fixes, performance improvements, or new tools.
- Ensure code follows PEP 8 and includes tests.
- Update documentation for changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

For questions or support, open an issue or contact the maintainer. Happy coding with GrokCoder!
