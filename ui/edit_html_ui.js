// Main UI JavaScript for HTML Editor

let previewPort = 8081;
let currentFindIndex = -1;
let findResults = [];

function initUI() {
    console.log('Initializing UI...');
    
    // Load initial content
    fetch('/get-content')
        .then(response => response.json())
        .then(data => {
            const editor = document.getElementById('html-editor');
            editor.value = data.content;
            highlighter = document.getElementById('highlighter');


            const text = editor.value;
            highlighter.innerHTML = highlight(text) || '\n'; // prevent collapse
            highlighter.style.height = editor.scrollHeight + 'px';

            if (data.filename) {
                document.getElementById('file-info').textContent = 'File: ' + data.filename;
            } else {
                document.getElementById('file-info').textContent = 'New file';
            }
            
            if (data.preview_port) {
                previewPort = data.preview_port;
            }
            
            // Initialize edit history
            if (typeof window.saveToHistory === 'function') {
                window.saveToHistory();
            }
            
            // Load initial preview
            refreshPreview();
            updateStatus('Loaded successfully');
            
            // Set up auto-save to history
            editor.addEventListener('input', function() {
                if (typeof window.saveToHistory === 'function') {
                    window.saveToHistory();
                }
            });
        })
        .catch(error => {
            console.error('Error loading content:', error);
            updateStatus('Error loading content');
        });
    
    // Initialize splitter
    initSplitter();
    
    // Set up file input
    document.getElementById('file-input').addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            if (typeof window.loadLocalFile === 'function') {
                window.loadLocalFile(e.target.files[0]);
            }
        }
    });
    
    // Set up editor event listeners
    const editor = document.getElementById('html-editor');
    editor.addEventListener('input', updatePreview);
    
    console.log('UI initialized');
}

function initSplitter() {
    let isDragging = false;
    const splitter = document.getElementById('splitter');
    const leftPanel = splitter.previousElementSibling;
    const rightPanel = splitter.nextElementSibling;
    
    // Set initial 50/50 split
    leftPanel.style.flex = '0 0 50%';
    rightPanel.style.flex = '0 0 50%';
    
    splitter.addEventListener('mousedown', function(e) {
        isDragging = true;
        document.body.style.cursor = 'col-resize';
        e.preventDefault();
    });
    
    document.addEventListener('mousemove', function(e) {
        if (!isDragging) return;
        
        const containerWidth = document.querySelector('.main-content').offsetWidth;
        const splitterWidth = splitter.offsetWidth;
        const mouseX = e.clientX;
        const containerRect = document.querySelector('.main-content').getBoundingClientRect();
        const relativeX = mouseX - containerRect.left;
        
        // Calculate new widths (minimum 20%)
        const leftWidth = Math.max(20, Math.min(80, (relativeX / containerWidth) * 100));
        
        leftPanel.style.flex = `0 0 ${leftWidth}%`;
        rightPanel.style.flex = `0 0 ${100 - leftWidth - (splitterWidth / containerWidth * 100)}%`;
    });
    
    document.addEventListener('mouseup', function() {
        isDragging = false;
        document.body.style.cursor = '';
    });
}

function wrapSelection(tag) {
    const editor = document.getElementById('html-editor');
    const start = editor.selectionStart;
    const end = editor.selectionEnd;
    
    if (start !== end) {
        const selectedText = editor.value.substring(start, end);
        const wrappedText = '<' + tag + '>' + selectedText + '</' + tag + '>';
        
        editor.value = editor.value.substring(0, start) + wrappedText + editor.value.substring(end);
        editor.selectionStart = start;
        editor.selectionEnd = start + wrappedText.length;
        
        updateStatus('Wrapped with ' + tag + ' tags');
    } else {
        const cursorPos = editor.selectionStart;
        const textToInsert = '<' + tag + '>text</' + tag + '>';
        
        editor.value = editor.value.substring(0, cursorPos) + textToInsert + editor.value.substring(cursorPos);
        editor.selectionStart = cursorPos + tag.length + 2;
        editor.selectionEnd = editor.selectionStart + 4;
        
        updateStatus('Inserted ' + tag + ' tags');
    }
    
    updatePreview();
    editor.focus();
    if (typeof window.saveToHistory === 'function') {
        window.saveToHistory();
    }
}

function updatePreview() {
    const content = document.getElementById('html-editor').value;
    
    fetch('/update-preview', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({content: content})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            refreshPreview();
        }
    })
    .catch(error => {
        console.error('Error updating preview:', error);
    });
}

function refreshPreview() {
    const iframe = document.getElementById('preview-frame');
    iframe.src = 'http://localhost:' + previewPort + '/?t=' + Date.now();
}

function handleSave() {
    const content = document.getElementById('html-editor').value;
    
    fetch('/save-file', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({content: content})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateStatus('Saved: ' + data.filename);
            document.getElementById('file-info').textContent = 'File: ' + data.filename;
        } else {
            updateStatus('Save failed: ' + data.error);
        }
    })
    .catch(error => {
        updateStatus('Save failed: ' + error);
    });
}

function handleOpen() {
    document.getElementById('file-input').click();
}

function handleClear() {
    if (confirm('Clear all text?')) {
        document.getElementById('html-editor').value = '';
        updatePreview();
        updateStatus('Cleared');
        if (typeof window.saveToHistory === 'function') {
            window.saveToHistory();
        }
    }
}

function updateStatus(message) {
    document.getElementById('status').textContent = message;
    console.log('Status:', message);
}

// Expose functions to window object
window.wrapSelection = wrapSelection;
window.handleSave = handleSave;
window.handleOpen = handleOpen;
window.handleClear = handleClear;
window.updatePreview = updatePreview;
window.refreshPreview = refreshPreview;
window.updateStatus = updateStatus;
window.initUI = initUI;