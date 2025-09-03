# Grok Chat: Standalone Streamlit Application for xAI API Integration

![Version](https://img.shields.io/badge/Version-1.1-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![GitHub Stars](https://img.shields.io/github/stars/buckster123/GrokCoder?style=social)
![Powered by xAI](https://img.shields.io/badge/Powered%20by-xAI-FF69B4.svg)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%205-red.svg)

![Grok Chat Banner](https://github.com/buckster123/GrokCoder/blob/main/screenshot.png)

Grok Chat is a production-level, standalone Streamlit application designed for integration with xAI's API, optimized for deployment on Raspberry Pi 5 hardware. It facilitates interactive chat sessions with models such as grok-4-0709, grok-3-mini, and grok-code-fast-1, enabling workflows for planning, code generation, and task execution. The application supports model switching to leverage each model's strengths: grok-4-0709 for strategic planning, grok-3-mini for lightweight adjustments, and grok-code-fast-1 for efficient code implementation. This setup transforms resource-constrained hardware into a capable development environment.

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

![Grok Chat Demo](path/to/your/demo-gif-or-screenshot.gif) <!-- Replace with actual GIF or screenshot URL -->

Grok Chat is a Streamlit-based application tailored for Raspberry Pi 5, providing an interactive interface for xAI's API. It utilizes the OpenAI SDK for compatibility and supports models including grok-4-0709 for complex reasoning, grok-3-mini for general tasks, and grok-code-fast-1 for specialized code generation. The application runs within a Python virtual environment, offering streaming responses, customizable system prompts, and sandboxed file operations in a modern user interface with neon-gradient styling.

Optimized for efficiency on Raspberry Pi hardware, Grok Chat enables AI-assisted development with low power consumption. It is suitable for intermediate developers, providing detailed explanations, step-by-step guidance, and resource recommendations in responses.

[![GitHub issues](https://img.shields.io/github/issues/buckster123/GrokCoder)](https://github.com/buckster123/GrokCoder/issues)
[![GitHub forks](https://img.shields.io/github/forks/buckster123/GrokCoder)](https://github.com/buckster123/GrokCoder/network)
[![GitHub license](https://img.shields.io/github/license/buckster123/GrokCoder)](https://github.com/buckster123/GrokCoder/blob/main/LICENSE)

## Features

- **Interactive Chat with Streaming Responses**: Conversational interface with real-time response generation, expandable message groups, and automatic syntax highlighting for code blocks.
- **Model Selection**: Seamless switching between xAI models (grok-4-0709, grok-3-mini, grok-code-fast-1) to align with workflow requirements.
- **System Prompt Management**: Load, edit, and save prompts from the `./prompts/` directory, with defaults for general assistance, coding, and tool-enabled scenarios.
- **User Authentication**: Secure login and registration using hashed passwords via passlib.
- **Chat History Management**: SQLite database for storing user-specific, searchable, and auto-titled conversation histories.
- **Image Analysis Support**: Upload images for model-based analysis, such as interpreting diagrams or code excerpts.
- **Sandboxed File Operations**: Toggleable tools for reading, writing, listing, and creating directories within the `./sandbox/` directory. Supports relative paths and nested structures for organized file management. The AI invokes these tools through structured calls, ensuring secure execution.
- **Persistent Memory via Sandbox**: Utilizes sandbox tools to store and retrieve hierarchical data (e.g., user preferences, project details, progress notes) as JSON files. Supports triggers for saving, recalling, updating, and searching memories, with built-in caching and size limits for efficiency.
- **User Interface Enhancements**: Neon-gradient theme, dark mode toggle, and wrapped code display to prevent horizontal scrolling.
- **Performance Optimizations**: Automatic message truncation, API retry mechanisms, and limits on tool iterations to ensure reliability on resource-limited hardware.

These features provide a responsive and efficient user experience.

## Installation

### Prerequisites

- Raspberry Pi 5 running Raspberry Pi OS or a compatible Linux distribution.
- Python 3.8 or later (install via `sudo apt install python3-venv` if necessary).
- xAI API key (obtain from [x.ai/api](https://x.ai/api)).
- Optional: `ntplib` for precise time synchronization (`pip install ntplib`).

### Steps

1. **Clone the Repository**:
   ```
   git clone https://github.com/buckster123/GrokCoder.git
   cd GrokCoder
   ```

2. **Create a Virtual Environment** (Recommended for dependency management):
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies** (from `requirements.txt`):
   ```
   pip install -r requirements.txt
   ```
   Dependencies include Streamlit, OpenAI, passlib, python-dotenv, and ntplib.

4. **Configuration**:
   - Create a `.env` file containing `XAI_API_KEY=your-key-here`.
   - The `./prompts/` and `./sandbox/` directories are created automatically.

5. **Run the Application**:
   ```
   streamlit run app.py
   ```
   Access the interface at `http://localhost:8501` or the Raspberry Pi's IP address (e.g., `http://raspberrypi.local:8501`). For headless mode, use `screen -S grokchat`.

### Docker Deployment (Optional)
```
docker build -t grokchat .
docker run -p 8501:8501 --network=host grokchat
```

## Usage

1. **Authentication**: Register or log in using secure credentials.
2. **Sidebar Settings**: Select a model, edit or load a system prompt, enable file tools, and upload images as needed.
3. **Chat Interaction**: Enter queries to receive streaming responses.
4. **Tool and Memory Usage**: With tools enabled, request file operations (e.g., create directories, read/write files) or memory actions (e.g., "Save preference: Use Python for scripts"). The AI handles confirmations and sandbox interactions.
5. **History Management**: Search, load, or delete previous conversations; clear the current chat for new sessions.

Consult the Streamlit [documentation](https://docs.streamlit.io/) for additional interface details, and monitor system resources using `htop`.

## Example Use Case: Multi-Model Development Workflow

**Scenario**: Build a web scraper on Raspberry Pi hardware using model specialization and persistent memory.

1. **Planning Phase (grok-4-0709)**: Select the model and query: "Outline a Python web scraper using requests and BeautifulSoup, including error handling." Save the outline: "Save progress on scraper-project."
   - The AI generates a structured plan, stored via sandbox tools for later access.

2. **Implementation Phase (grok-code-fast-1)**: Switch models and recall: "Recall scraper-project." Then: "Generate code based on the plan in PEP 8 style."
   - The AI produces and verifies code, suggesting sandbox storage for testing.

3. **Refinement Phase (grok-3-mini)**: Switch models and query: "Search memories for scraper-project progress." Then: "Optimize the code for performance."
   - Leverage stored data for iterative improvements.

4. **Verification**: Enable tools and request: "Create directory 'scraper' and write 'scraper.py' to it." Test the file directly.

This approach utilizes model switching and sandbox-based memory for continuous, efficient development.

## Customization

- **Model Options**: Edit the `st.selectbox` in `app.py` to include additional xAI models.
- **Tool Extensions**: Modify the `TOOLS` list to add functionalities; update prompts for new behaviors.
- **Prompt Files**: Add `.txt` files to `./prompts/` for domain-specific configurations.
- **Interface Adjustments**: Customize CSS in `app.py` for theme variations, suitable for touchscreen interfaces.

The repository is open-source; fork it for tailored modifications.

## Troubleshooting

- **API Connectivity**: Verify the `.env` file and network settings; built-in retries handle transient issues.
- **Tool Errors**: Ensure `./sandbox/` has appropriate permissions and tools are enabled. Review `app.log` for diagnostics.
- **Performance on Raspberry Pi**: Limit image uploads and truncate extended histories. Use cooling solutions for prolonged operation.
- **General Issues**: Report problems with logs and steps to reproduce on the [issues page](https://github.com/buckster123/GrokCoder/issues).

## Contributing

Contributions are welcome. Fork the repository, create a branch (e.g., `feature/new-tool`), commit changes adhering to PEP 8, and submit a pull request.

- Submit bug reports or feature requests via [Issues](https://github.com/buckster123/GrokCoder/issues).

Acknowledgments to xAI for the underlying models.

## License

MIT License. See [LICENSE](LICENSE) for full terms.
