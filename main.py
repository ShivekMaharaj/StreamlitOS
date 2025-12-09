import streamlit as st
import streamlit.components.v1 as components 
from datetime import datetime
import styles
import components as ui 
import window_manager
from apps import notepad, calculator, weather, clock, calendar, terminal, apitester

st.set_page_config(page_title="Windows 11 OS", layout="wide", initial_sidebar_state="collapsed")
st.markdown(styles.get_css(), unsafe_allow_html=True)

if 'start_menu_open' not in st.session_state:
    st.session_state.start_menu_open = False
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

window_manager.init_window_state()

def toggle_start():
    st.session_state.start_menu_open = not st.session_state.start_menu_open
    if not st.session_state.start_menu_open:
        st.session_state.search_query = ""

def launch_notepad(): window_manager.open_app("Notepad")
def launch_calculator(): window_manager.open_app("Calculator")
def launch_weather(): window_manager.open_app("Weather")
def launch_clock(): window_manager.open_app("Clock")
def launch_calendar(): window_manager.open_app("Calendar")
def launch_terminal(): window_manager.open_app("Terminal")
def launch_apitester(): window_manager.open_app("APITester")

now = datetime.now()
ui.render_taskbar(now.strftime("%H:%M"), now.strftime("%Y/%m/%d"))

for win in st.session_state.open_windows:
    if not win['minimized']:
        if win['id'] == "Notepad": notepad.render()
        elif win['id'] == "Calculator": calculator.render()
        elif win['id'] == "Weather": weather.render()
        elif win['id'] == "Clock": clock.render()
        elif win['id'] == "Calendar": calendar.render()
        elif win['id'] == "Terminal": terminal.render()
        elif win['id'] == "APITester": apitester.render()

open_ids = [w['id'] for w in st.session_state.open_windows]
js_cleanup = f"""
<script>
    (function() {{
        const openApps = {open_ids}; 
        const idMap = {{
            "Notepad": "win11-notepad-frame", 
            "Calculator": "win11-calc-frame",
            "Weather": "win11-weather-frame",
            "Clock": "win11-clock-frame",
            "Calendar": "win11-calendar-frame",
            "Terminal": "win11-terminal-frame",
            "APITester": "win11-apitester-frame"
        }};
        
        Object.keys(idMap).forEach(appName => {{
            if (!openApps.includes(appName)) {{
                const el = window.parent.document.getElementById(idMap[appName]);
                if (el) el.remove();
            }}
        }});
    }})();
</script>
"""
components.html(js_cleanup, height=0)

if st.session_state.start_menu_open:
    st.text_input("Search Apps", value=st.session_state.search_query, placeholder="Type here to search apps...", key="menu_search")
    if 'menu_search' in st.session_state:
        search_query = st.session_state.menu_search
    else:
        search_query = ""
    ui.render_start_menu(search_query, window_manager)

st.button(" ", key="api_trigger", on_click=launch_apitester)
st.button(" ", key="term_trigger", on_click=launch_terminal)
st.button(" ", key="cal_trigger", on_click=launch_calendar)
st.button(" ", key="clock_trigger", on_click=launch_clock)
st.button(" ", key="weather_trigger", on_click=launch_weather)
st.button(" ", key="calc_trigger", on_click=launch_calculator)
st.button(" ", key="notepad_trigger", on_click=launch_notepad)
st.button(" ", key="start_trigger", on_click=toggle_start)

js_code = """
<script>
    function alignButton(htmlId, btnIndexFromEnd) {
        try {
            const icon = window.parent.document.getElementById(htmlId);
            const buttons = window.parent.document.querySelectorAll('.stButton');
            
            if (!buttons || buttons.length < btnIndexFromEnd) return;

            const triggerBtnDiv = buttons[buttons.length - btnIndexFromEnd];
            
            if (icon && triggerBtnDiv) {
                const rect = icon.getBoundingClientRect();
                triggerBtnDiv.style.position = 'fixed';
                triggerBtnDiv.style.left = rect.left + 'px';
                triggerBtnDiv.style.top = rect.top + 'px';
                triggerBtnDiv.style.width = rect.width + 'px';
                triggerBtnDiv.style.height = rect.height + 'px';
                triggerBtnDiv.style.zIndex = '99999';
                triggerBtnDiv.style.opacity = '0'; 
                triggerBtnDiv.style.cursor = 'pointer';
            }
        } catch (e) { console.log(e); }
    }

    function alignAll() {
        alignButton('start-icon', 1);       
        alignButton('notepad-icon', 2);     
        alignButton('calculator-icon', 3);  
        alignButton('weather-icon', 4);
        alignButton('clock-icon', 5);
        alignButton('calendar-icon', 6);
        alignButton('terminal-icon', 7);
        alignButton('apitester-icon', 8);
    }

    window.addEventListener('resize', alignAll);
    setInterval(alignAll, 500); 
    alignAll(); 
</script>
"""
components.html(js_code, height=0)

if st.session_state.active_window:
    active_id = st.session_state.active_window
    js_focus = f"""
    <script>
    (function() {{
        const activeApp = "{active_id}";
        const idMap = {{
            "Notepad": "win11-notepad-frame",
            "Calculator": "win11-calc-frame",
            "Weather": "win11-weather-frame",
            "Clock": "win11-clock-frame",
            "Calendar": "win11-calendar-frame",
            "Terminal": "win11-terminal-frame",
            "APITester": "win11-apitester-frame"
        }};
        
        const doc = window.parent.document;
        const targetId = idMap[activeApp];
        
        if (targetId) {{
            const el = doc.getElementById(targetId);
            if (el) {{
                const allWindows = doc.querySelectorAll('div[class*="win11-window"]');
                let maxZ = 1000;
                allWindows.forEach(w => {{
                    const z = parseInt(w.style.zIndex || 0);
                    if (z > maxZ) maxZ = z;
                }});
                el.style.zIndex = maxZ + 1;
                
                if (el.style.display === 'none') {{
                    el.style.display = 'flex';
                }}
            }}
        }}
    }})();
    </script>
    """
    components.html(js_focus, height=0)