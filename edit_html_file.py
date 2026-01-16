#!/usr/bin/env python3

import sys
import os
import http.server
import socketserver
import webbrowser
import threading
import json
import mimetypes
import time

class SimpleHTMLEditor:
    def __init__(self, html_file=None):
        self.html_file = html_file
        self.content = ""
        self.editor_server = None
        self.preview_server = None
        self.editor_port = 8080
        self.preview_port = 8081
        self.preview_content = ""
        self.base_dir = os.getcwd()
        self.ui_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui')
        
        # Check if UI directory exists
        if not os.path.exists(self.ui_dir):
            print(f"Error: UI directory not found: {self.ui_dir}")
            print("Please create the ui/ directory with the required files:")
            print("  ui/edit_html_ui.html")
            print("  ui/edit_html_ui.css")
            print("  ui/edit_html_ui.js")
            print("  ui/mainmenu.js")
            print("  ui/actionhandlers.js")
            print("  ui/default_html_edited_file.html (optional)")
            sys.exit(1)
        
        # Load content if file exists
        if html_file and os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as f:
                self.content = f.read()
                self.preview_content = self.content
                self.base_dir = os.path.dirname(os.path.abspath(html_file))
        else:
            self.content = self.get_default_html()
            self.preview_content = self.content
    
    def get_default_html(self):
        """Get default HTML template from file or fallback"""
        default_html_file = os.path.join(self.ui_dir, 'default_html_edited_file.html')
        
        if os.path.exists(default_html_file):
            try:
                with open(default_html_file, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"Warning: Could not read default HTML file: {e}")
                print("Using built-in default HTML...")
                return self.get_builtin_default_html()
        else:
            print("Info: No default_html_edited_file.html found, using built-in default HTML")
            return self.get_builtin_default_html()
    
    def get_builtin_default_html(self):
        """Fallback built-in default HTML template"""
        return """<!DOCTYPE html>
<html>
<head>
    <title>HTML Editor</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="author" content="HTML Editor">
    <meta name="description" content="A simple HTML editor with live preview">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            line-height: 1.6;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        .demo-section {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
            border-left: 4px solid #3498db;
        }
        .editor-info {
            background: #e8f4f8;
            border: 1px solid #b3e0f2;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }
        code {
            background: #f1f1f1;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to HTML Editor</h1>
        
        <div class="editor-info">
            <p><strong>Note:</strong> This is the built-in default HTML. Create a file named 
            <code>default_html_edited_file.html</code> in the <code>ui/</code> directory 
            to use your own custom default template.</p>
        </div>
        
        <div class="demo-section">
            <h2>Getting Started</h2>
            <p>This is a live preview of your HTML. Edit the code in the left panel to see changes here.</p>
            
            <h3>Features:</h3>
            <ul>
                <li>HTML syntax editing</li>
                <li>Live preview</li>
                <li>Tag formatting tools</li>
                <li>Find and replace</li>
                <li>Insert common HTML elements</li>
                <li>Undo/Redo functionality</li>
                <li>On-screen keyboard</li>
            </ul>
        </div>
        
        <div class="demo-section">
            <h2>Sample HTML Elements</h2>
            
            <h3>Text Formatting:</h3>
            <p><b>Bold text</b>, <i>italic text</i>, and <u>underlined text</u>.</p>
            
            <h3>Links:</h3>
            <p>Visit <a href="#">this example link</a> for more information.</p>
            
            <h3>Lists:</h3>
            <ul>
                <li>Unordered list item 1</li>
                <li>Unordered list item 2</li>
                <li>Unordered list item 3</li>
            </ul>
            
            <ol>
                <li>Ordered list item 1</li>
                <li>Ordered list item 2</li>
                <li>Ordered list item 3</li>
            </ol>
            
            <h3>Code Example:</h3>
            <pre><code>&lt;!-- This is an HTML comment --&gt;
&lt;div class="example"&gt;
    &lt;p&gt;Example paragraph&lt;/p&gt;
&lt;/div&gt;</code></pre>
        </div>
        
        <div class="demo-section">
            <h2>Quick Tips:</h2>
            <ol>
                <li>Use the menu bar to insert HTML elements</li>
                <li>Select text and click toolbar buttons to wrap with tags</li>
                <li>Use Ctrl+S to save your work</li>
                <li>Drag the splitter between panels to resize</li>
                <li>Use Find/Replace from the Edit menu to search text</li>
            </ol>
        </div>
    </div>
    
    <script>
        // Simple script for the default template
        console.log('Default HTML template loaded');
    </script>
</body>
</html>"""
    
    def serve_file(self, path, content_type=None):
        """Serve a file from the filesystem"""
        # Map paths to actual file locations
        if path == '/':
            file_path = os.path.join(self.ui_dir, 'edit_html_ui.html')
        elif path.startswith('/ui/'):
            file_path = os.path.join(self.ui_dir, path[4:])
        else:
            return None
        
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            if not content_type:
                content_type, _ = mimetypes.guess_type(file_path)
                if not content_type:
                    content_type = 'application/octet-stream'
            
            return content, content_type
        except Exception as e:
            print(f"Error serving file {file_path}: {e}")
            return None
    
    def start_editor_server(self):
        """Start editor HTTP server"""
        class EditorHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                editor_instance = self.server.editor_instance
                
                # Try to serve static file
                file_data = editor_instance.serve_file(self.path)
                if file_data:
                    content, content_type = file_data
                    self.send_response(200)
                    self.send_header('Content-type', content_type)
                    self.send_header('Content-Length', str(len(content)))
                    self.end_headers()
                    self.wfile.write(content)
                    return
                
                # API endpoints
                if self.path == '/get-content':
                    # Return current content as JSON
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    
                    response = {
                        'content': editor_instance.content,
                        'filename': os.path.basename(editor_instance.html_file) if editor_instance.html_file else None,
                        'preview_port': editor_instance.preview_port,
                        'has_custom_default': os.path.exists(os.path.join(editor_instance.ui_dir, 'default_html_edited_file.html'))
                    }
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                    return
                
                # Not found
                self.send_error(404, f"Not found: {self.path}")
            
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
        """Start preview HTTP server"""
        class PreviewHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                editor_instance = self.server.editor_instance
                
                # Remove query parameters
                clean_path = self.path.split('?')[0]
                
                if clean_path == '/':
                    # Serve the preview HTML content
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                    self.send_header('Pragma', 'no-cache')
                    self.send_header('Expires', '0')
                    self.end_headers()
                    
                    self.wfile.write(editor_instance.preview_content.encode('utf-8'))
                    return
                
                # Handle static files from base directory
                file_path = os.path.join(editor_instance.base_dir, clean_path.lstrip('/'))
                
                # Security check
                try:
                    file_path = os.path.normpath(file_path)
                    if not file_path.startswith(os.path.abspath(editor_instance.base_dir)):
                        self.send_error(403, "Forbidden")
                        return
                except:
                    self.send_error(403, "Forbidden")
                    return
                
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    try:
                        mime_type, _ = mimetypes.guess_type(file_path)
                        if not mime_type:
                            mime_type = 'application/octet-stream'
                        
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
                    self.send_error(404, f"File not found: {clean_path}")
                    return
            
            def log_message(self, format, *args):
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
        print("Starting HTML Editor with modular UI...")
        print(f"UI directory: {self.ui_dir}")
        print(f"Base directory for static files: {self.base_dir}")
        
        # Check for custom default HTML
        default_html_file = os.path.join(self.ui_dir, 'default_html_edited_file.html')
        if os.path.exists(default_html_file):
            print("✓ Using custom default HTML from: default_html_edited_file.html")
        else:
            print("ℹ Using built-in default HTML (create default_html_edited_file.html for custom)")
        
        # Start both servers
        self.start_editor_server()
        self.start_preview_server()
        
        if not self.editor_server or not self.preview_server:
            print("Failed to start servers")
            return
        
        print(f"✓ Editor server started at http://localhost:{self.editor_port}")
        print(f"✓ Preview server started at http://localhost:{self.preview_port}")
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
            print(f"File '{html_file}' not found. Starting with default HTML.")
            html_file = None
    
    # Create and run editor
    editor = SimpleHTMLEditor(html_file)
    editor.run()

if __name__ == "__main__":
    main()