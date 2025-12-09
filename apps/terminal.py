import streamlit as st
import streamlit.components.v1 as components
import window_manager
from datetime import datetime
import html
import json
import random

def init_filesystem():
    """Initializes a fake file system in session state if it doesn't exist."""
    if 'fs_state' not in st.session_state:
        st.session_state.fs_state = {
            "C:": {
                "Users": {
                    "Streamlit": {
                        "Desktop": {
                            "project_ideas.txt": "1. Make a viral OS\n2. ???\n3. Profit",
                            "secret.png": "[Binary Data]"
                        },
                        "Downloads": {
                            "chrome_installer.exe": "[Binary]"
                        },
                        "Documents": {}
                    },
                    "Public": {}
                },
                "Windows": {
                    "System32": {
                        "cmd.exe": "[Binary]",
                        "drivers": {}
                    }
                }
            }
        }
    if 'current_path' not in st.session_state:
        st.session_state.current_path = ["C:", "Users", "Streamlit"]
    if 'term_color' not in st.session_state:
        st.session_state.term_color = "#cccccc"

def get_current_dir_content():
    """Navigates the dictionary based on current_path."""
    d = st.session_state.fs_state
    try:
        for part in st.session_state.current_path:
            d = d[part]
        return d
    except KeyError:
        return None

def format_dir_output(content_dict):
    """Formats the directory listing like Windows CMD."""
    lines = []
    lines.append(f" Directory of {'\\'.join(st.session_state.current_path)}")
    lines.append("")
    
    total_files = 0
    total_dirs = 0
    
    for name, content in content_dict.items():
        dt = datetime.now().strftime("%m/%d/%Y  %I:%M %p")
        if isinstance(content, dict):
            lines.append(f"{dt}    <DIR>          {name}")
            total_dirs += 1
        else:
            size = "{:,}".format(random.randint(100, 50000))
            lines.append(f"{dt}        {str(size).rjust(10)} {name}")
            total_files += 1
            
    lines.append("")
    lines.append(f"              {total_files} File(s)")
    lines.append(f"              {total_dirs} Dir(s)")
    return "\n".join(lines)

def process_command(cmd_str):
    """Processes commands with arguments."""
    init_filesystem()
    
    cmd_str = cmd_str.strip()
    if not cmd_str: return None
    
    parts = cmd_str.split(" ")
    base = parts[0].lower()
    args = parts[1:] if len(parts) > 1 else []
    
    output = ""
    current_loc = get_current_dir_content()
    
    if base in ["help", "?"]:
        output = (
            "Available Commands:\n"
            "-------------------\n"
            "help      : Show this list\n"
            "cls       : Clear screen\n"
            "dir / ls  : List contents\n"
            "cd [dir]  : Change directory (.. to go back)\n"
            "mkdir [name] : Create directory\n"
            "touch [name] : Create empty file\n"
            "rm [name]    : Delete file or folder\n"
            "color [a-f0-9] : Change text color (e.g., 'color 0a')\n"
            "neofetch  : System Info Art\n"
            "ipconfig  : Network Info\n"
            "matrix    : Wake up...\n"
            "date      : Show date\n"
            "echo [txt]: Print text\n"
            "exit      : Close terminal"
        )

    elif base in ["cls", "clear"]:
        st.session_state.term_history = []
        return None

    elif base in ["ls", "dir"]:
        output = format_dir_output(current_loc)

    elif base == "cd":
        if not args:
            output = "\\".join(st.session_state.current_path)
        else:
            target = args[0]
            if target == "..":
                if len(st.session_state.current_path) > 1:
                    st.session_state.current_path.pop()
                else:
                    output = "Access Denied: Already at root."
            elif target in current_loc and isinstance(current_loc[target], dict):
                st.session_state.current_path.append(target)
            else:
                output = "The system cannot find the path specified."

    elif base in ["mkdir", "md"]:
        if not args: output = "usage: mkdir [directory name]"
        elif args[0] in current_loc: output = "A subdirectory or file already exists."
        else: current_loc[args[0]] = {}

    elif base == "touch":
        if not args: output = "usage: touch [filename]"
        else: current_loc[args[0]] = ""

    elif base in ["rm", "del"]:
        if not args: output = "usage: rm [filename]"
        elif args[0] not in current_loc: output = "Could not find file."
        else: del current_loc[args[0]]

    elif base == "whoami":
        output = "streamlitos\\admin"

    elif base == "date":
        output = datetime.now().strftime("Current date: %a %m/%d/%Y")

    elif base == "echo":
        output = " ".join(args)
        
    elif base == "ipconfig":
        output = (
            "\nWindows IP Configuration\n\n"
            "Ethernet adapter Ethernet:\n\n"
            "   Connection-specific DNS Suffix  . : localdomain\n"
            "   IPv6 Address. . . . . . . . . . . : fe80::a1b2:c3d4:e5f6%12\n"
            "   IPv4 Address. . . . . . . . . . . : 192.168.1.42\n"
            "   Subnet Mask . . . . . . . . . . . : 255.255.255.0\n"
            "   Default Gateway . . . . . . . . . : 192.168.1.1"
        )

    elif base == "color":
        colors = {
            "0a": "#00FF00",
            "0c": "#FF0000",
            "0e": "#FFFF00",
            "0b": "#00FFFF",
            "0f": "#FFFFFF",
            "07": "#CCCCCC",
        }
        if args and args[0] in colors:
            st.session_state.term_color = colors[args[0]]
        else:
            output = "Usage: color [0a|0c|0e|0b|0f|07]"

    elif base == "neofetch":
        output = r"""
       .---.        StreamlitOS 11 (Pro)
      /     \       --------------------
      |  O  |       Host: Streamlit Cloud
      |  |  |       Kernel: NT 10.0.22631
      \  \  /       Uptime: 42 mins
       '---'        Shell: PowerShell 7.4.1
                    CPU: Virtual vCPU (2)
      .-----.       Memory: 640KB / 16GB
      '-----'       
        """

    elif base == "matrix":
        st.session_state.term_color = "#00FF00"
        output = "Wake up, Neo...\nThe Matrix has you.\nFollow the white rabbit.\n\nKnock, knock, Neo."

    elif base == "exit":
        window_manager.close_app("Terminal")
        st.rerun()

    else:
        output = f"'{base}' is not recognized as an internal or external command."
        
    return output

def render():
    WINDOW_ID = "win11-terminal-frame"
    init_filesystem()
    
    current_prompt = "\\".join(st.session_state.current_path) + ">"

    if 'term_history' not in st.session_state:
        st.session_state.term_history = [
            "StreamlitOS [Version 11.0.22631.3007]",
            "(c) Microsoft Corporation. All rights reserved.",
            "",
            current_prompt
        ]

    st.markdown("""
        <style>
        div[data-testid="stForm"] { position: absolute; top: -10000px; left: -10000px; opacity: 0; }
        .term-bridge-wrapper { display: none; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="term-bridge-wrapper">', unsafe_allow_html=True)
    if st.button("term_close_trigger", key="term_close_btn"):
        window_manager.close_app("Terminal")
        st.rerun()
    if st.button("term_min_trigger", key="term_min_btn"):
        window_manager.minimize_app("Terminal")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    with st.form(key="terminal_bridge_form", clear_on_submit=True):
        cmd_input = st.text_input("Terminal Command", key="term_cmd_input")
        submit_btn = st.form_submit_button("RunCommand")

        if submit_btn and cmd_input:
            user_cmd = cmd_input
            
            if st.session_state.term_history and st.session_state.term_history[-1].endswith(">"):
                st.session_state.term_history.pop()

            st.session_state.term_history.append(f"{current_prompt} {user_cmd}")
            
            response = process_command(user_cmd)
            
            if response:
                for line in response.split('\n'):
                    st.session_state.term_history.append(line)
            
            new_prompt = "\\".join(st.session_state.current_path) + ">"
            if st.session_state.term_history != []: # don't add if CLS happened
                st.session_state.term_history.append("")
                st.session_state.term_history.append(new_prompt)
            
            st.rerun()

    history_html = ""
    current_prompt_display = "\\".join(st.session_state.current_path) + ">"
    
    for line in st.session_state.term_history:
        if line == current_prompt_display: continue
        safe_line = html.escape(line).replace(" ", "&nbsp;")
        history_html += f"<div class='term-line'>{safe_line}</div>"

    text_color = st.session_state.term_color

    js_code = f"""
    <script>
    (function() {{
        const doc = window.parent.document;
        const WINDOW_ID = '{WINDOW_ID}'; 
        const STORAGE_KEY = 'win11_term_config';
        
        const bringToFront = (targetFrame) => {{
            const allWindows = doc.querySelectorAll('div[class*="win11-window"]');
            let maxZ = 5000;
            allWindows.forEach(w => {{
                const z = parseInt(w.style.zIndex || 0);
                if (z > maxZ) maxZ = z;
            }});
            targetFrame.style.zIndex = maxZ + 1;
        }};

        function findStreamlitButton(textKey) {{
            const buttons = Array.from(doc.querySelectorAll('button'));
            return buttons.find(b => b.innerText.includes(textKey));
        }}

        let frame = doc.getElementById(WINDOW_ID);
        let winState = JSON.parse(sessionStorage.getItem(STORAGE_KEY)) || {{
            isMaximized: false, x: '100px', y: '100px', w: '700px', h: '450px',
            restoreX: '100px', restoreY: '100px', restoreW: '700px', restoreH: '450px'
        }};

        if (!frame) {{
            frame = doc.createElement('div');
            frame.id = WINDOW_ID;
            frame.className = 'win11-window';
            
            Object.assign(frame.style, {{
                position: 'fixed', zIndex: '5005', backgroundColor: '#0c0c0c',
                borderRadius: '8px', boxShadow: '0 0 0 1px #333, 0 20px 50px rgba(0,0,0,0.6)',
                display: 'flex', flexDirection: 'column', overflow: 'hidden',
                minWidth: '350px', minHeight: '200px', animation: 'fadeInTerm 0.15s ease-out',
                fontFamily: 'Consolas, "Cascadia Code", monospace'
            }});
            
            const style = doc.createElement('style');
            style.innerHTML = `
                @keyframes fadeInTerm {{ from {{ opacity:0; transform: scale(0.95); }} to {{ opacity:1; transform: scale(1); }} }}
                .term-btn:hover {{ background-color: #2d2d2d; }}
                .term-btn-close:hover {{ background-color: #e81123; color: white; }}
                .term-scroll::-webkit-scrollbar {{ width: 12px; }}
                .term-scroll::-webkit-scrollbar-track {{ background: #0c0c0c; }}
                .term-scroll::-webkit-scrollbar-thumb {{ background: #444; border: 3px solid #0c0c0c; border-radius: 6px; }}
                .term-scroll::-webkit-scrollbar-thumb:hover {{ background: #555; }}
                .term-line {{ white-space: pre-wrap; word-break: break-all; margin-bottom: 2px; line-height: 1.4; }}
                #term-input-field {{
                    background: transparent; border: none; outline: none; flex: 1; padding: 0; margin: 0;
                    font-family: inherit; font-size: inherit; color: inherit; caret-color: inherit;
                }}
            `;
            frame.appendChild(style);

            frame.innerHTML = `
                <div id="${{WINDOW_ID}}-header" style="height: 32px; background: #1f1f1f; display: flex; align-items: center; justify-content: space-between; user-select: none; border-bottom: 1px solid #111;">
                    <div style="display:flex; align-items:center; gap:10px; padding-left:12px;">
                        <span style="font-size:14px; color:#ccc;">>_</span>
                        <span style="font-size:12px; font-weight:500; color:#fff;">Administrator: PowerShell</span>
                    </div>
                    <div style="display: flex; height: 100%;">
                        <div id="${{WINDOW_ID}}-btn-min" class="term-btn" style="width:46px; display:flex; justify-content:center; align-items:center; cursor:pointer; color:#fff;">&#8212;</div>
                        <div id="${{WINDOW_ID}}-btn-max" class="term-btn" style="width:46px; display:flex; justify-content:center; align-items:center; cursor:pointer; color:#fff;">&#9633;</div>
                        <div id="${{WINDOW_ID}}-btn-close" class="term-btn-close" style="width:46px; display:flex; justify-content:center; align-items:center; cursor:pointer; color:#fff;">&#10005;</div>
                    </div>
                </div>
                <div id="${{WINDOW_ID}}-body" class="term-scroll" style="flex: 1; padding: 8px; overflow-y: auto; overflow-x: hidden; cursor: text;">
                    <div id="${{WINDOW_ID}}-history"></div>
                    <div style="display: flex; flex-direction: row; align-items: flex-start; margin-top: 4px;">
                        <span id="term-prompt-span" style="margin-right: 8px; white-space: nowrap;"></span>
                        <input type="text" id="term-input-field" autocomplete="off" spellcheck="false" autofocus>
                    </div>
                </div>
                <div id="${{WINDOW_ID}}-resizer" style="width: 15px; height: 15px; position: absolute; right: 0; bottom: 0; cursor: se-resize; z-index: 10;"></div>
            `;
            doc.body.appendChild(frame);
        }}

        if(frame.style.display === 'none') frame.style.display = 'flex';

        // --- UPDATE CONTENT (Dynamic Colors & Path) ---
        const bodyDiv = frame.querySelector(`#${{WINDOW_ID}}-body`);
        bodyDiv.style.color = '{text_color}'; 
        
        frame.querySelector(`#${{WINDOW_ID}}-history`).innerHTML = `{history_html}`;
        
        // Update Prompt text
        const promptSpan = frame.querySelector('#term-prompt-span');
        promptSpan.innerText = '{current_prompt_display}';
        promptSpan.style.color = '{text_color}'; // Apply dynamic color to prompt too

        const termInput = frame.querySelector('#term-input-field');
        setTimeout(() => {{ bodyDiv.scrollTop = bodyDiv.scrollHeight; }}, 10);

        bodyDiv.onclick = (e) => {{ if (window.getSelection().toString() === "") termInput.focus(); }};

        // --- RESTORE WINDOW STATE ---
        const applyState = () => {{
            const maxBtn = frame.querySelector(`#${{WINDOW_ID}}-btn-max`);
            if (winState.isMaximized) {{
                Object.assign(frame.style, {{ top: '0', left: '0', width: '100%', height: 'calc(100vh - 48px)', borderRadius: '0' }});
                maxBtn.innerHTML = '&#10697;'; 
            }} else {{
                Object.assign(frame.style, {{ top: winState.y, left: winState.x, width: winState.w, height: winState.h, borderRadius: '8px' }});
                maxBtn.innerHTML = '&#9633;'; 
            }}
            sessionStorage.setItem(STORAGE_KEY, JSON.stringify(winState));
        }};
        applyState();
        bringToFront(frame);
        frame.onmousedown = () => bringToFront(frame);

        // --- DRAG LOGIC ---
        const header = frame.querySelector(`#${{WINDOW_ID}}-header`);
        header.onmousedown = (e) => {{
            if (e.target.closest('.term-btn') || e.target.closest('.term-btn-close') || winState.isMaximized) return;
            e.preventDefault(); bringToFront(frame);
            const startX = e.clientX, startY = e.clientY;
            const rect = frame.getBoundingClientRect();
            const startLeft = rect.left, startTop = rect.top;

            const onMouseMove = (ev) => {{
                frame.style.left = (startLeft + (ev.clientX - startX)) + 'px';
                frame.style.top = (startTop + (ev.clientY - startY)) + 'px';
            }};
            const onMouseUp = () => {{
                doc.removeEventListener('mousemove', onMouseMove);
                doc.removeEventListener('mouseup', onMouseUp);
                winState.x = frame.style.left; winState.y = frame.style.top;
                winState.restoreX = winState.x; winState.restoreY = winState.y;
                applyState();
            }};
            doc.addEventListener('mousemove', onMouseMove);
            doc.addEventListener('mouseup', onMouseUp);
        }};

        // --- RESIZE LOGIC ---
        const resizer = frame.querySelector(`#${{WINDOW_ID}}-resizer`);
        resizer.onmousedown = (e) => {{
            e.stopPropagation(); e.preventDefault(); bringToFront(frame);
            const startX = e.clientX, startY = e.clientY;
            const rect = frame.getBoundingClientRect();
            const startW = rect.width, startH = rect.height;

            const onMouseMove = (ev) => {{
                const newW = startW + (ev.clientX - startX), newH = startH + (ev.clientY - startY);
                if (newW > 300) frame.style.width = newW + 'px';
                if (newH > 200) frame.style.height = newH + 'px';
            }};
            const onMouseUp = () => {{
                doc.removeEventListener('mousemove', onMouseMove);
                doc.removeEventListener('mouseup', onMouseUp);
                winState.w = frame.style.width; winState.h = frame.style.height;
                winState.restoreW = winState.w; winState.restoreH = winState.h;
                applyState();
            }};
            doc.addEventListener('mousemove', onMouseMove);
            doc.addEventListener('mouseup', onMouseUp);
        }};

        // --- BUTTON HANDLERS ---
        frame.querySelector(`#${{WINDOW_ID}}-btn-close`).onclick = (e) => {{
            e.stopPropagation(); frame.remove();
            const btn = findStreamlitButton('term_close_trigger'); if (btn) btn.click();
        }};
        frame.querySelector(`#${{WINDOW_ID}}-btn-min`).onclick = (e) => {{
            e.stopPropagation(); frame.style.display = 'none';
            const btn = findStreamlitButton('term_min_trigger'); if (btn) btn.click();
        }};
        frame.querySelector(`#${{WINDOW_ID}}-btn-max`).onclick = (e) => {{
            e.stopPropagation(); winState.isMaximized = !winState.isMaximized; applyState();
        }};

        // --- SUBMIT LOGIC ---
        termInput.onkeydown = (e) => {{
            if (e.key === 'Enter') {{
                const cmd = termInput.value;
                termInput.value = ""; 
                const bridgeInput = doc.querySelector('input[aria-label="Terminal Command"]');
                if (bridgeInput) {{
                    const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
                    setter.call(bridgeInput, cmd);
                    bridgeInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    setTimeout(() => {{
                         const btn = findStreamlitButton("RunCommand");
                         if (btn) btn.click();
                    }}, 50);
                }}
            }}
        }};
    }})();
    </script>
    """
    components.html(js_code, height=0, width=0)