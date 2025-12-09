import streamlit as st
import streamlit.components.v1 as components
import window_manager

def render():
    if 'notepad_content' not in st.session_state:
        st.session_state.notepad_content = ""

    with st.container():
        st.markdown('<div id="notepad-anchor"></div>', unsafe_allow_html=True)
        content = st.text_area("Content", value=st.session_state.notepad_content, label_visibility="collapsed", key="notepad_area", height=600)
        st.session_state.notepad_content = content

        col_h1, col_h2 = st.columns(2)
        with col_h1:
            if st.button("Close_Hidden_Trigger", key="notepad_close_btn"):
                window_manager.close_app("Notepad")
                st.rerun()
        with col_h2:
            if st.button("Minimize_Hidden_Trigger", key="notepad_min_btn"):
                window_manager.minimize_app("Notepad")
                st.rerun()

    js_code = """
    <script>
    (function() {
        const doc = window.parent.document;
        const WINDOW_ID = 'win11-notepad-frame';
        const STORAGE_KEY = 'win11_notepad_state';
        
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
            isMaximized: false, restoreX: '200px', restoreY: '100px', restoreW: '600px', restoreH: '450px'
        };

        if (!frame) {
            frame = doc.createElement('div');
            frame.id = WINDOW_ID;
            frame.className = 'win11-window';
            
            Object.assign(frame.style, {
                position: 'fixed', zIndex: '5001', backgroundColor: '#ffffff',
                borderRadius: '8px', boxShadow: '0 10px 30px rgba(0,0,0,0.2), 0 0 0 1px rgba(0,0,0,0.05)',
                display: 'flex', flexDirection: 'column', overflow: 'hidden',
                minWidth: '350px', minHeight: '250px',
                animation: 'fadeIn 0.1s ease-out', fontFamily: '"Segoe UI", sans-serif'
            });

            const iconMax = `<div style="width:10px; height:10px; border:1px solid #000;"></div>`;
            const iconRestore = `<div style="position:relative; width:10px; height:10px;"><div style="position:absolute; top:-2px; right:-2px; width:8px; height:8px; border:1px solid #000; background:white; z-index:1;"></div><div style="position:absolute; bottom:-2px; left:-2px; width:8px; height:8px; border:1px solid #000; background:transparent; z-index:0;"></div></div>`;

            frame.innerHTML = `
                <div id="${WINDOW_ID}-header" style="height: 32px; background: #f0f0f0; display: flex; align-items: center; justify-content: space-between; padding-left: 15px; cursor: default; user-select: none;">
                    <div style="display:flex; align-items:center; gap:10px; pointer-events:none;">
                        <img src="https://img.icons8.com/fluency/48/notepad.png" width="16">
                        <span style="font-size:12px; color:#333;">Untitled - Notepad</span>
                    </div>
                    <div style="display:flex; height:100%;">
                        <div id="${WINDOW_ID}-min" class="win-btn" style="width:46px; display:flex; justify-content:center; align-items:center; cursor:pointer;"><span>&#8212;</span></div>
                        <div id="${WINDOW_ID}-max" class="win-btn" style="width:46px; display:flex; justify-content:center; align-items:center; cursor:pointer;">${winState.isMaximized ? iconRestore : iconMax}</div>
                        <div id="${WINDOW_ID}-close" class="win-btn-close" style="width:46px; display:flex; justify-content:center; align-items:center; cursor:pointer; border-top-right-radius:8px;"><span style="font-size:14px;">&#10005;</span></div>
                    </div>
                </div>
                <div id="${WINDOW_ID}-menu" style="height: 28px; background: #ffffff; display: flex; align-items: center; padding: 0 10px; border-bottom: 1px solid #e5e5e5; fontSize: 12px; color: #333; gap: 15px;">
                    <span style="cursor:pointer;" id="${WINDOW_ID}-save-btn">Save As</span>
                    <span style="cursor:pointer;">Edit</span>
                    <span style="cursor:pointer;">View</span>
                </div>
                <div id="${WINDOW_ID}-content" style="flex: 1; position: relative; background: white; display: flex; flexDirection: column;"></div>
                <div id="${WINDOW_ID}-resizer" style="width: 15px; height: 15px; position: absolute; right: 0; bottom: 0; cursor: se-resize; zIndex: 510;"></div>
            `;
            
            const style = doc.createElement('style');
            style.innerHTML = `.win-btn:hover { background-color: #e5e5e5; } .win-btn-close:hover { background-color: #e81123; color: white; }`;
            frame.appendChild(style);
            doc.body.appendChild(frame);
        } else {
             if (frame.style.display === 'none') {
                frame.style.display = 'flex';
                frame.style.animation = 'none'; frame.offsetHeight; frame.style.animation = 'fadeIn 0.1s ease-out';
            }
        }
        
        bringToFront(frame);

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

        frame.onmousedown = () => bringToFront(frame);

        const header = frame.querySelector(`#${WINDOW_ID}-header`);
        let isDragging = false, dragX = 0, dragY = 0;
        
        header.onmousedown = (e) => {
            if(e.target.closest('.win-btn') || e.target.closest('.win-btn-close') || winState.isMaximized) return;
            isDragging = true; 
            dragX = e.clientX - frame.getBoundingClientRect().left; 
            dragY = e.clientY - frame.getBoundingClientRect().top;
            bringToFront(frame);
        };

        doc.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            e.preventDefault(); 
            frame.style.left = (e.clientX - dragX) + 'px'; 
            frame.style.top = (e.clientY - dragY) + 'px';
        });

        doc.addEventListener('mouseup', () => { 
            if (isDragging) { 
                isDragging = false; 
                winState.restoreX = frame.style.left; 
                winState.restoreY = frame.style.top; 
                updateStorage(); 
            }
        });

        frame.querySelector(`#${WINDOW_ID}-max`).onclick = (e) => {
            e.stopPropagation();
            if (!winState.isMaximized) {
                winState.restoreX = frame.style.left; winState.restoreY = frame.style.top;
                winState.restoreW = frame.style.width; winState.restoreH = frame.style.height;
            }
            winState.isMaximized = !winState.isMaximized;
            applyStyles(); updateStorage(); bringToFront(frame);
        };
        frame.querySelector(`#${WINDOW_ID}-min`).onclick = (e) => { 
            e.stopPropagation(); frame.style.display = 'none'; 
            const btn = findButtonByText('Minimize_Hidden_Trigger'); if(btn) btn.click();
        };
        frame.querySelector(`#${WINDOW_ID}-close`).onclick = (e) => { 
            e.stopPropagation(); frame.remove(); 
            const btn = findButtonByText('Close_Hidden_Trigger'); if(btn) btn.click();
        };

        const resizer = frame.querySelector(`#${WINDOW_ID}-resizer`);
        let isResizing = false;
        resizer.onmousedown = (e) => { 
            if(!winState.isMaximized) { 
                isResizing = true; e.stopPropagation(); bringToFront(frame);
            } 
        };
        doc.addEventListener('mousemove', (e) => {
            if(isResizing) { 
                e.preventDefault(); 
                frame.style.width = (e.clientX - frame.getBoundingClientRect().left) + 'px'; 
                frame.style.height = (e.clientY - frame.getBoundingClientRect().top) + 'px'; 
            }
        });
        doc.addEventListener('mouseup', () => { 
            if(isResizing) { 
                isResizing = false; 
                winState.restoreW = frame.style.width; 
                winState.restoreH = frame.style.height; 
                updateStorage(); 
            }
        });

        frame.querySelector(`#${WINDOW_ID}-save-btn`).onclick = () => {
            const ta = frame.querySelector('textarea');
            if (!ta) return;
            const blob = new Blob([ta.value], { type: 'text/plain' });
            const url = window.URL.createObjectURL(blob);
            const a = doc.createElement('a'); a.style.display='none'; a.href=url; a.download='MyNote.txt';
            doc.body.appendChild(a); a.click(); window.URL.revokeObjectURL(url); doc.body.removeChild(a);
        };

        const anchor = doc.getElementById('notepad-anchor');
        if (anchor) {
            const allTextAreas = Array.from(doc.querySelectorAll('div[data-testid="stTextArea"]'));
            let targetArea = null;
            for (let ta of allTextAreas) {
                if (anchor.compareDocumentPosition(ta) & Node.DOCUMENT_POSITION_FOLLOWING) {
                    targetArea = ta; break;
                }
            }
            if (targetArea) {
                const contentBox = doc.getElementById(WINDOW_ID + '-content');
                contentBox.innerHTML = '';
                contentBox.appendChild(targetArea);
                targetArea.style.flex = '1'; targetArea.style.height = '100%';
                const divs = targetArea.querySelectorAll('div'); divs.forEach(d => d.style.height = '100%');
                const taInput = targetArea.querySelector('textarea');
                if (taInput) {
                    Object.assign(taInput.style, {
                        height:'100%', minHeight:'100%', border:'none', borderRadius:'0', resize:'none',
                        fontFamily:'Consolas, monospace', fontSize:'14px', padding:'10px', boxShadow:'none', background:'transparent'
                    });
                }
            }
        }
        
        ['Close_Hidden_Trigger', 'Minimize_Hidden_Trigger'].forEach(txt => {
            const btn = findButtonByText(txt); if(btn) btn.closest('.stButton').style.display = 'none';
        });

    })();
    </script>
    """
    
    components.html(js_code, height=0, width=0)
    st.markdown("<style>div[data-testid='stTextArea'] { width: 100% !important; }</style>", unsafe_allow_html=True)