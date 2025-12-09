import streamlit as st
import streamlit.components.v1 as components
import window_manager

def render():

    st.markdown('<div style="display:none;">', unsafe_allow_html=True)
    if st.button("Close_W_Trigger", key="weather_close_btn"):
        window_manager.close_app("Weather")
        st.rerun()
    if st.button("Min_W_Trigger", key="weather_min_btn"):
        window_manager.minimize_app("Weather")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    js_code = """
    <script>
    (function() {
        const doc = window.parent.document;
        const WINDOW_ID = 'win11-weather-frame';
        const STORAGE_KEY = 'win11_weather_state';
        
        const bringToFront = (targetFrame) => {
            const allWindows = doc.querySelectorAll('div[class*="win11-window"]');
            let maxZ = 1000;
            allWindows.forEach(w => {
                const z = parseInt(w.style.zIndex || 0);
                if (z > maxZ) maxZ = z;
            });
            targetFrame.style.zIndex = maxZ + 1;
        };

        function findButtonByText(text) {
            const buttons = doc.querySelectorAll('button');
            for (const btn of buttons) {
                if (btn.innerText.includes(text)) return btn;
            }
            return null;
        }

        let frame = doc.getElementById(WINDOW_ID);
        
        let winState = JSON.parse(sessionStorage.getItem(STORAGE_KEY)) || {
            isMaximized: false, 
            restoreX: '300px', restoreY: '150px', 
            restoreW: '400px', restoreH: '500px',
            lastCity: '', lastTemp: '', lastDesc: ''
        };

        if (!frame) {
            frame = doc.createElement('div');
            frame.id = WINDOW_ID;
            frame.className = 'win11-window';
            
            Object.assign(frame.style, {
                position: 'fixed', zIndex: '5001', 
                backgroundColor: '#ffffff', // Weather apps are usually light/clean
                borderRadius: '8px', 
                boxShadow: '0 10px 30px rgba(0,0,0,0.25), 0 0 0 1px rgba(0,0,0,0.05)',
                display: 'flex', flexDirection: 'column', overflow: 'hidden',
                minWidth: '320px', minHeight: '400px',
                animation: 'fadeIn 0.1s ease-out', fontFamily: '"Segoe UI", sans-serif'
            });

            const header = doc.createElement('div');
            header.id = WINDOW_ID + '-header';
            Object.assign(header.style, {
                height: '32px', background: '#f9f9f9', 
                display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 0 0 10px',
                cursor: 'default', userSelect: 'none', borderBottom: '1px solid #eee'
            });

            const iconMax = `<div style="width:10px; height:10px; border:1px solid #000;"></div>`;
            const iconRestore = `<div style="position:relative; width:10px; height:10px;"><div style="position:absolute; top:-2px; right:-2px; width:8px; height:8px; border:1px solid #000; background:white; z-index:1;"></div><div style="position:absolute; bottom:-2px; left:-2px; width:8px; height:8px; border:1px solid #000; background:transparent; z-index:0;"></div></div>`;

            header.innerHTML = `
                <div style="display:flex; align-items:center; gap:8px; font-size:12px; font-weight:600; color:#444;">
                    <img src="https://img.icons8.com/fluency/48/weather.png" width="16"> Weather
                </div>
                <div style="display:flex; height:100%;">
                    <div id="${WINDOW_ID}-min" class="win-btn" style="width:46px; display:flex; justify-content:center; align-items:center; cursor:pointer;"><span>&#8212;</span></div>
                    <div id="${WINDOW_ID}-max" class="win-btn" style="width:46px; display:flex; justify-content:center; align-items:center; cursor:pointer;">${winState.isMaximized ? iconRestore : iconMax}</div>
                    <div id="${WINDOW_ID}-close" class="win-btn-close" style="width:46px; display:flex; justify-content:center; align-items:center; cursor:pointer; border-top-right-radius:8px;"><span style="font-size:14px;">&#10005;</span></div>
                </div>
            `;
            frame.appendChild(header);

            const contentBox = doc.createElement('div');
            Object.assign(contentBox.style, { 
                flex: '1', position: 'relative', overflowY: 'auto', padding: '20px',
                backgroundColor: 'linear-gradient(to bottom, #ffffff, #f0f8ff)',
                display: 'flex', flexDirection: 'column', gap: '15px'
            });

            contentBox.innerHTML = `
                <!-- Search Bar -->
                <div style="display:flex; gap:10px;">
                    <input type="text" id="w-input" placeholder="Enter city (e.g. London)" value="${winState.lastCity || ''}" 
                        style="flex:1; padding:8px 12px; border:1px solid #ccc; border-radius:4px; font-family:'Segoe UI'; font-size:14px; outline:none;">
                    <button id="w-btn" style="padding:8px 15px; background:#0067c0; color:white; border:none; border-radius:4px; cursor:pointer; font-weight:600;">Search</button>
                </div>

                <!-- Loading Spinner -->
                <div id="w-loading" style="display:none; text-align:center; padding:20px; color:#666;">
                    Loading weather data...
                </div>

                <!-- Result Display -->
                <div id="w-result" style="display: ${winState.lastTemp ? 'flex' : 'none'}; flex-direction: column; align-items: center; justify-content: center; flex: 1; text-align: center;">
                    <div id="w-city-name" style="font-size: 24px; color: #555; margin-bottom: 5px;">${winState.lastCity}</div>
                    <div style="display:flex; align-items:center; gap:10px;">
                        <img id="w-icon" src="https://img.icons8.com/fluency/96/partly-cloudy-day.png" width="80">
                        <div id="w-temp" style="font-size: 64px; font-weight: 300; color: #222;">${winState.lastTemp}</div>
                    </div>
                    <div id="w-desc" style="font-size: 18px; color: #666; margin-top: -10px; margin-bottom: 20px;">${winState.lastDesc}</div>
                    
                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px; width:100%; margin-top:20px; background:rgba(255,255,255,0.6); padding:15px; border-radius:8px;">
                        <div>
                            <div style="font-size:12px; color:#888;">Wind</div>
                            <div id="w-wind" style="font-weight:600; color:#444;">--</div>
                        </div>
                        <div>
                            <div style="font-size:12px; color:#888;">Elevation</div>
                            <div id="w-elev" style="font-weight:600; color:#444;">--</div>
                        </div>
                    </div>
                </div>
            `;
            frame.appendChild(contentBox);

            const resizer = doc.createElement('div');
            resizer.id = WINDOW_ID + '-resizer';
            Object.assign(resizer.style, {
                width: '15px', height: '15px', position: 'absolute', right: '0', bottom: '0',
                cursor: 'se-resize', zIndex: '510'
            });
            frame.appendChild(resizer);

            const style = doc.createElement('style');
            style.innerHTML = `
                .win-btn:hover{background:#e5e5e5;} 
                .win-btn-close:hover{background:#e81123;color:white;}
                #w-input:focus { border-color: #0067c0; box-shadow: 0 0 0 2px rgba(0,103,192,0.2); }
                #w-btn:hover { background: #005da0; }
                #w-btn:active { transform: scale(0.98); }
            `;
            frame.appendChild(style);

            doc.body.appendChild(frame);
        } else {
            if (frame.style.display === 'none') {
                frame.style.display = 'flex';
                frame.style.animation = 'fadeIn 0.1s ease-out';
            }
        }

        const updateStorage = () => sessionStorage.setItem(STORAGE_KEY, JSON.stringify(winState));
        const applyStyles = () => {
            const maxBtn = frame.querySelector(`#${WINDOW_ID}-max`);
            const iconMax = `<div style="width:10px; height:10px; border:1px solid #000;"></div>`;
            const iconRestore = `<div style="position:relative; width:10px; height:10px;"><div style="position:absolute; top:-2px; right:-2px; width:8px; height:8px; border:1px solid #000; background:white; z-index:1;"></div><div style="position:absolute; bottom:-2px; left:-2px; width:8px; height:8px; border:1px solid #000; background:transparent; z-index:0;"></div></div>`;
            if (winState.isMaximized) {
                Object.assign(frame.style, { top: '0', left: '0', width: '100%', height: 'calc(100vh - 48px)', borderRadius: '0' });
                maxBtn.innerHTML = iconRestore;
            } else {
                Object.assign(frame.style, { top: winState.restoreY, left: winState.restoreX, width: winState.restoreW, height: winState.restoreH, borderRadius: '8px' });
                maxBtn.innerHTML = iconMax;
            }
        };
        applyStyles();
        
        bringToFront(frame);
        frame.onmousedown = () => bringToFront(frame);

        const input = frame.querySelector('#w-input');
        const btn = frame.querySelector('#w-btn');
        const resultBox = frame.querySelector('#w-result');
        const loadingBox = frame.querySelector('#w-loading');

        input.onkeypress = (e) => {
            e.stopPropagation(); // Allow typing
            if (e.key === 'Enter') btn.click();
        };
        
        input.onmousedown = (e) => e.stopPropagation();

        btn.onclick = async (e) => {
            e.stopPropagation();
            const city = input.value.trim();
            if (!city) return;

            resultBox.style.display = 'none';
            loadingBox.style.display = 'block';

            try {
                const geoReq = await fetch(`https://geocoding-api.open-meteo.com/v1/search?name=${city}&count=1&language=en&format=json`);
                const geoData = await geoReq.json();

                if (!geoData.results || geoData.results.length === 0) {
                    alert("City not found!");
                    loadingBox.style.display = 'none';
                    return;
                }

                const { latitude, longitude, name, country } = geoData.results[0];

                const wReq = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current_weather=true`);
                const wData = await wReq.json();
                const current = wData.current_weather;

                const code = current.weathercode;
                let desc = "Clear Sky";
                let icon = "https://img.icons8.com/fluency/96/sun.png";

                if (code > 0 && code <= 3) { desc = "Partly Cloudy"; icon = "https://img.icons8.com/fluency/96/partly-cloudy-day.png"; }
                else if (code >= 45 && code <= 48) { desc = "Foggy"; icon = "https://img.icons8.com/fluency/96/fog-day.png"; }
                else if (code >= 51 && code <= 67) { desc = "Rain"; icon = "https://img.icons8.com/fluency/96/rain.png"; }
                else if (code >= 71 && code <= 77) { desc = "Snow"; icon = "https://img.icons8.com/fluency/96/snow.png"; }
                else if (code >= 80) { desc = "Storm"; icon = "https://img.icons8.com/fluency/96/storm.png"; }

                frame.querySelector('#w-city-name').innerText = `${name}, ${country || ''}`;
                frame.querySelector('#w-temp').innerText = `${current.temperature}°C`;
                frame.querySelector('#w-desc').innerText = desc;
                frame.querySelector('#w-icon').src = icon;
                frame.querySelector('#w-wind').innerText = `${current.windspeed} km/h`;
                frame.querySelector('#w-elev').innerText = `${wData.elevation} m`;

                loadingBox.style.display = 'none';
                resultBox.style.display = 'flex';

                winState.lastCity = city;
                winState.lastTemp = `${current.temperature}°C`;
                winState.lastDesc = desc;
                updateStorage();

            } catch (err) {
                console.error(err);
                alert("Error fetching weather data.");
                loadingBox.style.display = 'none';
            }
        };

        const header = frame.querySelector(`#${WINDOW_ID}-header`);
        const resizer = frame.querySelector(`#${WINDOW_ID}-resizer`);
        let isDragging=false, dragX=0, dragY=0;
        let isResizing=false;

        header.onmousedown = (e) => {
            if(e.target.closest('.win-btn') || e.target.closest('.win-btn-close') || winState.isMaximized) return;
            isDragging=true; dragX=e.clientX - frame.offsetLeft; dragY=e.clientY - frame.offsetTop;
            bringToFront(frame);
        };
        doc.addEventListener('mousemove', (e) => {
            if(isDragging) { e.preventDefault(); frame.style.left=(e.clientX-dragX)+'px'; frame.style.top=(e.clientY-dragY)+'px'; }
            if(isResizing) { e.preventDefault(); frame.style.width=(e.clientX-frame.getBoundingClientRect().left)+'px'; frame.style.height=(e.clientY-frame.getBoundingClientRect().top)+'px'; }
        });
        doc.addEventListener('mouseup', () => {
            if(isDragging) { isDragging=false; winState.restoreX=frame.style.left; winState.restoreY=frame.style.top; updateStorage(); }
            if(isResizing) { isResizing=false; winState.restoreW=frame.style.width; winState.restoreH=frame.style.height; updateStorage(); }
        });

        resizer.onmousedown = (e) => { if(!winState.isMaximized) { isResizing=true; e.stopPropagation(); bringToFront(frame); } };

        frame.querySelector(`#${WINDOW_ID}-max`).onclick = (e) => {
            e.stopPropagation();
            if (!winState.isMaximized) { winState.restoreX = frame.style.left; winState.restoreY = frame.style.top; winState.restoreW = frame.style.width; winState.restoreH = frame.style.height; }
            winState.isMaximized = !winState.isMaximized;
            applyStyles(); updateStorage(); bringToFront(frame);
        };
        frame.querySelector(`#${WINDOW_ID}-min`).onclick = (e) => { e.stopPropagation(); frame.style.display='none'; const btn=findButtonByText('Min_W_Trigger'); if(btn) btn.click(); };
        frame.querySelector(`#${WINDOW_ID}-close`).onclick = (e) => { e.stopPropagation(); frame.remove(); const btn=findButtonByText('Close_W_Trigger'); if(btn) btn.click(); };

        ['Close_W_Trigger', 'Min_W_Trigger'].forEach(txt => {
            const btn = findButtonByText(txt); if(btn) btn.closest('.stButton').style.display = 'none';
        });

    })();
    </script>
    """
    components.html(js_code, height=0, width=0)