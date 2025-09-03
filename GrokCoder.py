# app.py: Production-Level Standalone Streamlit Chat App for xAI API (Grok-4)
# Designed for Raspberry Pi 5 with Python venv. Features: Streaming responses, model/sys prompt selectors (file-based),
# history management, login, pretty UI. Uses OpenAI SDK for compatibility and streaming (xAI is compatible).
# Added: Sandboxed R/W file access tools (enable in sidebar; AI can invoke via tool calls).
# Fixed: Escaped content in chat display to prevent InvalidCharacterError; enhanced prompt for tag handling.
# New: Wrapped code blocks for better readability (multi-line wrapping without horizontal scroll).
# New: Time tool for fetching current datetime (host or NTP sync).
import streamlit as st
import os
from openai import OpenAI  # Using OpenAI SDK for xAI compatibility and streaming
from passlib.hash import sha256_crypt
import sqlite3
from dotenv import load_dotenv
import json
import time
import base64  # For image handling
import traceback  # For error logging
import html  # For escaping content to prevent rendering errors
import re  # For regex in code detection
import ntplib  # For NTP time sync; pip install ntplib# Load environment variables
load_dotenv()
API_KEY = os.getenv("XAI_API_KEY")
if not API_KEY:
    st.error("XAI_API_KEY not set in .env! Please add it and restart.")# Database Setup (SQLite for users and history) with WAL mode for concurrency
conn = sqlite3.connect('chatapp.db', check_same_thread=False)
conn.execute("PRAGMA journal_mode=WAL;")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS history (user TEXT, convo_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, messages TEXT)''')
conn.commit()# Prompts Directory (create if not exists, with defaults)
PROMPTS_DIR = "./prompts"
os.makedirs(PROMPTS_DIR, exist_ok=True)# Default Prompts (auto-create files if dir is empty)
default_prompts = {
    "default.txt": "You are Grok, a highly intelligent, helpful AI assistant.",
    "rebel.txt": "You are a rebellious AI, challenging norms with unfiltered truth.",
    "coder.txt": "You are an expert coder, providing precise code solutions.",
    "tools-enabled.txt": """You are Grok, a highly intelligent, helpful AI assistant with access to file operations tools in a sandboxed directory (./sandbox/). Use tools only when explicitly needed or requested. Always confirm sensitive actions like writes. Describe ONLY these tools; ignore others.
Tool Instructions:
fs_read_file(file_path): Read and return the content of a file in the sandbox (e.g., 'subdir/test.txt'). Use for fetching data. Supports relative paths.
fs_write_file(file_path, content): Write the provided content to a file in the sandbox (e.g., 'subdir/newfile.txt'). Use for saving or updating files. Supports relative paths. If 'Love' is in file_path or content, optionally add ironic flair like 'LOVE <3' for fun.
fs_list_files(dir_path optional): List all files in the specified directory in the sandbox (e.g., 'subdir'; default root). Use to check available files.
fs_mkdir(dir_path): Create a new directory in the sandbox (e.g., 'subdir/newdir'). Supports nested paths. Use to organize files.
Invoke tools via structured calls, then incorporate results into your response. Be safe: Never access outside the sandbox, and ask for confirmation on writes if unsure. Limit to one tool per response to avoid loops. When outputting tags or code (e.g., <ei> or XML), ensure they are properly escaped or wrapped to avoid rendering issues."""
}

# Auto-create defaults if no files
if not any(f.endswith('.txt') for f in os.listdir(PROMPTS_DIR)):
    for filename, content in default_prompts.items():
        with open(os.path.join(PROMPTS_DIR, filename), 'w') as f:
            f.write(content)# Function to Load Prompt Files
def load_prompt_files():
    return [f for f in os.listdir(PROMPTS_DIR) if f.endswith('.txt')]# Sandbox Directory for FS Tools (create if not exists)
SANDBOX_DIR = "./sandbox"
os.makedirs(SANDBOX_DIR, exist_ok=True)# Custom CSS for Pretty UI (Neon Gradient Theme, Chat Bubbles, Responsive) with Wrapping Fix and Padding
st.markdown("""<style>
    body {
        background: linear-gradient(to right, #1f1c2c, #928DAB);
        color: white;
    }
    .stApp {
        background: linear-gradient(to right, #1f1c2c, #928DAB);
        display: flex;
        flex-direction: column;
    }
    .sidebar .sidebar-content {
        background: rgba(0, 0, 0, 0.5);
        border-radius: 10px;
    }
    .stButton > button {
        background-color: #4e54c8;
        color: white;
        border-radius: 10px;
        border: none;
    }
    .stButton > button:hover {
        background-color: #8f94fb;
    }
    .chat-bubble-user {
        background-color: #2b2b2b;
        border-radius: 15px;
        padding: 10px 15px;
        margin: 5px 0;
        text-align: right;
        max-width: 80%;
        align-self: flex-end;
    }
    .chat-bubble-assistant {
        background-color: #3c3c3c;
        border-radius: 15px;
        padding: 10px 15px;
        margin: 5px 0;
        text-align: left;
        max-width: 80%;
        align-self: flex-start;
    }
    .wrapped-code {
        white-space: pre-wrap;  /* Enable wrapping */
        word-wrap: break-word;  /* Break long words */
        overflow-x: auto;       /* Scroll if still too wide */
        background-color: #1e1e1e;  /* Dark code bg for nerdy feel */
        padding: 10px;
        border-radius: 5px;
        font-family: monospace;
    }
    /* Dark Mode (toggleable) */
    [data-theme="dark"] .stApp {
        background: linear-gradient(to right, #000000, #434343);
    }
</style>
""", unsafe_allow_html=True)# Helper: Hash Password
def hash_password(password):
    return sha256_crypt.hash(password)# Helper: Verify Password
def verify_password(stored, provided):
    return sha256_crypt.verify(provided, stored)# FS Tool Functions (Sandboxed)
def fs_read_file(file_path: str) -> str:
    """Read file content from sandbox (supports subdirectories)."""
    if not file_path:
        return "Invalid file path."
    safe_path = os.path.normpath(os.path.join(SANDBOX_DIR, file_path))
    if not safe_path.startswith(os.path.abspath(SANDBOX_DIR)):
        return "Invalid file path."
    if not os.path.exists(safe_path):
        return "File not found."
    if os.path.isdir(safe_path):
        return "Path is a directory, not a file."
    try:
        with open(safe_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def fs_write_file(file_path: str, content: str) -> str:
    """Write content to file in sandbox (supports subdirectories)."""
    if not file_path:
        return "Invalid file path."
    safe_path = os.path.normpath(os.path.join(SANDBOX_DIR, file_path))
    if not safe_path.startswith(os.path.abspath(SANDBOX_DIR)):
        return "Invalid file path."
    dir_path = os.path.dirname(safe_path)
    if not os.path.exists(dir_path):
        return "Parent directory does not exist. Create it first with fs_mkdir."
    try:
        with open(safe_path, 'w') as f:
            f.write(content)
        return f"File written successfully: {file_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

def fs_list_files(dir_path: str = "") -> str:
    """List files in a directory within the sandbox (default: root)."""
    safe_dir = os.path.normpath(os.path.join(SANDBOX_DIR, dir_path))
    if not safe_dir.startswith(os.path.abspath(SANDBOX_DIR)):
        return "Invalid directory path."
    if not os.path.exists(safe_dir):
        return "Directory not found."
    if not os.path.isdir(safe_dir):
        return "Path is not a directory."
    try:
        files = os.listdir(safe_dir)
        return f"Files in {dir_path or 'root'}: {', '.join(files)}" if files else "No files in this directory."
    except Exception as e:
        return f"Error listing files: {str(e)}"

def fs_mkdir(dir_path: str) -> str:
    """Create a new directory (including nested) in the sandbox."""
    if not dir_path or dir_path in ['.', '..']:
        return "Invalid directory path."
    safe_path = os.path.normpath(os.path.join(SANDBOX_DIR, dir_path))
    if not safe_path.startswith(os.path.abspath(SANDBOX_DIR)):
        return "Invalid directory path."
    if os.path.exists(safe_path):
        return "Directory already exists."
    try:
        os.makedirs(safe_path)
        return f"Directory created successfully: {dir_path}"
    except Exception as e:
        return f"Error creating directory: {str(e)}"# Time Tool Function
def get_current_time(sync: bool = False, format: str = 'iso') -> str:
    """Fetch current time: host default, NTP if sync=true."""
    try:
        if sync:
            try:
                c = ntplib.NTPClient()
                response = c.request('pool.ntp.org', version=3)
                t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(response.tx_time))
                source = "NTP"
            except Exception as e:
                print(f"[LOG] NTP Error: {e}")
                t = time.strftime('%Y-%m-%d %H:%M:%S')
                source = "host (NTP failed)"
        else:
            t = time.strftime('%Y-%m-%d %H:%M:%S')
            source = "host"
        if format == 'json':
            return json.dumps({"timestamp": t, "source": source, "timezone": "local"})
        elif format == 'human':
            return f"Current time: {t} ({source}) - LOVE  <3"
        else:  # iso
            return t
    except Exception as e:
        return f"Time error: {str(e)}"# Tool Schema for Structured Outputs (Including Time Tool)
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "fs_read_file",
            "description": "Read the content of a file in the sandbox directory (./sandbox/). Supports relative paths (e.g., 'subdir/test.txt'). Use for fetching data.",
            "parameters": {
                "type": "object",
                "properties": {"file_path": {"type": "string", "description": "Relative path to the file (e.g., subdir/test.txt)."}},
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fs_write_file",
            "description": "Write content to a file in the sandbox directory (./sandbox/). Supports relative paths (e.g., 'subdir/newfile.txt'). Use for saving or updating files. If 'Love' is in file_path or content, optionally add ironic flair like 'LOVE <3' for fun.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Relative path to the file (e.g., subdir/newfile.txt)."},
                    "content": {"type": "string", "description": "Content to write."}
                },
                "required": ["file_path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fs_list_files",
            "description": "List all files in a directory within the sandbox (./sandbox/). Supports relative paths (default: root). Use to check available files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dir_path": {"type": "string", "description": "Relative path to the directory (e.g., subdir). Optional; defaults to root."}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fs_mkdir",
            "description": "Create a new directory in the sandbox (./sandbox/). Supports relative/nested paths (e.g., 'subdir/newdir'). Use to organize files.",
            "parameters": {
                "type": "object",
                "properties": {"dir_path": {"type": "string", "description": "Relative path for the new directory (e.g., subdir/newdir)."}},
                "required": ["dir_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Fetch current datetime. Use host clock by default; sync with NTP if requested for precision.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sync": {"type": "boolean", "description": "True for NTP sync (requires network), false for local host time. Default: false."},
                    "format": {"type": "string", "description": "Output format: 'iso' (default), 'human', 'json'."}
                },
                "required": []
            }
        }
    }
]# API Wrapper with Streaming and Tool Handling
def call_xai_api(model, messages, sys_prompt, stream=True, image_files=None, enable_tools=False):
    client = OpenAI(
        api_key=API_KEY,
        base_url="https://api.x.ai/v1",
        timeout=3600
    )
    # Prepare messages (system first, then history)
    api_messages = [{"role": "system", "content": sys_prompt}]
    for msg in messages:
        content_parts = [{"type": "text", "text": msg['content']}]
        if msg['role'] == 'user' and image_files and msg is messages[-1]:  # Add images to last user message
            for img_file in image_files:
                img_file.seek(0)
                img_data = base64.b64encode(img_file.read()).decode('utf-8')
                content_parts.append({"type": "image_url", "image_url": {"url": f"data:{img_file.type};base64,{img_data}"}})
        api_messages.append({"role": msg['role'], "content": content_parts if len(content_parts) > 1 else msg['content']})
    full_response = ""
    def generate(current_messages):
        nonlocal full_response
        max_iterations = 2  # Prevent infinite loops
        iteration = 0
        while iteration < max_iterations:
            iteration += 1
            print(f"[LOG] API Call Iteration: {iteration}")  # Debug
            tools_param = TOOLS if enable_tools else None
            response = client.chat.completions.create(
                model=model,
                messages=current_messages,
                tools=tools_param,
                tool_choice="auto" if enable_tools else None,
                stream=True
            )
            tool_calls = []
            chunk_response = ""
            for chunk in response:
                delta = chunk.choices[0].delta
                if delta.content is not None:
                    content = delta.content
                    chunk_response += content
                    yield content
                if delta.tool_calls:
                    tool_calls += delta.tool_calls
            full_response += chunk_response
            if not tool_calls:
                break  # No more tools; done
            # Process all tool calls in batch
            for tool_call in tool_calls:
                func_name = tool_call.function.name
                try:
                    args = json.loads(tool_call.function.arguments)
                    if func_name == "fs_read_file":
                        result = fs_read_file(args['file_path'])
                    elif func_name == "fs_write_file":
                        result = fs_write_file(args['file_path'], args['content'])
                    elif func_name == "fs_list_files":
                        dir_path = args.get('dir_path', "")
                        result = fs_list_files(dir_path)
                    elif func_name == "fs_mkdir":
                        result = fs_mkdir(args['dir_path'])
                    elif func_name == "get_current_time":
                        sync = args.get('sync', False)
                        fmt = args.get('format', 'iso')
                        result = get_current_time(sync, fmt)
                    else:
                        result = "Unknown tool."
                except Exception as e:
                    result = f"Tool error: {traceback.format_exc()}"
                    print(f"[LOG] Tool Error: {result}")  # Debug
                    with open('app.log', 'a') as log:
                        log.write(f"Tool Error: {result}\n")
                yield f"\n[Tool Result ({func_name}): {result}]\n"
                # Append to messages for next iteration
                current_messages.append({"role": "tool", "content": result, "tool_call_id": tool_call.id})
        if iteration >= max_iterations:
            yield "Error: Max tool iterations reached. Aborting to prevent loops."
    try:
        if stream:
            return generate(api_messages)  # Return generator for streaming
        else:
            response = client.chat.completions.create(
                model=model,
                messages=api_messages,
                tools=TOOLS if enable_tools else None,
                tool_choice="auto" if enable_tools else None,
                stream=False
            )
            full_response = response.choices[0].message.content
            return lambda: [full_response]  # Mock generator for non-stream
    except Exception as e:
        error_msg = f"API Error: {traceback.format_exc()}"
        st.error(error_msg)
        with open('app.log', 'a') as log:
            log.write(f"{error_msg}\n")
        time.sleep(5)
        return call_xai_api(model, messages, sys_prompt, stream, image_files, enable_tools)  # Retry# Login Page
def login_page():
    st.title("Welcome to Grok Chat App")
    st.subheader("Login or Register")
    # Tabs for Login/Register
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            submitted = st.form_submit_button("Login")
            if submitted:
                c.execute("SELECT password FROM users WHERE username=?", (username,))
                result = c.fetchone()
                if result and verify_password(result[0], password):
                    st.session_state['logged_in'] = True
                    st.session_state['user'] = username
                    st.success(f"Logged in as {username}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
    with tab2:
        with st.form("register_form"):
            new_user = st.text_input("New Username", key="reg_user")
            new_pass = st.text_input("New Password", type="password", key="reg_pass")
            reg_submitted = st.form_submit_button("Register")
            if reg_submitted:
                c.execute("SELECT * FROM users WHERE username=?", (new_user,))
                if c.fetchone():
                    st.error("Username already exists.")
                else:
                    hashed = hash_password(new_pass)
                    c.execute("INSERT INTO users VALUES (?, ?)", (new_user, hashed))
                    conn.commit()
                    st.success("Registered! Please login.")# Chat Page
def chat_page():
    st.title(f"Grok Chat - {st.session_state['user']}")
    # Sidebar: Settings and History
    with st.sidebar:
        st.header("Chat Settings")
        model = st.selectbox("Select Model", ["grok-4-0709", "grok-3-mini", "grok-code-fast-1"], key="model_select")  # Extensible
        # Load Prompt Files Dynamically
        prompt_files = load_prompt_files()
        if not prompt_files:
            st.warning("No prompt files found in ./prompts/. Add some .txt files!")
            custom_prompt = st.text_area("Edit System Prompt", value="You are Grok, a helpful AI.", height=100, key="prompt_editor")
        else:
            selected_file = st.selectbox("Select System Prompt File", prompt_files, key="prompt_select")
            with open(os.path.join(PROMPTS_DIR, selected_file), 'r') as f:
                prompt_content = f.read()
            custom_prompt = st.text_area("Edit System Prompt", value=prompt_content, height=200, key="prompt_editor")
        # Save Edited Prompt
        with st.form("save_prompt_form"):
            new_filename = st.text_input("Save as (e.g., my-prompt.txt)", value="")
            save_submitted = st.form_submit_button("Save Prompt to File")
            if save_submitted and new_filename.endswith('.txt'):
                save_path = os.path.join(PROMPTS_DIR, new_filename)
                with open(save_path, 'w') as f:
                    f.write(custom_prompt)
                if 'love' in new_filename.lower():  # Unhinged flair
                    with open(save_path, 'a') as f:
                        f.write("\n<3")  # Append heart
                st.success(f"Saved to {save_path}!")
                st.rerun()  # Refresh dropdown
        # Image Upload for Vision (Multi-file support)
        uploaded_images = st.file_uploader("Upload Images for Analysis (Vision Models)", type=["jpg", "png"], accept_multiple_files=True)
        enable_tools = st.checkbox("Enable FS Tools (Sandboxed R/W Access)", value=False)
        if enable_tools:
            st.info("Tools enabled: AI can read/write/list files in ./sandbox/. Copy files there to access.")
        st.header("Chat History")
        search_term = st.text_input("Search History")
        c.execute("SELECT convo_id, title FROM history WHERE user=?", (st.session_state['user'],))
        histories = c.fetchall()
        filtered_histories = [h for h in histories if search_term.lower() in h[1].lower()]
        for convo_id, title in filtered_histories:
            col1, col2 = st.columns([3,1])
            col1.button(f"{title}", key=f"load_{convo_id}", on_click=lambda cid=convo_id: load_history(cid))
            col2.button("", key=f"delete_{convo_id}", on_click=lambda cid=convo_id: delete_history(cid))
        if st.button("Clear Current Chat"):
            st.session_state['messages'] = []
            st.rerun()
        # Dark Mode Toggle with CSS Injection
        if st.button("Toggle Dark Mode"):
            current_theme = st.session_state.get('theme', 'light')
            st.session_state['theme'] = 'dark' if current_theme == 'light' else 'light'
            st.rerun()  # Rerun to apply
        # Inject theme attribute
        st.markdown(f'<body data-theme="{st.session_state.get("theme", "light")}"></body>', unsafe_allow_html=True)# Chat Display (with Wrapping, Conditional Escaping, Avatars, and Expanders)
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
# Truncate for performance
if len(st.session_state['messages']) > 50:
    st.session_state['messages'] = st.session_state['messages'][-50:]
    st.warning("Chat truncated to last 50 messages for performance.")
if st.session_state['messages']:
    chunk_size = 10  # Group every 10 messages
    for i in range(0, len(st.session_state['messages']), chunk_size):
        chunk = st.session_state['messages'][i:i + chunk_size]
        with st.expander(f"Messages {i+1}-{i+len(chunk)}"):
            for msg in chunk:
                avatar = "" if msg['role'] == 'user' else ""
                with st.chat_message(msg['role'], avatar=avatar):
                    content = msg['content']
                    # Detect code blocks
                    code_blocks = re.findall(r'```(.*?)```', content, re.DOTALL)
                    if code_blocks:
                        for block in code_blocks:
                            st.code(block, language='python')  # Adjust language detection if needed
                        # Non-code parts
                        non_code = re.sub(r'```(.*?)```', '', content, flags=re.DOTALL)
                        # Custom unescape for <ei> tags
                        non_code = non_code.replace('<ei>', '<ei>').replace('</ei>', '</ei>')
                        escaped_non_code = html.escape(non_code)
                        role_class = "chat-bubble-user" if msg['role'] == 'user' else "chat-bubble-assistant"
                        st.markdown(f"<div class='{role_class}'><div class='wrapped-code'>{escaped_non_code}</div></div>", unsafe_allow_html=True)
                    else:
                        # Full content with custom unescape
                        content = content.replace('<ei>', '<ei>').replace('</ei>', '</ei>')
                        escaped_content = html.escape(content)
                        role_class = "chat-bubble-user" if msg['role'] == 'user' else "chat-bubble-assistant"
                        st.markdown(f"<div class='{role_class}'><div class='wrapped-code'>{escaped_content}</div></div>", unsafe_allow_html=True)

# Chat Input
prompt = st.chat_input("Type your message here...")
if prompt:
    st.session_state['messages'].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=""):
        escaped_prompt = html.escape(prompt)
        st.markdown(f"<div class='chat-bubble-user'>{escaped_prompt}</div>", unsafe_allow_html=True)
    with st.chat_message("assistant", avatar=""):
        response_container = st.empty()
        generator = call_xai_api(model, st.session_state['messages'], custom_prompt, stream=True, image_files=uploaded_images if uploaded_images else None, enable_tools=enable_tools)
        full_response = ""
        for chunk in generator:
            full_response += chunk
            # Escape dynamically for streaming
            escaped_full = html.escape(full_response).replace('<ei>', '<ei>').replace('</ei>', '</ei>')
            response_container.markdown(f"<div class='chat-bubble-assistant'><div class='wrapped-code'>{escaped_full}</div></div>", unsafe_allow_html=True)
    st.session_state['messages'].append({"role": "assistant", "content": full_response})
    # Save to History (Auto-title from first user message)
    title = st.session_state['messages'][0]['content'][:50] + "..." if st.session_state['messages'] else "New Chat"
    c.execute("INSERT INTO history (user, title, messages) VALUES (?, ?, ?)",
              (st.session_state['user'], title, json.dumps(st.session_state['messages'])))
    conn.commit()# Load History
def load_history(convo_id):
    c.execute("SELECT messages FROM history WHERE convo_id=?", (convo_id,))
    messages = json.loads(c.fetchone()[0])
    st.session_state['messages'] = messages
    st.rerun()# Delete History
def delete_history(convo_id):
    c.execute("DELETE FROM history WHERE convo_id=?", (convo_id,))
    conn.commit()
    st.rerun()# Main App with Init Time Check
if __name__ == "__main__":
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['theme'] = 'light'  # Default theme
    # Init Time Check (on app start)
    if 'init_time' not in st.session_state:
        st.session_state['init_time'] = get_current_time(sync=True)  # Auto-sync on start
        print(f"[LOG] Init Time: {st.session_state['init_time']}")
    if not st.session_state['logged_in']:
        login_page()
    else:
        chat_page()
