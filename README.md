# HTML File Editor

A simple web-based HTML editor with live preview and tag formatting tools. This editor is designed for quick HTML editing with real-time preview in a split-pane interface.

## Screenshots

![Open index.html and edit it in the left panel](https://dl.dropbox.com/scl/fi/uq13t4ugxe33ukmmtr14g/edit_I.png?rlkey=mhujupvndz8vt748vt7ai05vr&st=cvhd2uiq)

![View changed file at right panel](https://dl.dropbox.com/scl/fi/b7r5v0cyj7sy3pfgrxrkz/edit_II.png?rlkey=iiecz5s0a7zn7yo87m0grv2dg&st=dp8l53ys)

## Features

- **Split-pane interface**: Left panel for HTML editing, right panel for live preview
- **Tag formatting buttons**: Quickly wrap selected text with HTML tags (B, I, U, P, DIV, SPAN)
- **Live preview**: See HTML rendering as you type
- **Static file serving**: Preview loads CSS, JavaScript, and images from the current directory
- **File operations**: Open, Save, and Clear editor
- **Resizable panels**: Drag the splitter to adjust editor/preview sizes
- **Auto-load**: Open HTML files from command line

## Installation

No installation required! This is a pure Python script with no external dependencies.

### Requirements
- Python 3.6 or higher
- Modern web browser

## Usage

### Basic usage
```bash
# Run the editor
python3 edit_html_file.py

# Open an HTML file for editing
python3 edit_html_file.py index.html

# Edit HTML templates for entity_xml_crud_app
python3 edit_html_file.py path/to/template.html
```

### Using the Editor
1. **Left panel**: Edit your HTML code
2. **Right panel**: See live preview of the rendered HTML
3. **Toolbar buttons**:
   - **Save**: Save current HTML to file
   - **Open**: Open an HTML file from your computer
   - **Clear**: Clear the editor
   - **B/I/U/P/DIV/SPAN**: Wrap selected text with HTML tags

4. **Splitter**: Drag the `‖` symbol between panels to resize

### Keyboard Shortcuts
- **Select text** → Click tag button to wrap with HTML tags
- **No selection** → Click tag button to insert `<tag>text</tag>` at cursor
- The preview updates automatically as you type

## Integration with entity_xml_crud_app

This editor is particularly useful for editing HTML templates in the [ArtNazarov/entity_xml_crud_app](https://github.com/ArtNazarov/entity_xml_crud_app) project.

### Editing Templates
```bash
# Navigate to your entity_xml_crud_app directory
cd ~/projects/entity_xml_crud_app

# Edit HTML templates
python3 ~/edit_html_file/edit_html_file.py templates/customer_form.html
python3 ~/edit_html_file/edit_html_file.py templates/product_list.html
```

The preview will automatically load CSS, JavaScript, and images from the template's directory, making it ideal for template development.

## How It Works

The editor runs two local HTTP servers:
1. **Editor server** (port 8080): Serves the editor interface
2. **Preview server** (port 8081): Serves HTML content and static files

When you edit HTML, the content is sent to the preview server, and the iframe reloads to show the updated page.

## Troubleshooting

### Port already in use
The script automatically tries ports 8080-8099. If you have conflicts, close other applications using these ports.

### Images/CSS not loading in preview
Make sure asset files (images, CSS, JS) are in the same directory as your HTML file or use correct relative paths.

### Browser doesn't open automatically
Open your browser and navigate to: `http://localhost:8080`

## Stopping the Editor
Press **Ctrl+C** in the terminal to stop the editor.

## Project Structure
```
edit_html_file/
├── edit_html_file.py    # Main editor script
├── README.md           # This file
└── (no dependencies required)
```

## License
Open source - use as you wish!

## Related Projects
- [ArtNazarov/entity_xml_crud_app](https://github.com/ArtNazarov/entity_xml_crud_app) - Use this editor for HTML template development

---

Perfect for quick HTML edits, template development, or learning HTML with immediate visual feedback!
