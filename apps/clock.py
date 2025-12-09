import streamlit as st
import streamlit.components.v1 as components
import window_manager

def render():
    st.markdown('<div style="display:none;">', unsafe_allow_html=True)
    if st.button("Close_Clock_Trigger", key="clock_close_btn"):
        window_manager.close_app("Clock")
        st.rerun()
    if st.button("Min_Clock_Trigger", key="clock_min_btn"):
        window_manager.minimize_app("Clock")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    js_code = """
    <script>
    (function() {
        const doc = window.parent.document;
        const WINDOW_ID = 'win11-clock-frame';
        const STORAGE_KEY = 'win11_clock_state';
        
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
            isMaximized: false, restoreX: '100px', restoreY: '100px', restoreW: '350px', restoreH: '250px'
        };

        if (!frame) {
            frame = doc.createElement('div');
            frame.id = WINDOW_ID;
            frame.className = 'win11-window';
            
            Object.assign(frame.style, {
                position: 'fixed', zIndex: '5001', backgroundColor: '#ffffff',
                borderRadius: '8px', boxShadow: '0 10px 30px rgba(0,0,0,0.25), 0 0 0 1px rgba(0,0,0,0.05)',
                display: 'flex', flexDirection: 'column', overflow: 'hidden',
                minWidth: '300px', minHeight: '200px',
                animation: 'fadeIn 0.1s ease-out', fontFamily: '"Segoe UI", sans-serif'
            });

            const header = doc.createElement('div');
            header.id = WINDOW_ID + '-header';
            Object.assign(header.style, {
                height: '32px', background: '#f3f3f3', 
                display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 0 0 10px',
                cursor: 'default', userSelect: 'none'
            });

            const iconMax = `<div style="width:10px; height:10px; border:1px solid #000;"></div>`;
            const iconRestore = `<div style="position:relative; width:10px; height:10px;"><div style="position:absolute; top:-2px; right:-2px; width:8px; height:8px; border:1px solid #000; background:white; z-index:1;"></div><div style="position:absolute; bottom:-2px; left:-2px; width:8px; height:8px; border:1px solid #000; background:transparent; z-index:0;"></div></div>`;

            header.innerHTML = `
                <div style="display:flex; align-items:center; gap:8px; font-size:12px; font-weight:600; color:#444;">
                    <img src="https://img.icons8.com/fluency/48/clock.png" width="16"> Clock
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
                flex: '1', position: 'relative', overflow: 'hidden',
                backgroundColor: '#ffffff', display: 'flex', flexDirection: 'column',
                alignItems: 'center', justifyContent: 'center'
            });
            
            contentBox.innerHTML = `
                <div style="text-align:center; color:#333;">
                    <div id="clk-time" style="font-size:56px; font-weight:300; letter-spacing:2px; line-height:1;">00:00:00</div>
                    <div id="clk-date" style="font-size:18px; color:#666; margin-top:10px; font-weight:500;">Monday, January 1</div>
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
            style.innerHTML = `.win-btn:hover{background:#e5e5e5;} .win-btn-close:hover{background:#e81123;color:white;}`;
            frame.appendChild(style);

            doc.body.appendChild(frame);
        } else {
            if (frame.style.display === 'none') {
                frame.style.display = 'flex';
                frame.style.animation = 'fadeIn 0.1s ease-out';
            }
        }

        const timeEl = frame.querySelector('#clk-time');
        const dateEl = frame.querySelector('#clk-date');
        
        function updateClock() {
            const now = new Date();
            timeEl.innerText = now.toLocaleTimeString('en-US', { hour12: false });
            const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
            dateEl.innerText = now.toLocaleDateString('en-US', options);
        }
        
        updateClock();
        if (!frame.dataset.timerId) {
            const tid = setInterval(updateClock, 1000);
            frame.dataset.timerId = tid;
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
        frame.querySelector(`#${WINDOW_ID}-min`).onclick = (e) => { e.stopPropagation(); frame.style.display='none'; const btn=findButtonByText('Min_Clock_Trigger'); if(btn) btn.click(); };
        frame.querySelector(`#${WINDOW_ID}-close`).onclick = (e) => { e.stopPropagation(); frame.remove(); const btn=findButtonByText('Close_Clock_Trigger'); if(btn) btn.click(); };

        ['Close_Clock_Trigger', 'Min_Clock_Trigger'].forEach(txt => {
            const btn = findButtonByText(txt); if(btn) btn.closest('.stButton').style.display = 'none';
        });

    })();
    </script>
    """
    components.html(js_code, height=0, width=0)