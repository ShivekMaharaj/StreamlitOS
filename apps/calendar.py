import streamlit as st
import streamlit.components.v1 as components
import window_manager

def render():
    st.markdown('<div style="display:none;">', unsafe_allow_html=True)
    if st.button("Close_Cal_Trigger", key="calendar_close_btn"):
        window_manager.close_app("Calendar")
        st.rerun()
    if st.button("Min_Cal_Trigger", key="calendar_min_btn"):
        window_manager.minimize_app("Calendar")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    js_code = """
    <script>
    (function() {
        const doc = window.parent.document;
        const WINDOW_ID = 'win11-calendar-frame';
        const STORAGE_KEY = 'win11_calendar_state';
        
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
            isMaximized: false, restoreX: '150px', restoreY: '150px', restoreW: '360px', restoreH: '420px'
        };

        if (!frame) {
            frame = doc.createElement('div');
            frame.id = WINDOW_ID;
            frame.className = 'win11-window';
            
            Object.assign(frame.style, {
                position: 'fixed', zIndex: '5001', backgroundColor: '#ffffff',
                borderRadius: '8px', boxShadow: '0 10px 30px rgba(0,0,0,0.25), 0 0 0 1px rgba(0,0,0,0.05)',
                display: 'flex', flexDirection: 'column', overflow: 'hidden',
                minWidth: '300px', minHeight: '350px',
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
                    <img src="https://img.icons8.com/fluency/48/calendar.png" width="16"> Calendar
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
                flex: '1', position: 'relative', overflow: 'hidden', padding: '15px',
                backgroundColor: '#ffffff', display: 'flex', flexDirection: 'column'
            });
            
            contentBox.innerHTML = `
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                    <div id="cal-month-year" style="font-size:18px; font-weight:700; color:#333;">January 2025</div>
                    <div style="display:flex; gap:5px;">
                        <button id="cal-prev" class="cal-nav-btn">&#10094;</button>
                        <button id="cal-next" class="cal-nav-btn">&#10095;</button>
                    </div>
                </div>
                
                <div style="display:grid; grid-template-columns: repeat(7, 1fr); gap:5px; margin-bottom:10px; text-align:center;">
                    <span class="cal-day-head">Su</span><span class="cal-day-head">Mo</span><span class="cal-day-head">Tu</span>
                    <span class="cal-day-head">We</span><span class="cal-day-head">Th</span><span class="cal-day-head">Fr</span><span class="cal-day-head">Sa</span>
                </div>
                
                <div id="cal-grid" style="display:grid; grid-template-columns: repeat(7, 1fr); gap:5px; flex:1;">
                    <!-- JS will fill this -->
                </div>
                
                <div id="cal-selected-date" style="margin-top:15px; border-top:1px solid #eee; padding-top:10px; font-size:13px; color:#666;">
                    No date selected
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
                .cal-nav-btn { background:transparent; border:none; font-size:16px; cursor:pointer; width:30px; height:30px; border-radius:4px; color:#555; }
                .cal-nav-btn:hover { background:#f0f0f0; }
                .cal-day-head { font-size:12px; font-weight:600; color:#666; }
                .cal-cell { 
                    display:flex; justify-content:center; align-items:center; 
                    font-size:14px; cursor:pointer; border-radius:50%; aspect-ratio:1; 
                    transition:background 0.1s; user-select:none;
                }
                .cal-cell:hover { background:#f3f3f3; }
                .cal-cell.today { background:#0078d4; color:white; font-weight:bold; }
                .cal-cell.dim { color:#ccc; }
                .cal-cell.selected { border: 2px solid #0078d4; }
            `;
            frame.appendChild(style);

            doc.body.appendChild(frame);
        } else {
            if (frame.style.display === 'none') {
                frame.style.display = 'flex';
                frame.style.animation = 'fadeIn 0.1s ease-out';
            }
        }

        let currDate = new Date();
        let currMonth = currDate.getMonth();
        let currYear = currDate.getFullYear();
        
        const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        
        const renderCalendar = () => {
            const firstDay = new Date(currYear, currMonth, 1).getDay();
            const daysInMonth = new Date(currYear, currMonth + 1, 0).getDate();
            const prevLastDay = new Date(currYear, currMonth, 0).getDate();
            
            const monthYearEl = frame.querySelector('#cal-month-year');
            const gridEl = frame.querySelector('#cal-grid');
            
            monthYearEl.innerText = `${monthNames[currMonth]} ${currYear}`;
            gridEl.innerHTML = "";
            
            for(let i = firstDay; i > 0; i--) {
                const day = prevLastDay - i + 1;
                gridEl.innerHTML += `<div class="cal-cell dim">${day}</div>`;
            }
            
            const today = new Date();
            for(let i = 1; i <= daysInMonth; i++) {
                let isToday = (i === today.getDate() && currMonth === today.getMonth() && currYear === today.getFullYear()) ? "today" : "";
                gridEl.innerHTML += `<div class="cal-cell ${isToday}" data-day="${i}">${i}</div>`;
            }
            
            const cells = gridEl.querySelectorAll('.cal-cell:not(.dim)');
            cells.forEach(cell => {
                cell.addEventListener('click', (e) => {
                    e.stopPropagation(); // Stop drag
                    // Remove other selected
                    cells.forEach(c => c.classList.remove('selected'));
                    cell.classList.add('selected');
                    
                    const d = cell.getAttribute('data-day');
                    const selDate = new Date(currYear, currMonth, d);
                    frame.querySelector('#cal-selected-date').innerText = "Selected: " + selDate.toDateString();
                });
            });
        };
        
        renderCalendar();
        
        frame.querySelector('#cal-prev').onclick = (e) => {
            e.stopPropagation();
            currMonth--;
            if(currMonth < 0) { currMonth = 11; currYear--; }
            renderCalendar();
        };
        
        frame.querySelector('#cal-next').onclick = (e) => {
            e.stopPropagation();
            currMonth++;
            if(currMonth > 11) { currMonth = 0; currYear++; }
            renderCalendar();
        };

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
            if(e.target.closest('.win-btn') || e.target.closest('.win-btn-close') || winState.isMaximized || e.target.closest('.cal-nav-btn')) return;
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
        frame.querySelector(`#${WINDOW_ID}-min`).onclick = (e) => { e.stopPropagation(); frame.style.display='none'; const btn=findButtonByText('Min_Cal_Trigger'); if(btn) btn.click(); };
        frame.querySelector(`#${WINDOW_ID}-close`).onclick = (e) => { e.stopPropagation(); frame.remove(); const btn=findButtonByText('Close_Cal_Trigger'); if(btn) btn.click(); };

        ['Close_Cal_Trigger', 'Min_Cal_Trigger'].forEach(txt => {
            const btn = findButtonByText(txt); if(btn) btn.closest('.stButton').style.display = 'none';
        });

    })();
    </script>
    """
    components.html(js_code, height=0, width=0)