#!/usr/bin/env python3

import sys
import os
import http.server
import socketserver
import webbrowser
import threading
import json
from urllib.parse import parse_qs, urlparse
import time
import mimetypes
import tempfile
import shutil

class SimpleHTMLEditor:
    def __init__(self, html_file=None):
        self.html_file = html_file
        self.content = ""
        self.editor_server = None
        self.preview_server = None
        self.editor_port = 8080
        self.preview_port = 8081
        self.preview_content = ""
        self.base_dir = os.getcwd()  # Current working directory for static files
        
        # Load content if file exists
        if html_file and os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as f:
                self.content = f.read()
                self.preview_content = self.content
                # Update base directory to the HTML file's directory
                self.base_dir = os.path.dirname(os.path.abspath(html_file))
        else:
            self.content = self.get_default_html()
            self.preview_content = self.content
    
    def get_default_html(self):
        """Get default HTML template"""
        return """<!DOCTYPE html>
<html>
<head>
    <title>HTML Editor</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            background: #f0f0f0;
            height: 100vh;
            overflow: hidden;
        }
        
        .container {
            display: flex;
            flex-direction: column;
            height: 100vh;
        }
        
        .header {
            background: #2c3e50;
            color: white;
            padding: 15px;
        }
        
        .header h1 {
            font-size: 20px;
            margin-bottom: 10px;
        }
        
        .toolbar {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        button {
            padding: 8px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
            font-size: 14px;
        }
        
        .file-btn {
            background: #3498db;
            color: white;
        }
        
        .file-btn:hover {
            background: #2980b9;
        }
        
        .tag-btn {
            background: #27ae60;
            color: white;
        }
        
        .tag-btn:hover {
            background: #229954;
        }
        
        .clear-btn {
            background: #e74c3c;
            color: white;
        }
        
        .clear-btn:hover {
            background: #c0392b;
        }
        
        .main-content {
            display: flex;
            flex: 1;
            overflow: hidden;
        }
        
        .split-panel {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            padding: 10px;
        }
        
        .panel-label {
            font-weight: bold;
            margin-bottom: 10px;
            color: #2c3e50;
            font-size: 16px;
        }
        
        .editor-container, .preview-container {
            flex: 1;
            border: 1px solid #bdc3c7;
            border-radius: 4px;
            overflow: hidden;
            background: white;
        }
        
        #html-editor {
            width: 100%;
            height: 100%;
            border: none;
            padding: 15px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            resize: none;
            outline: none;
        }
        
        #preview-frame {
            width: 100%;
            height: 100%;
            border: none;
        }
        
        .splitter {
            width: 10px;
            background: #95a5a6;
            cursor: col-resize;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        
        .splitter:hover {
            background: #7f8c8d;
        }
        
        .status-bar {
            background: #34495e;
            color: white;
            padding: 8px 15px;
            font-size: 13px;
            display: flex;
            justify-content: space-between;
        }
        
        #file-info {
            font-weight: bold;
        }
        
        #status {
            font-style: italic;
        }
        
        .file-input {
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>HTML Editor</h1>
            <div class="toolbar">
                <button class="file-btn" onclick="saveFile()">Save</button>
                <button class="file-btn" onclick="document.getElementById('file-input').click()">Open</button>
                <button class="clear-btn" onclick="clearEditor()">Clear</button>
                
                <input type="file" id="file-input" class="file-input" accept=".html,.htm" onchange="loadLocalFile(this.files[0])">
                
                <div style="flex-grow: 1;"></div>
                
                <button class="tag-btn" onclick="wrapSelection('b')">Bold (B)</button>
                <button class="tag-btn" onclick="wrapSelection('i')">Italic (I)</button>
                <button class="tag-btn" onclick="wrapSelection('u')">Underline (U)</button>
                <button class="tag-btn" onclick="wrapSelection('p')">Paragraph (P)</button>
                <button class="tag-btn" onclick="wrapSelection('div')">Div</button>
                <button class="tag-btn" onclick="wrapSelection('span')">Span</button>
            </div>
        </div>
        
        <div class="main-content">
            <div class="split-panel">
                <div class="panel-label">HTML Source</div>
                <div class="editor-container">
                    <textarea id="html-editor" oninput="updatePreview()"></textarea>
                </div>
            </div>
            
            <div class="splitter" id="splitter">‖</div>
            
            <div class="split-panel">
                <div class="panel-label">Live Preview</div>
                <div class="preview-container">
                    <iframe id="preview-frame"></iframe>
                </div>
            </div>
        </div>
        
        <div class="status-bar">
            <div id="file-info">No file loaded</div>
            <div>Status: <span id="status">Ready</span></div>
        </div>
    </div>
    
    <script>
        let previewPort = 8081;
        
        // Initialize splitter
        let isDragging = false;
        const splitter = document.getElementById('splitter');
        const leftPanel = splitter.previousElementSibling;
        const rightPanel = splitter.nextElementSibling;
        
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
        
        // Load initial content
        window.onload = function() {
            fetch('/get-content')
                .then(response => response.json())
                .then(data => {
                    const editor = document.getElementById('html-editor');
                    editor.value = data.content;
                    
                    if (data.filename) {
                        document.getElementById('file-info').textContent = 'File: ' + data.filename;
                    } else {
                        document.getElementById('file-info').textContent = 'New file';
                    }
                    
                    // Get preview port from server
                    if (data.preview_port) {
                        previewPort = data.preview_port;
                    }
                    
                    // Load initial preview
                    refreshPreview();
                    updateStatus('Loaded successfully');
                })
                .catch(error => {
                    console.error('Error loading content:', error);
                    updateStatus('Error loading content');
                });
        };
        
        function wrapSelection(tag) {
            const editor = document.getElementById('html-editor');
            const start = editor.selectionStart;
            const end = editor.selectionEnd;
            
            if (start !== end) {
                // Text is selected
                const selectedText = editor.value.substring(start, end);
                const wrappedText = '<' + tag + '>' + selectedText + '</' + tag + '>';
                
                // Replace selection
                editor.value = editor.value.substring(0, start) + 
                               wrappedText + 
                               editor.value.substring(end);
                
                // Restore cursor position
                editor.selectionStart = start;
                editor.selectionEnd = start + wrappedText.length;
                
                updateStatus('Wrapped with ' + tag + ' tags');
            } else {
                // No selection, insert at cursor
                const cursorPos = editor.selectionStart;
                const textToInsert = '<' + tag + '>text</' + tag + '>';
                
                editor.value = editor.value.substring(0, cursorPos) + 
                               textToInsert + 
                               editor.value.substring(cursorPos);
                
                // Move cursor inside the tags
                editor.selectionStart = cursorPos + tag.length + 2;
                editor.selectionEnd = editor.selectionStart + 4;
                
                updateStatus('Inserted ' + tag + ' tags');
            }
            
            updatePreview();
            editor.focus();
        }
        
        function updatePreview() {
            const content = document.getElementById('html-editor').value;
            
            // Send content to preview server
            fetch('/update-preview', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({content: content})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    refreshPreview();
                    updateStatus('Preview updated');
                }
            })
            .catch(error => {
                console.error('Error updating preview:', error);
            });
        }
        
        function refreshPreview() {
            // Refresh iframe to show updated content
            const iframe = document.getElementById('preview-frame');
            iframe.src = 'http://localhost:' + previewPort + '/?t=' + Date.now();
        }
        
        function saveFile() {
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
                    // Update preview after save
                    updatePreview();
                } else {
                    updateStatus('Save failed: ' + data.error);
                }
            })
            .catch(error => {
                updateStatus('Save failed: ' + error);
            });
        }
        
        function clearEditor() {
            if (confirm('Clear all text?')) {
                document.getElementById('html-editor').value = '';
                updatePreview();
                updateStatus('Cleared');
            }
        }
        
        function loadLocalFile(file) {
            if (!file) return;
            
            const reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById('html-editor').value = e.target.result;
                updatePreview();
                updateStatus('Loaded local file: ' + file.name);
                document.getElementById('file-info').textContent = 'Local: ' + file.name;
            };
            reader.readAsText(file);
        }
        
        function updateStatus(message) {
            document.getElementById('status').textContent = message;
        }
    </script>
</body>
</html>"""
    
    def start_editor_server(self):
        """Start editor HTTP server"""
        class EditorHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                editor_instance = self.server.editor_instance
                
                if self.path == '/':
                    # Serve editor page
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    
                    editor_html = editor_instance.get_default_html()
                    self.wfile.write(editor_html.encode('utf-8'))
                    
                elif self.path == '/get-content':
                    # Return current content as JSON
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    
                    response = {
                        'content': editor_instance.content,
                        'filename': os.path.basename(editor_instance.html_file) if editor_instance.html_file else None,
                        'preview_port': editor_instance.preview_port
                    }
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                    
                else:
                    self.send_error(404, "Not found")
            
            def do_POST(self):
                editor_instance = self.server.editor_instance
                
                if self.path == '/update-preview':
                    # Update preview content
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length).decode('utf-8')
                    data = json.loads(post_data)
                    
                    if 'content' in data:
                        editor_instance.preview_content = data['content']
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': True}).encode('utf-8'))
                    
                elif self.path == '/save-file':
                    # Save content to file
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length).decode('utf-8')
                    data = json.loads(post_data)
                    
                    if 'content' in data:
                        content_to_save = data['content']
                        editor_instance.content = content_to_save
                        editor_instance.preview_content = content_to_save
                        
                        # If no file is set, create one
                        if not editor_instance.html_file:
                            editor_instance.html_file = "edited.html"
                        
                        try:
                            with open(editor_instance.html_file, 'w', encoding='utf-8') as f:
                                f.write(content_to_save)
                            
                            # Update base directory to the saved file's directory
                            editor_instance.base_dir = os.path.dirname(os.path.abspath(editor_instance.html_file))
                            
                            response = {
                                'success': True,
                                'filename': os.path.basename(editor_instance.html_file)
                            }
                        except Exception as e:
                            response = {'success': False, 'error': str(e)}
                    else:
                        response = {'success': False, 'error': 'No content provided'}
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                    
                else:
                    self.send_error(404, "Not found")
            
            def log_message(self, format, *args):
                # Suppress HTTP logs
                pass
        
        # Try different ports for editor
        for port in range(8080, 8100):
            try:
                self.editor_server = socketserver.TCPServer(("", port), EditorHandler)
                self.editor_server.editor_instance = self
                self.editor_port = port
                break
            except OSError:
                continue
        
        if not self.editor_server:
            print("Could not start editor server")
            return
        
        # Start editor server in background thread
        editor_thread = threading.Thread(target=self.editor_server.serve_forever)
        editor_thread.daemon = True
        editor_thread.start()
    
    def start_preview_server(self):
        """Start preview HTTP server - serves static files from current directory"""
        class PreviewHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                editor_instance = self.server.editor_instance
                
                # Remove query parameters from path
                clean_path = self.path.split('?')[0]
                
                # Root path serves the HTML content directly
                if clean_path == '/':
                    # Serve the preview HTML content directly
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                    self.send_header('Pragma', 'no-cache')
                    self.send_header('Expires', '0')
                    self.end_headers()
                    
                    self.wfile.write(editor_instance.preview_content.encode('utf-8'))
                    return
                
                # Handle static file requests (CSS, JS, images, etc.)
                # Default to index.html for empty path
                if clean_path == '':
                    clean_path = '/index.html'
                
                # Try to serve file from base directory
                file_path = os.path.join(editor_instance.base_dir, clean_path.lstrip('/'))
                
                # Security check: ensure the file is within the base directory
                try:
                    file_path = os.path.normpath(file_path)
                    if not file_path.startswith(os.path.abspath(editor_instance.base_dir)):
                        self.send_error(403, "Forbidden")
                        return
                except:
                    self.send_error(403, "Forbidden")
                    return
                
                # Check if file exists and is a file (not a directory)
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    try:
                        # Determine MIME type
                        mime_type, _ = mimetypes.guess_type(file_path)
                        if not mime_type:
                            mime_type = 'application/octet-stream'
                        
                        # Read and serve the file
                        with open(file_path, 'rb') as f:
                            content = f.read()
                        
                        self.send_response(200)
                        self.send_header('Content-type', mime_type)
                        self.send_header('Content-Length', str(len(content)))
                        self.end_headers()
                        
                        self.wfile.write(content)
                        return
                    except Exception as e:
                        self.send_error(500, f"Server error: {str(e)}")
                        return
                else:
                    # File not found
                    self.send_error(404, f"File not found: {clean_path}")
                    return
            
            def log_message(self, format, *args):
                # Suppress HTTP logs
                pass
        
        # Try different ports for preview
        for port in range(8081, 8100):
            try:
                self.preview_server = socketserver.TCPServer(("", port), PreviewHandler)
                self.preview_server.editor_instance = self
                self.preview_port = port
                break
            except OSError:
                continue
        
        if not self.preview_server:
            print("Could not start preview server")
            return
        
        # Start preview server in background thread
        preview_thread = threading.Thread(target=self.preview_server.serve_forever)
        preview_thread.daemon = True
        preview_thread.start()
    
    def start_servers(self):
        """Start both servers"""
        print("Starting HTML Editor...")
        print(f"Base directory for static files: {self.base_dir}")
        
        # Start both servers
        self.start_editor_server()
        self.start_preview_server()
        
        if not self.editor_server or not self.preview_server:
            print("Failed to start servers")
            return
        
        print(f"Editor server started at http://localhost:{self.editor_port}")
        print(f"Preview server started at http://localhost:{self.preview_port}")
        print("Opening browser...")
        print("Press Ctrl+C to stop")
        
        # Open browser to editor
        webbrowser.open(f"http://localhost:{self.editor_port}")
        
        # Keep main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
            if self.editor_server:
                self.editor_server.shutdown()
            if self.preview_server:
                self.preview_server.shutdown()
    
    def run(self):
        """Run the editor"""
        self.start_servers()

def main():
    # Get filename from command line
    html_file = None
    if len(sys.argv) > 1:
        html_file = sys.argv[1]
        if not os.path.exists(html_file):
            print(f"File '{html_file}' not found. Starting with empty editor.")
            html_file = None
    
    # Create and run editor
    editor = SimpleHTMLEditor(html_file)
    editor.run()

if __name__ == "__main__":
    main()