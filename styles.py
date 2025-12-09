import config

def get_css():
    return f"""
    <style>
        #MainMenu, footer, header {{visibility: hidden;}}
        .block-container {{padding: 0; margin: 0; max-width: 100%; overflow: hidden;}}
        
        .stApp {{
            background-image: url("{config.WALLPAPER_URL}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .taskbar {{
            position: fixed;
            bottom: 0; left: 0; width: 100%; height: 48px;
            background: rgba(243, 243, 243, 0.85);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border-top: 1px solid rgba(255, 255, 255, 0.3);
            display: flex; justify-content: center; align-items: center;
            z-index: 100;
            box-shadow: 0 -4px 20px rgba(0,0,0,0.1);
        }}

        .app-icon {{
            width: 40px; height: 40px; margin: 0 2px;
            border-radius: 4px; display: flex; align-items: center; justify-content: center;
            transition: background 0.2s;
        }}
        .app-icon:hover {{ background-color: rgba(255,255,255,0.6); }}
        .app-icon img {{ width: 24px; height: 24px; object-fit: contain; }}

        .search-pill {{
            width: 130px; height: 32px;
            background-color: rgba(255, 255, 255, 0.6);
            border-radius: 18px; display: flex; align-items: center;
            padding-left: 10px; margin: 0 6px; border: 1px solid rgba(0,0,0,0.05);
        }}
        .search-text {{
            font-family: "Segoe UI", sans-serif; font-size: 13px; color: #555; margin-left: 8px; padding-top: 2px;
        }}

        .system-tray {{
            position: absolute; right: 0; top: 0; height: 48px;
            display: flex; align-items: center; padding-right: 15px;
        }}
        .tray-icon {{ width: 18px; height: 18px; margin: 0 8px; opacity: 0.7; }}
        
        .clock-box {{
            display: flex; flex-direction: column; align-items: flex-end;
            margin-left: 10px; font-family: "Segoe UI", sans-serif; font-size: 12px; color: #333;
            line-height: 14px;
        }}

        .start-menu {{
            position: fixed;
            bottom: 60px; left: 50%;
            transform: translateX(-50%);
            width: 640px; height: 600px;
            background: rgba(245, 245, 245, 0.90);
            backdrop-filter: blur(30px);
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.5);
            box-shadow: 0 0 25px rgba(0,0,0,0.25);
            z-index: 900;
            padding: 30px;
            padding-top: 75px; 
            display: flex; flex-direction: column;
            animation: popUp 0.2s cubic-bezier(0.1, 0.9, 0.2, 1);
        }}
        
        @keyframes popUp {{
            from {{ transform: translate(-50%, 40px); opacity: 0; }}
            to {{ transform: translate(-50%, 0); opacity: 1; }}
        }}

        div.stButton:last-of-type, div.stButton:nth-last-of-type(2) {{
            position: fixed !important;
            z-index: 99999 !important;
            margin: 0 !important;
            left: 50%; /* Default center if JS fails */
            bottom: 4px;
        }}

        div.stButton:last-of-type > button, div.stButton:nth-last-of-type(2) > button {{
            background-color: transparent !important;
            border: none !important;
            color: transparent !important;
            padding: 0 !important;
            cursor: default !important;
            height: 40px; 
            width: 40px;
        }}
        
        div[data-testid="stTextInput"] {{
            position: fixed;
            bottom: 605px; 
            left: 50%;
            transform: translateX(-50%);
            width: 580px !important;
            z-index: 902;
        }}
        
        div[data-testid="stTextInput"] input {{
            background-color: #fbfbfb !important;
            border: 1px solid #ccc !important;
            border-bottom: 2px solid #0067c0 !important;
            border-radius: 4px !important;
            color: #333 !important;
            font-family: "Segoe UI" !important;
            padding-left: 15px !important;
        }}
        
        label[data-testid="stWidgetLabel"] {{ display: none; }}
        .stTooltipIcon {{ display: none !important; }}
    </style>
    """