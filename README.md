# GrokCoder
Overview

GrokCoder is a production-ready, standalone chat application built with Streamlit, designed for seamless interaction with xAI's Grok AI models (including Grok-4 and Grok-Beta). Optimized for environments like Raspberry Pi 5 with Python virtual environments, it offers a user-friendly interface with streaming responses, customizable system prompts, chat history management, user authentication, and integrated sandboxed file system tools. This v1 release focuses on stability, security, and extensibility for both casual users and developers exploring AI-powered conversations.


Key highlights include vision model support for image analysis, dark mode toggling, and a responsive UI with neon gradient themes. The app uses the OpenAI SDK for xAI compatibility, ensuring reliable API interactions with built-in error handling and retry mechanisms.


Features


Streaming Chat Responses: Real-time, chunked responses from Grok models for a smooth conversational experience.

Model Selection: Switch between Grok-4 and Grok-Beta dynamically via the sidebar.

Customizable System Prompts: Load, edit, and save prompts from ./prompts/ directory (auto-creates defaults like "coder.txt" for specialized interactions).

User Authentication: Secure login/register system using SQLite database with password hashing (SHA-256 crypt).

Chat History Management: Save, load, search, and delete conversations per user; auto-titles based on initial messages.

Sandboxed File System Tools: Enable AI access to read/write/list files in ./sandbox/ (safe, isolated operations with path validation).

Time Synchronization Tool: Fetch current datetime (host or NTP-synced) for context-aware responses.

Vision Support: Upload and analyze images (JPG/PNG) for multimodal conversations.

Responsive UI: Neon gradient theme with chat bubbles, avatars, code block wrapping, and dark mode toggle.

Performance Optimizations: Message truncation (last 50), expanders for long chats, and concurrent-safe SQLite (WAL mode).

Security & Safety: HTML escaping for content rendering, sandboxed tool access, and loop prevention in API calls.

Logging & Debugging: Console and file-based logs for API/tool errors; auto-retry on failures.

Extensibility: Easy to add new tools or models; designed for deployment on lightweight hardware.


Installation

Prerequisites


Python 3.8+ (recommended: Python 3.10 for Raspberry Pi compatibility).

A valid xAI API key (sign up at xAI if needed).

Internet connection for API calls and optional NTP sync.


Setup Steps



Clone or Download the Repository:


git clone https://github.com/yourusername/grokcoder.git
cd grokcoder




Set Up Virtual Environment (recommended for isolation):


python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate




Install Dependencies:


pip install streamlit openai passlib python-dotenv ntplib




Configure Environment:



Create a .env file in the root directory:
XAI_API_KEY=your_xai_api_key_here



Ensure the key is set; the app will prompt if missing.




Run the App:


streamlit run pne19s_2.py



Access at http://localhost:8501 in your browser.

On Raspberry Pi: Use a browser or enable remote access via streamlit run pne19s_2.py --server.headless true --server.port 8501.




Directory Structure


pne19s_2.py: Main application script.

./prompts/: Directory for system prompt files (auto-populated with defaults).

./sandbox/: Sandboxed directory for file tools (AI-safe R/W operations).

chatapp.db: SQLite database for users and history (created automatically).

.env: Environment variables (API key).

app.log: Error log file (generated on errors).


Usage


Launch the App: Run as described in Installation. Register or log in to access the chat interface.

Configure Settings (Sidebar):

Select a Grok model.

Choose or edit a system prompt (e.g., "tools-enabled.txt" for file access).

Enable tools if needed (e.g., for sandbox file operations).

Upload images for vision-enabled chats.



Chat Interaction:

Type messages in the input box; responses stream in real-time.

View chat history in the sidebar; search, load, or delete past conversations.

Toggle dark mode for better visibility.



Tool Usage (when enabled):

The AI can invoke sandboxed tools like reading/writing files or fetching time.

Example: Ask "List files in the sandbox" to trigger fs_list_files.



Best Practices:

Keep chats under 50 messages for optimal performance (auto-truncation applies).

Use code blocks (```) for better rendering in responses.

For production, monitor app.log for errors.




Example Interactions


Basic Chat: "Explain Python recursion."

With Tools: "Read the content of test.txt in the sandbox."

Vision: Upload an image and ask "What's in this photo?"

Time Query: "What's the current time?" (uses NTP if synced).


Screenshots

(Add placeholders or actual images here once deployed)



Main chat interface with neon theme.

Sidebar settings and history.

Dark mode toggle example.


Requirements


Python Libraries: streamlit, openai, passlib, python-dotenv, ntplib.

System: Compatible with Linux (e.g., Raspberry Pi), macOS, Windows; lightweight enough for low-resource devices.

API: xAI Grok API (no additional costs beyond your xAI usage).


Contributing

Contributions are welcome! This is v1, so we're looking for feedback on usability, new features (e.g., more models or tools), and bug fixes.



Fork the repository.

Create a feature branch: git checkout -b feature/your-idea.

Commit changes: git commit -m &quot;Add your feature&quot;.

Push and submit a pull request.


Please ensure code follows PEP 8, includes comments, and is tested for security (e.g., no sandbox escapes).


License

This project is licensed under the MIT License. See LICENSE for details.


Acknowledgments


Built with Streamlit for the UI framework.

Powered by xAI's Grok API for AI capabilities.

Inspired by open-source chat apps; special thanks to the xAI community for model access.

Icons and themes adapted from free resources (e.g., gradient designs).


For issues or questions, open a GitHub issue or contact the maintainer. Happy chatting with GrokCoder! 🚀
