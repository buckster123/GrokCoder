# Grok Chat: Standalone Streamlit Application for xAI API Integration

![Version](https://img.shields.io/badge/Version-1.2-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![GitHub Stars](https://img.shields.io/github/stars/buckster123/GrokCoder?style=social)
![Powered by xAI](https://img.shields.io/badge/Powered%20by-xAI-FF69B4.svg)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%205-red.svg)

![Grok Chat Banner](https://github.com/buckster123/GrokCoder/blob/main/screenshot.png)

Grok Chat is a production-level, standalone Streamlit application designed for integration with xAI's API, optimized for deployment on Raspberry Pi 5 hardware. It facilitates interactive chat sessions with models such as grok-4-0709, grok-3-mini, and grok-code-fast-1, enabling workflows for planning, code generation, and task execution. The application supports model switching to leverage each model's strengths: grok-4-0709 for strategic planning, grok-3-mini for general tasks, and grok-code-fast-1 for specialized code generation. This setup transforms resource-constrained hardware into a capable development environment.

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
- **Code Execution Support**: Stateful Python REPL tool for executing and verifying code snippets, supporting libraries like numpy, sympy, and pygame for computational tasks.
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
