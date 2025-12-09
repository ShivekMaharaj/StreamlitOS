import streamlit as st
import streamlit.components.v1 as components
import window_manager
import requests
import json
import time
from datetime import datetime
import html

def send_request(method, url, headers_str, body_str):
    """
    Executes the HTTP request using Python's requests library.
    Returns a dict with status, time, and content.
    """
    start_time = time.time()
    
    headers = {}
    if headers_str.strip():
        try:
            headers = json.loads(headers_str)
        except:
            return {"status": "Error", "time": "0ms", "body": "Invalid JSON in Headers"}

    data = None
    if method in ["POST", "PUT", "PATCH"] and body_str.strip():
        try:
            data = json.loads(body_str)
        except:
            return {"status": "Error", "time": "0ms", "body": "Invalid JSON in Body. Please ensure valid JSON format."}

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=10)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=10)
        elif method == "PATCH":
            response = requests.patch(url, headers=headers, json=data, timeout=10)
        else:
            return {"status": "Error", "time": "0ms", "body": "Method not supported"}

        elapsed = int((time.time() - start_time) * 1000)
        
        try:
            resp_body = json.dumps(response.json(), indent=2)
        except:
            resp_body = response.text

        return {
            "status": f"{response.status_code} {response.reason}",
            "code": response.status_code,
            "time": f"{elapsed} ms",
            "body": resp_body
        }

    except requests.exceptions.RequestException as e:
        return {"status": "Connection Error", "code": 0, "time": "0 ms", "body": str(e)}
    except Exception as e:
        return {"status": "System Error", "code": 0, "time": "0 ms", "body": str(e)}

def render():
    WINDOW_ID = "win11-apitester-frame"

    if 'api_history' not in st.session_state:
        st.session_state.api_history = [] 
    if 'api_last_response' not in st.session_state:
        st.session_state.api_last_response = None
    if 'api_form_defaults' not in st.session_state:
        st.session_state.api_form_defaults = {
            "method": "GET",
            "url": "https://jsonplaceholder.typicode.com/todos/1",
            "headers": '{"Content-Type": "application/json"}',
            "body": "{}"
        }

    st.markdown("""
        <style>
        div[data-testid="stForm"] { position: absolute; top: -10000px; left: -10000px; opacity: 0; }
        .api-bridge-wrapper { display: none; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="api-bridge-wrapper">', unsafe_allow_html=True)
    if st.button("api_close_trigger", key="api_close_btn"):
        window_manager.close_app("APITester")
        st.rerun()
    if st.button("api_min_trigger", key="api_min_btn"):
        window_manager.minimize_app("APITester")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    with st.form(key="api_bridge_form"):
        b_method = st.text_input("b_method", key="bridge_method")
        b_url = st.text_input("b_url", key="bridge_url")
        b_headers = st.text_input("b_headers", key="bridge_headers")
        b_body = st.text_input("b_body", key="bridge_body")
        b_submit = st.form_submit_button("APISend")

        if b_submit:
            st.session_state.api_form_defaults["method"] = b_method
            st.session_state.api_form_defaults["url"] = b_url
            st.session_state.api_form_defaults["headers"] = b_headers
            st.session_state.api_form_defaults["body"] = b_body

            if b_url:
                hist_item = {"method": b_method, "url": b_url, "timestamp": datetime.now().strftime("%H:%M:%S")}
                if not st.session_state.api_history or st.session_state.api_history[0]["url"] != b_url:
                    st.session_state.api_history.insert(0, hist_item)
            
            response_data = send_request(b_method, b_url, b_headers, b_body)
            st.session_state.api_last_response = response_data
            st.rerun()

    defaults = st.session_state.api_form_defaults
    last_resp = st.session_state.api_last_response
    
    def safe_json(val):
        return json.dumps(val).replace('</script>', '<\\/script>')

    js_defaults = safe_json(defaults)
    js_response = safe_json(last_resp)
    js_history = safe_json(st.session_state.api_history)

    js_code = f"""
    <script>
    (function() {{
        const doc = window.parent.document;
        const WINDOW_ID = '{WINDOW_ID}';
        const STORAGE_KEY = 'win11_api_config';

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

        function findStreamlitInput(labelKey) {{
             const inputs = Array.from(doc.querySelectorAll('input[type="text"]'));
             return inputs.find(i => i.getAttribute('aria-label') === labelKey);
        }}

        let frame = doc.getElementById(WINDOW_ID);
        let winState = JSON.parse(sessionStorage.getItem(STORAGE_KEY)) || {{
            isMaximized: false, x: '80px', y: '50px', w: '900px', h: '600px',
            restoreX: '80px', restoreY: '50px', restoreW: '900px', restoreH: '600px'
        }};

        if (!frame) {{
            frame = doc.createElement('div');
            frame.id = WINDOW_ID;
            frame.className = 'win11-window';
            
            Object.assign(frame.style, {{
                position: 'fixed', zIndex: '5006', backgroundColor: '#1e1e1e',
                borderRadius: '8px', boxShadow: '0 0 0 1px #333, 0 20px 50px rgba(0,0,0,0.6)',
                display: 'flex', flexDirection: 'column', overflow: 'hidden',
                minWidth: '500px', minHeight: '400px', animation: 'fadeInApi 0.2s ease-out',
                fontFamily: '"Segoe UI", sans-serif', color: '#e0e0e0'
            }});
            
            frame.innerHTML = `
                <div id="${{WINDOW_ID}}-header" class="api-header">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <img src="https://img.icons8.com/color/48/api-settings.png" width="18">
                        <span style="font-size:12px;">APITester</span>
                    </div>
                    <div style="display: flex; height: 100%;">
                        <div id="${{WINDOW_ID}}-min" class="api-btn-ctrl">&#8212;</div>
                        <div id="${{WINDOW_ID}}-max" class="api-btn-ctrl">&#9633;</div>
                        <div id="${{WINDOW_ID}}-close" class="api-btn-ctrl api-btn-close">&#10005;</div>
                    </div>
                </div>
                
                <div class="api-body">
                    <!-- SIDEBAR -->
                    <div class="api-sidebar">
                        <div style="padding:10px; font-size:11px; font-weight:bold; color:#777; text-transform:uppercase;">History</div>
                        <div id="api-hist-list"></div>
                    </div>
                    
                    <!-- MAIN -->
                    <div class="api-main">
                        <!-- URL BAR -->
                        <div class="api-bar">
                            <select id="api-method" class="api-select">
                                <option value="GET">GET</option>
                                <option value="POST">POST</option>
                                <option value="PUT">PUT</option>
                                <option value="PATCH">PATCH</option>
                                <option value="DELETE">DELETE</option>
                            </select>
                            <input type="text" id="api-url" class="api-input" style="flex:1;" placeholder="Enter Request URL">
                            <button id="api-send" class="api-send-btn">Send</button>
                        </div>
                        
                        <!-- TABS -->
                        <div class="api-tabs">
                            <div class="api-tab active" data-tab="params">Headers</div>
                            <div class="api-tab" data-tab="body">Body (JSON)</div>
                        </div>
                        
                        <!-- INPUT AREA -->
                        <div id="tab-params" class="api-editor-area show">
                            <textarea id="api-headers" class="api-textarea" placeholder='{{"Content-Type": "application/json"}}'></textarea>
                        </div>
                        <div id="tab-body" class="api-editor-area">
                            <textarea id="api-body" class="api-textarea" placeholder='{{ "key": "value" }}'></textarea>
                        </div>
                        
                        <!-- RESPONSE AREA -->
                        <div class="api-response-area">
                            <div class="api-res-header">
                                <div>Status: <span id="api-status-badge" class="api-badge" style="background:#333;">Wait</span></div>
                                <div style="color:#888;">Time: <span id="api-time">0 ms</span></div>
                            </div>
                            <textarea id="api-response-text" class="api-textarea" style="padding:10px; background:#1e1e1e; font-size:12px;" readonly></textarea>
                        </div>
                    </div>
                </div>
                <div id="${{WINDOW_ID}}-resizer" style="width: 15px; height: 15px; position: absolute; right: 0; bottom: 0; cursor: se-resize; z-index: 10;"></div>
            `;
            
            const style = doc.createElement('style');
            style.innerHTML = `
                @keyframes fadeInApi {{ from {{ opacity:0; transform: translateY(10px); }} to {{ opacity:1; transform: translateY(0); }} }}
                .api-header {{ height: 40px; background: #252526; display: flex; align-items: center; justify-content: space-between; padding-left: 10px; border-bottom: 1px solid #333; }}
                .api-btn-ctrl {{ width: 46px; height: 100%; display: flex; justify-content: center; align-items: center; cursor: pointer; color: #ccc; }}
                .api-btn-ctrl:hover {{ background: #333; }}
                .api-btn-close:hover {{ background: #e81123; color: white; }}
                
                .api-body {{ flex: 1; display: flex; overflow: hidden; height: calc(100% - 40px); }}
                .api-sidebar {{ width: 200px; background: #252526; border-right: 1px solid #333; overflow-y: auto; display: flex; flex-direction: column; }}
                .api-main {{ flex: 1; display: flex; flex-direction: column; background: #1e1e1e; overflow: hidden; }}
                
                .api-bar {{ padding: 10px; display: flex; gap: 10px; border-bottom: 1px solid #333; align-items: center; }}
                .api-input {{ background: #3c3c3c; border: 1px solid #3c3c3c; color: white; padding: 8px; border-radius: 4px; outline: none; }}
                .api-input:focus {{ border-color: #007fd4; }}
                .api-select {{ background: #3c3c3c; color: white; padding: 8px; border-radius: 4px; border: none; outline: none; font-weight: bold; cursor: pointer; }}
                
                .api-send-btn {{ background: #007fd4; color: white; border: none; padding: 0 20px; border-radius: 4px; font-weight: 600; cursor: pointer; }}
                .api-send-btn:hover {{ background: #0060a0; }}
                
                .api-tabs {{ display: flex; gap: 20px; padding: 10px 15px; border-bottom: 1px solid #333; font-size: 13px; color: #999; cursor: pointer; }}
                .api-tab.active {{ color: #fff; border-bottom: 2px solid #007fd4; padding-bottom: 8px; }}
                
                .api-editor-area {{ flex: 1; padding: 10px; display: none; flex-direction: column; }}
                .api-editor-area.show {{ display: flex; }}
                .api-textarea {{ flex: 1; background: #1e1e1e; border: none; color: #d4d4d4; font-family: 'Consolas', monospace; resize: none; outline: none; }}
                
                .api-response-area {{ height: 40%; border-top: 5px solid #333; display: flex; flex-direction: column; }}
                .api-res-header {{ padding: 5px 15px; background: #252526; display: flex; justify-content: space-between; align-items: center; font-size: 12px; }}
                .api-badge {{ padding: 2px 6px; border-radius: 4px; font-weight: bold; }}
                
                .hist-item {{ padding: 8px 10px; border-bottom: 1px solid #333; cursor: pointer; font-size: 12px; }}
                .hist-item:hover {{ background: #2a2d2e; }}
                .method-GET {{ color: #61affe; }}
                .method-POST {{ color: #49cc90; }}
                .method-PUT {{ color: #fca130; }}
                .method-DELETE {{ color: #f93e3e; }}
            `;
            frame.appendChild(style);
            doc.body.appendChild(frame);
            
        }} else {{
            if(frame.style.display === 'none') frame.style.display = 'flex';
        }}

        const defaults = {js_defaults};
        const lastResp = {js_response};
        const history = {js_history};

        const elMethod = frame.querySelector('#api-method');
        const elUrl = frame.querySelector('#api-url');
        const elHeaders = frame.querySelector('#api-headers');
        const elBody = frame.querySelector('#api-body');
        const elResText = frame.querySelector('#api-response-text');
        const elStatus = frame.querySelector('#api-status-badge');
        const elTime = frame.querySelector('#api-time');
        const listHist = frame.querySelector('#api-hist-list');

        elMethod.value = defaults.method;
        elUrl.value = defaults.url;
        elHeaders.value = defaults.headers;
        elBody.value = defaults.body;

        // Populate Response
        if (lastResp) {{
            elResText.value = lastResp.body;
            elStatus.innerText = lastResp.status;
            elTime.innerText = lastResp.time;
            
            const code = lastResp.code || 0;
            if (code >= 200 && code < 300) {{ elStatus.style.background = '#198754'; elStatus.style.color = 'white'; }}
            else if (code >= 400) {{ elStatus.style.background = '#dc3545'; elStatus.style.color = 'white'; }}
            else {{ elStatus.style.background = '#ffc107'; elStatus.style.color = 'black'; }}
        }}

        listHist.innerHTML = '';
        history.forEach(h => {{
            const div = doc.createElement('div');
            div.className = 'hist-item';
            div.innerHTML = `<span class="method-${{h.method}}">${{h.method}}</span> <span style="color:#aaa;">${{h.url}}</span>`;
            div.onclick = () => {{
                elMethod.value = h.method;
                elUrl.value = h.url;
            }};
            listHist.appendChild(div);
        }});

        const tabs = frame.querySelectorAll('.api-tab');
        tabs.forEach(t => {{
            t.onclick = () => {{
                tabs.forEach(x => x.classList.remove('active'));
                t.classList.add('active');
                
                const target = t.getAttribute('data-tab');
                frame.querySelector('#tab-params').classList.remove('show');
                frame.querySelector('#tab-body').classList.remove('show');
                
                if(target === 'params') frame.querySelector('#tab-params').classList.add('show');
                if(target === 'body') frame.querySelector('#tab-body').classList.add('show');
            }};
        }});

        frame.querySelector('#api-send').onclick = () => {{
            elStatus.innerText = "Sending...";
            elStatus.style.background = "#007fd4";
            elResText.value = "Waiting for response...";
            
            const fill = (ariaKey, val) => {{
                const inp = findStreamlitInput(ariaKey);
                if(inp) {{
                    const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
                    setter.call(inp, val);
                    inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
            }};

            fill('b_method', elMethod.value);
            fill('b_url', elUrl.value);
            fill('b_headers', elHeaders.value);
            fill('b_body', elBody.value);

            setTimeout(() => {{
                const btn = findStreamlitButton("APISend");
                if(btn) btn.click();
            }}, 100);
        }};

        const header = frame.querySelector(`#${{WINDOW_ID}}-header`);
        bringToFront(frame);
        frame.onmousedown = () => bringToFront(frame);

        const saveState = () => {{
            sessionStorage.setItem(STORAGE_KEY, JSON.stringify(winState));
        }};
        
        const applyState = () => {{
            const maxBtn = frame.querySelector(`#${{WINDOW_ID}}-max`);
             if (winState.isMaximized) {{
                Object.assign(frame.style, {{ top: '0', left: '0', width: '100%', height: 'calc(100vh - 48px)', borderRadius: '0' }});
                maxBtn.innerHTML = '&#10697;';
            }} else {{
                Object.assign(frame.style, {{ top: winState.y, left: winState.x, width: winState.w, height: winState.h, borderRadius: '8px' }});
                maxBtn.innerHTML = '&#9633;';
            }}
        }};
        applyState();

        header.onmousedown = (e) => {{
            if(e.target.closest('.api-btn-ctrl') || winState.isMaximized) return;
            e.preventDefault(); bringToFront(frame);
            const startX = e.clientX, startY = e.clientY;
            const rect = frame.getBoundingClientRect();
            const startLeft = rect.left, startTop = rect.top;
            
            const onMove = (ev) => {{
                frame.style.left = (startLeft + (ev.clientX - startX)) + 'px';
                frame.style.top = (startTop + (ev.clientY - startY)) + 'px';
            }};
            const onUp = () => {{
                doc.removeEventListener('mousemove', onMove); doc.removeEventListener('mouseup', onUp);
                winState.x = frame.style.left; winState.y = frame.style.top; saveState();
            }};
            doc.addEventListener('mousemove', onMove); doc.addEventListener('mouseup', onUp);
        }};

        const resizer = frame.querySelector(`#${{WINDOW_ID}}-resizer`);
        resizer.onmousedown = (e) => {{
            e.stopPropagation(); e.preventDefault(); bringToFront(frame);
            const startX = e.clientX, startY = e.clientY;
            const rect = frame.getBoundingClientRect();
            const startW = rect.width, startH = rect.height;
            
            const onMove = (ev) => {{
                frame.style.width = Math.max(400, startW + (ev.clientX - startX)) + 'px';
                frame.style.height = Math.max(300, startH + (ev.clientY - startY)) + 'px';
            }};
            const onUp = () => {{
                doc.removeEventListener('mousemove', onMove); doc.removeEventListener('mouseup', onUp);
                winState.w = frame.style.width; winState.h = frame.style.height; saveState();
            }};
            doc.addEventListener('mousemove', onMove); doc.addEventListener('mouseup', onUp);
        }};

        frame.querySelector(`#${{WINDOW_ID}}-close`).onclick = (e) => {{ e.stopPropagation(); frame.remove(); const btn = findStreamlitButton('api_close_trigger'); if(btn) btn.click(); }};
        frame.querySelector(`#${{WINDOW_ID}}-min`).onclick = (e) => {{ e.stopPropagation(); frame.style.display='none'; const btn = findStreamlitButton('api_min_trigger'); if(btn) btn.click(); }};
        frame.querySelector(`#${{WINDOW_ID}}-max`).onclick = (e) => {{ e.stopPropagation(); winState.isMaximized = !winState.isMaximized; applyState(); saveState(); }};

    }})();
    </script>
    """
    components.html(js_code, height=0, width=0)