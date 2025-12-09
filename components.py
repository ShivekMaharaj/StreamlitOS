import streamlit as st
import config
import textwrap

def render_taskbar(time_str, date_str):
    open_apps = [w['id'] for w in st.session_state.get('open_windows', [])]
    active_app = st.session_state.get('active_window', None)

    def get_icon_style(app_name):
        style = ""

        if app_name in open_apps:
            style += " background-color: rgba(255, 255, 255, 0.4); border-bottom: 3px solid #0078d4;"

        if app_name == active_app:
             style += " background-color: rgba(255, 255, 255, 0.6); box-shadow: 0 0 10px rgba(255,255,255,0.3);"
        
        return f'style="{style}"' if style else ''

    taskbar_html = f"""
<div class="taskbar">
<div class="app-icon" id="start-icon" title="Start">
    <img src="https://img.icons8.com/color/48/000000/windows-11.png">
</div>
<div class="search-pill" title="Type here to search">
    <img src="https://img.icons8.com/nolan/64/search.png" style="width: 18px; height: 18px; opacity: 0.7; filter: grayscale(100%);">
    <span class="search-text">Search</span>
</div>

<!-- App Icons with Dynamic Styling & IDs for JS Alignment -->
<div class="app-icon" {get_icon_style('Explorer')} title="Explorer"><img src="https://img.icons8.com/fluency/48/folder-invoices.png"></div>

<div class="app-icon" id="notepad-icon" {get_icon_style('Notepad')} title="Notepad"><img src="https://img.icons8.com/fluency/48/notepad.png"></div>

<div class="app-icon" id="calculator-icon" {get_icon_style('Calculator')} title="Calculator"><img src="https://img.icons8.com/fluency/48/calculator.png"></div>

<div class="app-icon" id="weather-icon" {get_icon_style('Weather')} title="Weather"><img src="https://img.icons8.com/fluency/48/weather.png"></div>

<div class="app-icon" id="clock-icon" {get_icon_style('Clock')} title="Clock"><img src="https://img.icons8.com/fluency/48/clock.png"></div>

<div class="app-icon" id="calendar-icon" {get_icon_style('Calendar')} title="Calendar"><img src="https://img.icons8.com/fluency/48/calendar.png"></div>

<div class="app-icon" id="terminal-icon" {get_icon_style('Terminal')} title="Terminal"><img src="https://img.icons8.com/fluency/48/console.png"></div>

<div class="app-icon" id="apitester-icon" {get_icon_style('APITester')} title="API Tester"><img src="https://img.icons8.com/fluency/48/api-settings.png"></div>

<div class="app-icon" {get_icon_style('Store')} title="Microsoft Store"><img src="https://img.icons8.com/fluency/48/microsoft-store.png"></div>
<div class="app-icon" {get_icon_style('Mail')} title="Mail"><img src="https://img.icons8.com/fluency/48/mail.png"></div>
<div class="app-icon" {get_icon_style('Settings')} title="Settings"><img src="https://img.icons8.com/fluency/48/settings.png"></div>

<div class="system-tray">
    <img class="tray-icon" src="https://img.icons8.com/ios-filled/50/000000/wifi--v1.png">
    <img class="tray-icon" src="https://img.icons8.com/ios-filled/50/000000/medium-volume--v1.png">
    <img class="tray-icon" src="https://img.icons8.com/ios-filled/50/000000/battery.png">
    <div class="clock-box"><span>{time_str}</span><span>{date_str}</span></div>
</div>
</div>
"""
    
    st.markdown(textwrap.dedent(taskbar_html), unsafe_allow_html=True)

def render_start_menu(search_query, window_manager):

    st.markdown("""
    <style>
    div.stButton:not(:last-of-type):not(:nth-last-of-type(2)):not(:nth-last-of-type(3)):not(:nth-last-of-type(4)):not(:nth-last-of-type(5)):not(:nth-last-of-type(6)):not(:nth-last-of-type(7)):not(:nth-last-of-type(8)) {
        position: fixed !important;
        bottom: 120px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        z-index: 905 !important;
        width: auto !important;
    }
    
    div.stButton:not(:last-of-type):not(:nth-last-of-type(2)):not(:nth-last-of-type(3)):not(:nth-last-of-type(4)):not(:nth-last-of-type(5)):not(:nth-last-of-type(6)):not(:nth-last-of-type(7)):not(:nth-last-of-type(8)) button {
        background-color: #0067c0 !important;
        color: white !important;
        border: none !important;
        padding: 8px 20px !important;
        font-weight: 600 !important;
    }

    div.stButton:last-of-type, 
    div.stButton:nth-last-of-type(2), 
    div.stButton:nth-last-of-type(3), 
    div.stButton:nth-last-of-type(4),
    div.stButton:nth-last-of-type(5),
    div.stButton:nth-last-of-type(6),
    div.stButton:nth-last-of-type(7),
    div.stButton:nth-last-of-type(8) {
        position: fixed;
        opacity: 0; 
        z-index: 99999;
    }
    </style>
    """, unsafe_allow_html=True)

    filtered_apps = [app for app in config.ALL_APPS if search_query.lower() in app['name'].lower()]

    apps_html = ""
    for app in filtered_apps:
        apps_html += f"""<div style="text-align:center; cursor:pointer; padding:5px; border-radius:4px;" onmouseover="this.style.background='rgba(255,255,255,0.5)'" onmouseout="this.style.background='transparent'"><img src="{app['icon']}" width="32"><br><span style="font-size:11px; font-family:'Segoe UI'; color:#333; margin-top:5px; display:block;">{app['name']}</span></div>"""
    
    if not filtered_apps:
        apps_html = "<div style='grid-column: span 6; text-align:center; padding:20px; color:#666; font-family: Segoe UI;'>No apps found</div>"

    menu_html = f"""
<div class="start-menu">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; padding:0 5px;">
<h4 style="margin:0; color:#333; font-family:'Segoe UI'; font-weight:600; font-size:14px;">Pinned</h4>
<span style="font-size:12px; color:#0067c0; cursor:pointer; background:#fff; padding:2px 8px; border-radius:4px;">All apps &gt;</span>
</div>
<div style="display: grid; grid-template-columns: repeat(6, 1fr); gap: 15px; padding: 10px 0; overflow-y:auto; max-height:400px;">
{apps_html}
</div>
<div style="height: 60px;"></div>
<div style="margin-top: auto; border-top: 1px solid rgba(0,0,0,0.1); padding-top: 15px; display:flex; align-items:center; padding-left:10px; padding-right:10px;">
<div style="width:30px; height:30px; background:#e0e0e0; border-radius:50%; margin-right:12px; display:flex; align-items:center; justify-content:center;">
<img src="https://img.icons8.com/ios-glyphs/30/555555/user--v1.png" width="16">
</div>
<span style="font-size: 13px; font-weight: 500; font-family:'Segoe UI'; color:#333">User</span>
<div style="margin-left:auto; cursor:pointer; padding:5px; border-radius:4px;" onmouseover="this.style.background='rgba(0,0,0,0.05)'" onmouseout="this.style.background='transparent'">
<img src="https://img.icons8.com/ios-glyphs/30/000000/shutdown.png" width="18" style="opacity:0.8;">
</div>
</div>
</div>
    """
    st.markdown(textwrap.dedent(menu_html), unsafe_allow_html=True)

    if not search_query or "note" in search_query.lower():
        if st.button("📝 Open Notepad", key="btn_open_notepad"):
            window_manager.open_app("Notepad")
            st.rerun()