// Action Handlers for Menu Items
window.handleAction = function(action, data) {
    console.log('Handling action:', action, 'with data:', data);
    
    switch(action) {
        case 'newFile':
            newFile();
            break;
        case 'openFile':
            openFile();
            break;
        case 'saveFile':
            saveFile();
            break;
        case 'saveAsFile':
            saveAsFile();
            break;
        case 'exitApp':
            exitApp();
            break;
        case 'undo':
            undo();
            break;
        case 'redo':
            redo();
            break;
        case 'cut':
            cut();
            break;
        case 'copy':
            copy();
            break;
        case 'paste':
            paste();
            break;
        case 'findReplace':
            findReplace();
            break;
        case 'insertDate':
            insertDate();
            break;
        case 'screenKeyboard':
            screenKeyboard();
            break;
        case 'insertTag':
            insertTag(data);
            break;
        case 'insertForm':
            insertForm();
            break;
        case 'insertInput':
            insertInput(data);
            break;
        case 'insertSelect':
            insertSelect();
            break;
        case 'insertOption':
            insertOption();
            break;
        case 'insertTextarea':
            insertTextarea();
            break;
        case 'insertVideo':
            insertVideo();
            break;
        case 'insertAudio':
            insertAudio();
            break;
        case 'insertMeta':
            insertMeta(data);
            break;
        case 'showAbout':
            showAbout();
            break;
        case 'showDocs':
            showDocs();
            break;
        default:
            console.warn('Unknown action:', action);
    }
};

// File Operations
function newFile() {
    if (confirm('Create new file? Unsaved changes will be lost.')) {
        document.getElementById('html-editor').value = '';
        updatePreview();
        document.getElementById('file-info').textContent = 'New file';
        updateStatus('New file created');
    }
}

function openFile() {
    document.getElementById('file-input').click();
}

function saveFile() {
    const content = document.getElementById('html-editor').value;
    handleSave(content);
}

function saveAsFile() {
    const content = document.getElementById('html-editor').value;
    handleSave(content);
}

function exitApp() {
    if (confirm('Are you sure you want to exit?')) {
        window.close();
    }
}

// Edit Operations
let editHistory = [];
let historyIndex = -1;

function saveToHistory() {
    const content = document.getElementById('html-editor').value;
    if (editHistory[editHistory.length - 1] !== content) {
        editHistory.push(content);
        historyIndex = editHistory.length - 1;
        if (editHistory.length > 50) {
            editHistory.shift();
            historyIndex--;
        }
    }
}

function undo() {
    if (historyIndex > 0) {
        historyIndex--;
        document.getElementById('html-editor').value = editHistory[historyIndex];
        updatePreview();
        updateStatus('Undo');
    } else {
        updateStatus('Nothing to undo');
    }
}

function redo() {
    if (historyIndex < editHistory.length - 1) {
        historyIndex++;
        document.getElementById('html-editor').value = editHistory[historyIndex];
        updatePreview();
        updateStatus('Redo');
    } else {
        updateStatus('Nothing to redo');
    }
}

function cut() {
    const editor = document.getElementById('html-editor');
    const selected = editor.value.substring(editor.selectionStart, editor.selectionEnd);
    if (selected) {
        navigator.clipboard.writeText(selected);
        const start = editor.selectionStart;
        const end = editor.selectionEnd;
        editor.value = editor.value.substring(0, start) + editor.value.substring(end);
        editor.selectionStart = editor.selectionEnd = start;
        updatePreview();
        saveToHistory();
        updateStatus('Cut to clipboard');
    }
}

function copy() {
    const editor = document.getElementById('html-editor');
    const selected = editor.value.substring(editor.selectionStart, editor.selectionEnd);
    if (selected) {
        navigator.clipboard.writeText(selected);
        updateStatus('Copied to clipboard');
    }
}

function paste() {
    const editor = document.getElementById('html-editor');
    navigator.clipboard.readText().then(text => {
        const start = editor.selectionStart;
        const end = editor.selectionEnd;
        editor.value = editor.value.substring(0, start) + text + editor.value.substring(end);
        editor.selectionStart = editor.selectionEnd = start + text.length;
        updatePreview();
        saveToHistory();
        updateStatus('Pasted from clipboard');
    }).catch(err => {
        updateStatus('Failed to paste: ' + err);
    });
}

function findReplace() {
    showModal('find-replace-modal');
}

function handleFind() {
    const findText = document.getElementById('find-text').value;
    const caseSensitive = document.getElementById('case-sensitive').checked;
    const wholeWord = document.getElementById('whole-word').checked;
    
    if (!findText) {
        updateStatus('Please enter text to find');
        return;
    }
    
    const editor = document.getElementById('html-editor');
    const content = editor.value;
    let searchContent = content;
    let searchText = findText;
    
    if (!caseSensitive) {
        searchContent = content.toLowerCase();
        searchText = findText.toLowerCase();
    }
    
    let regex;
    if (wholeWord) {
        regex = new RegExp('\\b' + searchText.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\b', caseSensitive ? 'g' : 'gi');
    } else {
        regex = new RegExp(searchText.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), caseSensitive ? 'g' : 'gi');
    }
    
    const match = regex.exec(searchContent);
    if (match) {
        const matchIndex = match.index;
        editor.focus();
        editor.selectionStart = matchIndex;
        editor.selectionEnd = matchIndex + findText.length;
        updateStatus('Found text');
    } else {
        updateStatus('Text not found');
    }
}

function handleReplace() {
    const findText = document.getElementById('find-text').value;
    const replaceText = document.getElementById('replace-text').value;
    
    if (!findText) {
        updateStatus('Please enter text to find');
        return;
    }
    
    const editor = document.getElementById('html-editor');
    const selected = editor.value.substring(editor.selectionStart, editor.selectionEnd);
    
    if (selected === findText) {
        const start = editor.selectionStart;
        const end = editor.selectionEnd;
        editor.value = editor.value.substring(0, start) + replaceText + editor.value.substring(end);
        editor.selectionStart = editor.selectionEnd = start + replaceText.length;
        updatePreview();
        saveToHistory();
        updateStatus('Replaced');
    } else {
        handleFind();
        setTimeout(() => {
            const newSelected = editor.value.substring(editor.selectionStart, editor.selectionEnd);
            if (newSelected === findText) {
                const start = editor.selectionStart;
                const end = editor.selectionEnd;
                editor.value = editor.value.substring(0, start) + replaceText + editor.value.substring(end);
                editor.selectionStart = editor.selectionEnd = start + replaceText.length;
                updatePreview();
                saveToHistory();
                updateStatus('Replaced');
            }
        }, 100);
    }
}

function handleReplaceAll() {
    const findText = document.getElementById('find-text').value;
    const replaceText = document.getElementById('replace-text').value;
    const caseSensitive = document.getElementById('case-sensitive').checked;
    const wholeWord = document.getElementById('whole-word').checked;
    
    if (!findText) {
        updateStatus('Please enter text to find');
        return;
    }
    
    const editor = document.getElementById('html-editor');
    let content = editor.value;
    
    let regex;
    if (wholeWord) {
        regex = new RegExp('\\b' + findText.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\b', caseSensitive ? 'g' : 'gi');
    } else {
        regex = new RegExp(findText.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), caseSensitive ? 'g' : 'gi');
    }
    
    const newContent = content.replace(regex, replaceText);
    if (newContent !== content) {
        editor.value = newContent;
        updatePreview();
        saveToHistory();
        updateStatus('Replaced all occurrences');
    } else {
        updateStatus('No occurrences found');
    }
}

// Actions
function insertDate() {
    const now = new Date();
    const dateStr = now.toLocaleDateString() + ' ' + now.toLocaleTimeString();
    insertAtCursor(dateStr);
    updateStatus('Inserted current date');
}

function screenKeyboard() {
    showModal('keyboard-modal');
    createKeyboard();
}

// Tag insertion functions
function insertTag(tag) {
    const defaultContent = tag === 'dt' || tag === 'dd' ? 'Item' : 'Content';
    wrapSelectionWithTag(tag, defaultContent);
}

function wrapSelectionWithTag(tag, defaultText = 'text') {
    const editor = document.getElementById('html-editor');
    const start = editor.selectionStart;
    const end = editor.selectionEnd;
    
    if (start !== end) {
        const selected = editor.value.substring(start, end);
        const wrapped = '<' + tag + '>' + selected + '</' + tag + '>';
        editor.value = editor.value.substring(0, start) + wrapped + editor.value.substring(end);
        editor.selectionStart = start;
        editor.selectionEnd = start + wrapped.length;
    } else {
        const cursor = editor.selectionStart;
        const toInsert = '<' + tag + '>' + defaultText + '</' + tag + '>';
        editor.value = editor.value.substring(0, cursor) + toInsert + editor.value.substring(cursor);
        editor.selectionStart = cursor + tag.length + 2;
        editor.selectionEnd = editor.selectionStart + defaultText.length;
    }
    
    editor.focus();
    updatePreview();
    saveToHistory();
    updateStatus('Inserted ' + tag + ' tag');
}

function insertForm() {
    const formHTML = '\n<form action="#" method="post">\n  <!-- Form content here -->\n</form>\n';
    insertAtCursor(formHTML);
    updateStatus('Inserted form');
}

function insertInput(type) {
    const inputHTML = '<input type="' + type + '" name="" value="">';
    insertAtCursor(inputHTML);
    updateStatus('Inserted ' + type + ' input');
}

function insertSelect() {
    const selectHTML = '\n<select name="">\n  <option value="">Select option</option>\n</select>\n';
    insertAtCursor(selectHTML);
    updateStatus('Inserted select');
}

function insertOption() {
    const optionHTML = '  <option value="">Option text</option>';
    insertAtCursor(optionHTML);
    updateStatus('Inserted option');
}

function insertTextarea() {
    const textareaHTML = '\n<textarea name="" rows="4" cols="50"></textarea>\n';
    insertAtCursor(textareaHTML);
    updateStatus('Inserted textarea');
}

function insertVideo() {
    const videoHTML = '\n<video width="320" height="240" controls>\n  <source src="movie.mp4" type="video/mp4">\n  Your browser does not support the video tag.\n</video>\n';
    insertAtCursor(videoHTML);
    updateStatus('Inserted video');
}

function insertAudio() {
    const audioHTML = '\n<audio controls>\n  <source src="audio.mp3" type="audio/mpeg">\n  Your browser does not support the audio element.\n</audio>\n';
    insertAtCursor(audioHTML);
    updateStatus('Inserted audio');
}

function insertMeta(type) {
    let metaHTML = '';
    if (type === 'description') {
        metaHTML = '<meta name="description" content="Page description">';
    } else if (type === 'author') {
        metaHTML = '<meta name="author" content="Author name">';
    }
    insertAtCursor(metaHTML);
    updateStatus('Inserted meta ' + type);
}

// Helper functions
function insertAtCursor(text) {
    const editor = document.getElementById('html-editor');
    const start = editor.selectionStart;
    const end = editor.selectionEnd;
    editor.value = editor.value.substring(0, start) + text + editor.value.substring(end);
    editor.selectionStart = editor.selectionEnd = start + text.length;
    editor.focus();
    updatePreview();
    saveToHistory();
}

function createKeyboard() {
    const container = document.getElementById('keyboard-container');
    container.innerHTML = '';
    
    const keys = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
        'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
        'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';',
        'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/',
        'Space', 'Enter', 'Backspace', 'Tab'
    ];
    
    keys.forEach(key => {
        const keyElement = document.createElement('div');
        keyElement.className = 'keyboard-key';
        if (key === 'Space') keyElement.className += ' space';
        if (key === 'Enter') keyElement.className += ' enter';
        if (key === 'Backspace') keyElement.className += ' backspace';
        if (key === 'Tab') keyElement.className += ' tab';
        
        keyElement.textContent = key;
        keyElement.onclick = function() {
            const editor = document.getElementById('html-editor');
            let insertText = key;
            if (key === 'Space') insertText = ' ';
            if (key === 'Enter') insertText = '\n';
            if (key === 'Backspace') {
                const start = editor.selectionStart;
                const end = editor.selectionEnd;
                if (start === end && start > 0) {
                    editor.value = editor.value.substring(0, start - 1) + editor.value.substring(start);
                    editor.selectionStart = editor.selectionEnd = start - 1;
                } else {
                    editor.value = editor.value.substring(0, start) + editor.value.substring(end);
                    editor.selectionStart = editor.selectionEnd = start;
                }
            } else if (key === 'Tab') {
                insertText = '    ';
                insertAtCursor(insertText);
            } else {
                insertAtCursor(insertText);
            }
            editor.focus();
        };
        
        container.appendChild(keyElement);
    });
}

function showAbout() {
    alert('HTML Editor\nVersion 1.0\nA simple HTML editor with live preview.');
}

function showDocs() {
    alert('Documentation will be available in future versions.');
}

// Modal functions
function showModal(modalId) {
    document.getElementById('modal-overlay').style.display = 'block';
    document.getElementById(modalId).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById('modal-overlay').style.display = 'none';
    document.getElementById(modalId).style.display = 'none';
}

// Close modals when clicking outside
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('modal-overlay').onclick = function() {
        closeModal('find-replace-modal');
        closeModal('keyboard-modal');
    };
});

// Expose functions to window
window.saveToHistory = saveToHistory;
window.undo = undo;
window.redo = redo;
window.cut = cut;
window.copy = copy;
window.paste = paste;
window.findReplace = findReplace;
window.handleFind = handleFind;
window.handleReplace = handleReplace;
window.handleReplaceAll = handleReplaceAll;
window.insertDate = insertDate;
window.screenKeyboard = screenKeyboard;
window.insertTag = insertTag;
window.insertForm = insertForm;
window.insertInput = insertInput;
window.insertSelect = insertSelect;
window.insertOption = insertOption;
window.insertTextarea = insertTextarea;
window.insertVideo = insertVideo;
window.insertAudio = insertAudio;
window.insertMeta = insertMeta;
window.showAbout = showAbout;
window.showDocs = showDocs;
window.showModal = showModal;
window.closeModal = closeModal;
window.createKeyboard = createKeyboard;
window.insertAtCursor = insertAtCursor;
window.wrapSelectionWithTag = wrapSelectionWithTag;
//window.loadLocalFile = loadLocalFile;