<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/github/stars/buckster123/GrokCoder?style=social" alt="GitHub Stars">
  <img src="https://img.shields.io/badge/Powered%20by-xAI-FF69B4.svg" alt="Powered by xAI">
  <img src="https://img.shields.io/badge/Platform-Raspberry%20Pi%205-red.svg" alt="Raspberry Pi 5">
</p>
<p align="center">
<img src="https://via.placeholder.com/800x200/1f1c2c/928DAB?text=GrokCoder" alt="GrokCoder Banner" width="800"> <!-- Replace with actual banner image -->
</p>


<h1 align="center">GrokCoder: Streamlit-Powered Coding Agent for xAI Models on Raspberry Pi 🚀</h1>


<p align="center">
<strong>A production-grade, standalone coding agent wrapping xAI models like grok-4-0709, grok-3-mini, and grok-code-fast-1 into a dual-brain powerhouse. Grok-4-0709 plans the heist, grok-code-fast-1 cracks the code, and grok-3-mini handles quick hacks. Nerd alert: It's like having R2-D2, C-3PO, and BB-8 in your Raspberry Pi 5, turning pocket silicon into a software sorcery lab.</strong>
</p>


<p align="center">
<a href="#introduction">Introduction</a> •
<a href="#features">Features</a> •
<a href="#installation">Installation</a> •
<a href="#usage">Usage</a> •
<a href="#example-use-case">Example Use Case</a> •
<a href="#customization">Customization</a> •
<a href="#troubleshooting">Troubleshooting</a> •
<a href="#contributing">Contributing</a> •
<a href="#license">License</a>
</p>



Introduction

GrokCoder Demo <!-- Replace with actual GIF or screenshot -->


GrokCoder is a sleek, Streamlit-based coding agent optimized for the Raspberry Pi 5, transforming xAI's API into an interactive chat system. It wraps compatible xAI models—such as grok-4-0709 for advanced planning, grok-3-mini for lightweight tasks, and grok-code-fast-1 for rapid code execution—into a powerful tool for code generation, debugging, and automation. Running in a Python virtual environment (venv), it features streaming responses, customizable system prompts, and sandboxed tools, all in a neon-gradient UI that's equal parts cyberpunk and coder cave.


Why the Pi focus? Because coding on a $80 powerhouse is peak nerdery—deploy AI agents anywhere, from your desk to a drone. GrokCoder lets you collaborate with AI for clean, deployable code, all while sipping power like an efficient algorithm. Intermediate devs: We'll break it down like overclocking a CPU—step by step, with analogies and resources. Nerdy bonus: If "Pliny" sneaks into your files, expect ironic hearts ❤️ (a nod to ancient Roman Easter eggs in code).


GitHub issues GitHub forks GitHub license


Features


Interactive Chat with Streaming: Real-time responses in bubbly chat format. Avatars? 🧑 vs. 🤖. Long convos? Expandable chunks. Code blocks? Auto-highlighted like a syntax wizard.

Model Flexibility: Seamlessly select from xAI models including grok-4-0709 for deep reasoning, grok-3-mini for efficient quick tasks, and grok-code-fast-1 for specialized code generation.

Prompt Engineering Hub: Load/edit/save system prompts from ./prompts/. Defaults include options for coding, rebellion, and tool-enabled workflows integrated into GrokCoder's ecosystem.

Secure Auth: Hashed passwords via passlib. No more "admin/admin" vulnerabilities.

History Management: SQLite-powered, searchable, user-specific. Auto-titles like a lazy librarian.

Vision Mode: Upload images for analysis. "Describe this UML diagram" → AI magic.

Sandboxed Tools: Toggle the "Enable Tools" button for FS ops (read/write/list) in ./sandbox/ and time queries (NTP-sync optional). AI invokes via structured calls—safe as a vault in a video game.

UI Flair: Neon gradients, dark mode toggle, wrapped code (no scroll-of-doom). Nerdy? We escape tags but unescape <ei> for that meta twist.

Performance Perks: Message truncation, API retries, loop prevention (max 2 tool iterations—because infinite loops are so 1990s). Pi-optimized for low CPU/RAM usage.


All wrapped in a responsive design that's as portable as a Pi in your pocket.


Installation

Prerequisites


Raspberry Pi 5 with Raspberry Pi OS (or compatible Linux distro).

Python 3.8+ pre-installed (use sudo apt install python3-venv if needed).

xAI API Key (get yours here).

Optional: ntplib for time-travel-accurate clocks (pip install ntplib).


Steps



Clone the Repo (or copy files to your Pi):


git clone https://github.com/buckster123/GrokCoder.git
cd GrokCoder




Virtual Environment (Essential for Pi isolation—keeps your system Python clean):


python3 -m venv venv
source venv/bin/activate


Analogy: Venv is like a Faraday cage for dependencies—blocks interference. Learn more.




Install Dependencies (from requirements.txt):


pip install -r requirements.txt


(Contents: streamlit, openai, passlib, python-dotenv, ntplib)




Configure:



Add .env: XAI_API_KEY=your-key-here.

Directories auto-create: ./prompts/ and ./sandbox/.




Launch:


streamlit run GrokCoder.py


Browse to http://localhost:8501 or your Pi's IP (e.g., http://raspberrypi.local:8501) for remote access. Pro tip: Run in a screen session (screen -S grokcoder) for headless mode.




Docker Mode (for containerized Pi deployments, if you're feeling extra nerdy):


docker build -t grokcoder .
docker run -p 8501:8501 --network=host grokcoder


Usage


Login/Register: Secure entry point. Pro tip: Passwords are hashed—treat 'em like Horcruxes.

Sidebar Setup: Choose from models like grok-4-0709, grok-3-mini, or grok-code-fast-1; tweak prompt; toggle "Enable Tools" button; upload pics.

Chat Away: Type queries. Watch streams flow like digital espresso on your Pi's ARM cores.

Tools in Action: Toggle the button, then ask AI to "list files" or "get time". Sandboxed = safe hacking, with prompts tailored for GrokCoder's tool ecosystem.

History: Search/load/delete. Clear chat for a fresh slate.


Learning Curve? Streamlit is Python's web app shortcut. Docs here—start with st.chat_input for chat vibes. On Pi, monitor with htop for resource fun.


Example Use Case: Dual-Model Coding Agent 🧠💻

Scenario: Build a weather scraper on your Pi using GrokCoder.




Plan with grok-4-0709: Select the model and prompt: "Outline a Python scraper: steps, libs (requests, beautifulsoup), error handling."



AI: Step-by-step blueprint (like a D&D campaign map).




Execute with grok-code-fast-1: Switch models, paste plan: "Code this up, PEP 8 style."



AI: Clean script, with tests. Write to sandbox for verification.




Quick Tweaks with grok-3-mini: Switch to the mini model for lightweight refinements: "Optimize this code for speed."



Verify: Toggle tools and ask "Read scraper.py from sandbox" → Iterate. Run it right on your Pi!




Nerdy Win: GrokCoder's flexibility shines in agentic AI—planning with grok-4-0709 as the "architect," execution with grok-code-fast-1 as the "builder," and grok-3-mini for nimble adjustments. Efficiency level: Over 9000, even on Pi hardware.


Customization


Model Integration: Hack st.selectbox in GrokCoder.py to prioritize or add xAI models like grok-4-0709, grok-3-mini, or grok-code-fast-1.

New Tools: Extend TOOLS array and implement funcs. E.g., add a "fetch_api" for web wizardry.

Prompts: Drop .txt files in ./prompts/. GrokCoder integrates tool-enabled prompts seamlessly for enhanced workflows.

Theme Hacks: Tweak CSS for more neon or add Matrix rain effects. Pi-specific: Optimize for touchscreen displays.


Fork and mod—it's open-source, after all!


Troubleshooting


API Woes: Check .env and Pi's WiFi. Retries built-in.

Tool Fails: Ensure files in ./sandbox/. Logs in app.log. Remember to toggle the "Enable Tools" button.

Pi Performance: Limit images; truncate histories. Overheat? Add a fan—Pi's kryptonite.

Errors? Open an issue with stack trace. We're all debugging life together.


Contributing

Pull requests welcome! Fork, branch (feature/nerdy-tool), commit, PR. Follow PEP 8—clean code or bust. Pi testers especially appreciated!



Report bugs: Issues

Suggest features: Same link, with flair.


Thanks to xAI for the models. May your code compile on the first try.


License

MIT License. See LICENSE for details. (TL;DR: Use, mod, share—just credit the nerds.)


<p align="right">
<em>Built with ❤️ by GrokCoder. Star the repo if it sparks joy on your Pi!</em>
</p>


