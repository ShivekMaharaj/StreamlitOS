import streamlit as st
import streamlit.components.v1 as components
import window_manager

def render():
    st.markdown('<div style="display:none;">', unsafe_allow_html=True)
    if st.button("calc_close_trigger", key="calc_close_hidden"):
        window_manager.close_app("Calculator")
        st.rerun()
    if st.button("calc_min_trigger", key="calc_min_hidden"):
        window_manager.minimize_app("Calculator")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    js_code = """
    <script>
    (function() {
        const doc = window.parent.document;
        const WINDOW_ID = 'win11-calc-frame'; 
        const STORAGE_KEY = 'win11_calc_state';
        
        const bringToFront = (targetFrame) => {
            const allWindows = doc.querySelectorAll('div[class*="win11-window"]');
            let maxZ = 1000;
            allWindows.forEach(w => {
                const z = parseInt(w.style.zIndex || 0);
                if (z > maxZ) maxZ = z;
            });
            targetFrame.style.zIndex = maxZ + 1;
        };

        let frame = doc.getElementById(WINDOW_ID);
        let winState = JSON.parse(sessionStorage.getItem(STORAGE_KEY)) || {
            isMaximized: false, restoreX: '150px', restoreY: '150px', restoreW: '320px', restoreH: '480px'
        };

        if (!frame) {
            frame = doc.createElement('div');
            frame.id = WINDOW_ID;
            frame.className = 'win11-window'; 
            
            Object.assign(frame.style, {
                position: 'fixed', backgroundColor: '#f3f3f3', borderRadius: '8px',
                boxShadow: '0 10px 30px rgba(0,0,0,0.25), 0 0 0 1px rgba(0,0,0,0.1)',
                zIndex: '5001', display: 'flex', flexDirection: 'column',
                overflow: 'hidden', fontFamily: '"Segoe UI", sans-serif',
                animation: 'fadeIn 0.1s ease-out', minWidth: '260px', minHeight: '350px'
            });

            const style = doc.createElement('style');
            style.innerHTML = `
                .win-btn:hover { background-color: #e5e5e5; }
                .win-btn-close:hover { background-color: #e81123; color: white; }
                .calc-btn { border: 1px solid #e9e9e9; background-color: #fbfbfb; border-radius: 4px; width: 100%; height: 100%; font-size: 18px; font-weight: 600; cursor: pointer; display: flex; justify-content: center; align-items: center; user-select: none; }
                .calc-btn:hover { background-color: #f4f4f4; border-color: #d0d0d0; }
                .calc-btn:active { transform: scale(0.96); background-color: #ececec; }
                @keyframes fadeIn { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
            `;
            frame.appendChild(style);
            doc.body.appendChild(frame);
        } else {
            if (frame.style.display === 'none') {
                frame.style.display = 'flex';
                frame.style.animation = 'none'; frame.offsetHeight; frame.style.animation = 'fadeIn 0.1s ease-out';
            }
        }
        
        bringToFront(frame);
        frame.onmousedown = () => bringToFront(frame);

        const updateStorage = () => sessionStorage.setItem(STORAGE_KEY, JSON.stringify(winState));
        
        if (winState.isMaximized) {
             Object.assign(frame.style, { top: '0', left: '0', width: '100%', height: 'calc(100vh - 48px)', borderRadius: '0' });
        } else {
             Object.assign(frame.style, { top: winState.restoreY, left: winState.restoreX, width: winState.restoreW, height: winState.restoreH });
        }

        let savedScreenValue = "0";
        const oldScreen = doc.getElementById('calc-screen');
        if (oldScreen) savedScreenValue = oldScreen.innerText;

        const iconMax = `<div style="width:10px; height:10px; border:1px solid #000;"></div>`;
        const iconRestore = `<div style="position:relative; width:10px; height:10px;"><div style="position:absolute; top:-2px; right:-2px; width:8px; height:8px; border:1px solid #000; background:white; z-index:1;"></div><div style="position:absolute; bottom:-2px; left:-2px; width:8px; height:8px; border:1px solid #000; background:transparent; z-index:0;"></div></div>`;

        let contentContainer = frame.querySelector('.calc-content-wrapper');
        if (!contentContainer) {
            contentContainer = doc.createElement('div');
            contentContainer.className = 'calc-content-wrapper';
            Object.assign(contentContainer.style, { display:'flex', flexDirection:'column', height:'100%' });
            frame.appendChild(contentContainer);
        }

        contentContainer.innerHTML = `
            <div id="${WINDOW_ID}-header" style="height: 32px; display: flex; justify-content: space-between; align-items: center; padding-left: 10px; user-select: none; flex-shrink: 0;">
                <div style="font-size: 12px; font-weight: 600; color: #333; pointer-events: none;">Calculator</div>
                <div style="display: flex; height: 100%;">
                    <div id="${WINDOW_ID}-btn-min" class="win-btn" style="width:45px; display:flex; justify-content:center; align-items:center; cursor:pointer;"><span>&#8212;</span></div>
                    <div id="${WINDOW_ID}-btn-max" class="win-btn" style="width:45px; display:flex; justify-content:center; align-items:center; cursor:pointer;">${winState.isMaximized ? iconRestore : iconMax}</div>
                    <div id="${WINDOW_ID}-btn-close" class="win-btn-close" style="width:45px; display:flex; justify-content:center; align-items:center; cursor:pointer; border-top-right-radius: 8px;"><span style="font-size:14px;">&#10005;</span></div>
                </div>
            </div>
            <div style="padding: 5px 15px; font-size: 18px; font-weight: 700; color: #202020; flex-shrink: 0;">&#9776; Standard</div>
            <div id="calc-screen" style="height: 80px; display: flex; align-items: flex-end; justify-content: flex-end; padding: 0 15px 5px 15px; font-size: 48px; font-weight: 600; color: #202020; overflow: hidden; white-space: nowrap; flex-shrink: 0;">${savedScreenValue}</div>
            <div style="flex: 1; display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(6, 1fr); gap: 4px; padding: 6px; min-height: 0;">
                <button class="calc-btn op-btn" data-op="pct">%</button><button class="calc-btn op-btn" data-op="CE">CE</button><button class="calc-btn op-btn" data-op="C">C</button><button class="calc-btn op-btn" data-op="back">⌫</button>
                <button class="calc-btn op-btn" data-op="inv">¹/x</button><button class="calc-btn op-btn" data-op="sq">x²</button><button class="calc-btn op-btn" data-op="sqrt">√x</button><button class="calc-btn op-btn" data-op="/">÷</button>
                <button class="calc-btn num-btn">7</button><button class="calc-btn num-btn">8</button><button class="calc-btn num-btn">9</button><button class="calc-btn op-btn" data-op="*">×</button>
                <button class="calc-btn num-btn">4</button><button class="calc-btn num-btn">5</button><button class="calc-btn num-btn">6</button><button class="calc-btn op-btn" data-op="-">-</button>
                <button class="calc-btn num-btn">1</button><button class="calc-btn num-btn">2</button><button class="calc-btn num-btn">3</button><button class="calc-btn op-btn" data-op="+">+</button>
                <button class="calc-btn num-btn" style="font-size:16px;">+/-</button><button class="calc-btn num-btn">0</button><button class="calc-btn num-btn">.</button><button class="calc-btn eq-btn" style="background:#0067c0; color:white;">=</button>
            </div>
            <div id="${WINDOW_ID}-resizer" style="width: 15px; height: 15px; position: absolute; right: 0; bottom: 0; cursor: se-resize; zIndex: 510;"></div>
        `;

        const header = doc.getElementById(WINDOW_ID + '-header');
        let isDragging = false, dragX = 0, dragY = 0;
        
        header.onmousedown = (e) => {
            if(e.target.closest('.win-btn') || e.target.closest('.win-btn-close') || winState.isMaximized) return;
            isDragging = true; dragX = e.clientX - frame.offsetLeft; dragY = e.clientY - frame.offsetTop;
            bringToFront(frame);
        };

        doc.addEventListener('mousemove', (e) => {
            if(isDragging) { e.preventDefault(); frame.style.left = (e.clientX - dragX) + 'px'; frame.style.top = (e.clientY - dragY) + 'px'; }
        });
        doc.addEventListener('mouseup', () => { if(isDragging) { isDragging = false; winState.restoreX = frame.style.left; winState.restoreY = frame.style.top; updateStorage(); }});

        const resizer = doc.getElementById(WINDOW_ID + '-resizer');
        let isResizing = false;
        resizer.onmousedown = (e) => { if(!winState.isMaximized) { isResizing=true; e.stopPropagation(); bringToFront(frame); }};
        doc.addEventListener('mousemove', (e) => {
             if(isResizing) { e.preventDefault(); frame.style.width=(e.clientX-frame.getBoundingClientRect().left)+'px'; frame.style.height=(e.clientY-frame.getBoundingClientRect().top)+'px'; }
        });
        doc.addEventListener('mouseup', () => { if(isResizing){ isResizing=false; winState.restoreW=frame.style.width; winState.restoreH=frame.style.height; updateStorage(); }});

        function findStreamlitButton(keyPartial) {
            const buttons = Array.from(doc.querySelectorAll('button'));
            return buttons.find(b => b.innerText.includes(keyPartial));
        }
        frame.querySelector(`#${WINDOW_ID}-btn-max`).onclick = (e) => {
            e.stopPropagation();
            if (!winState.isMaximized) { winState.restoreX = frame.style.left; winState.restoreY = frame.style.top; winState.restoreW = frame.style.width; winState.restoreH = frame.style.height; }
            winState.isMaximized = !winState.isMaximized;
            
            const maxBtn = frame.querySelector(`#${WINDOW_ID}-btn-max`);
            if (winState.isMaximized) {
                Object.assign(frame.style, { top: '0', left: '0', width: '100%', height: 'calc(100vh - 48px)', borderRadius: '0' });
                maxBtn.innerHTML = iconRestore;
            } else {
                Object.assign(frame.style, { top: winState.restoreY, left: winState.restoreX, width: winState.restoreW, height: winState.restoreH, borderRadius: '8px' });
                maxBtn.innerHTML = iconMax;
            }
            updateStorage(); bringToFront(frame);
        };
        frame.querySelector(`#${WINDOW_ID}-btn-min`).onclick = (e) => { e.stopPropagation(); frame.style.display = 'none'; const btn = findStreamlitButton('calc_min_trigger'); if(btn) btn.click(); };
        frame.querySelector(`#${WINDOW_ID}-btn-close`).onclick = (e) => { e.stopPropagation(); frame.remove(); const btn = findStreamlitButton('calc_close_trigger'); if(btn) btn.click(); };

        let currentInput = savedScreenValue, previousInput = null, operator = null, resetScreen = false;
        const screen = doc.getElementById('calc-screen');
        const updateDisplay = () => screen.innerText = currentInput;

        frame.querySelectorAll('.num-btn').forEach(btn => {
            btn.onclick = () => {
                const val = btn.innerText;
                if(val === "+/-") { currentInput = (parseFloat(currentInput) * -1).toString(); }
                else if (currentInput === "0" || resetScreen) { currentInput = val; resetScreen = false; }
                else { currentInput += val; }
                updateDisplay();
            };
        });
        frame.querySelectorAll('.op-btn').forEach(btn => {
            btn.onclick = () => {
                const op = btn.getAttribute('data-op');
                if (op === 'C') { currentInput = "0"; previousInput = null; operator = null; resetScreen = false; updateDisplay(); return; }
                if (op === 'CE') { currentInput = "0"; updateDisplay(); return; }
                if (op === 'back') { currentInput = currentInput.slice(0, -1) || "0"; updateDisplay(); return; }
                if (op === 'pct') { currentInput = String(parseFloat(currentInput) / 100); updateDisplay(); resetScreen = true; return; }
                if (op === 'inv') { currentInput = String(1 / parseFloat(currentInput)); updateDisplay(); resetScreen = true; return; }
                if (op === 'sq')  { currentInput = String(Math.pow(parseFloat(currentInput), 2)); updateDisplay(); resetScreen = true; return; }
                if (op === 'sqrt') { currentInput = String(Math.sqrt(parseFloat(currentInput))); updateDisplay(); resetScreen = true; return; }
                if (operator && previousInput && !resetScreen) performCalculation();
                operator = op; previousInput = currentInput; resetScreen = true;
            };
        });
        frame.querySelector('.eq-btn').onclick = () => { if (!operator || !previousInput) return; performCalculation(); operator = null; resetScreen = true; };

        function performCalculation() {
            const prev = parseFloat(previousInput), curr = parseFloat(currentInput);
            if (isNaN(prev) || isNaN(curr)) return;
            let result;
            switch(operator) {
                case '+': result = prev + curr; break;
                case '-': result = prev - curr; break;
                case '*': result = prev * curr; break;
                case '/': result = curr === 0 ? "Error" : prev / curr; break;
            }
            currentInput = String(result); previousInput = null; updateDisplay();
        }

    })();
    </script>
    """
    components.html(js_code, height=0, width=0)