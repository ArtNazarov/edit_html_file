# HTML File Editor

A simple web-based HTML editor with live preview and tag formatting tools. This editor is designed for quick HTML editing with real-time preview in a split-pane interface.

## Screenshots

![Open index.html and edit it in the left panel](https://dl.dropbox.com/scl/fi/uq13t4ugxe33ukmmtr14g/edit_I.png?rlkey=mhujupvndz8vt748vt7ai05vr&st=cvhd2uiq)

![View changed file at right panel](https://dl.dropbox.com/scl/fi/b7r5v0cyj7sy3pfgrxrkz/edit_II.png?rlkey=iiecz5s0a7zn7yo87m0grv2dg&st=dp8l53ys)

## Features

### 📋 **Core Interface Features**
- **Split-pane interface**: Left panel for HTML editing, right panel for live preview
- **Resizable panels**: Drag the vertical splitter (`‖`) to adjust editor/preview widths (default 50/50 split)
- **Status bar**: Shows current file and operation status
- **Clean, professional UI**: No emojis or distracting icons - text-only interface

### 🏷️ **HTML Tags & Structure Menu**
The editor provides organized menu categories for inserting HTML tags:

#### **Current Implementation**
**Basic Formatting Tags:**
- **Bold (B)**: `<b>text</b>` - Bold text
- **Italic (I)**: `<i>text</i>` - Italic text  
- **Underline (U)**: `<u>text</u>` - Underlined text
- **Paragraph (P)**: `<p>text</p>` - Paragraph block
- **Div**: `<div>text</div>` - Division/container
- **Span**: `<span>text</span>` - Inline container

#### **Planned/Upcoming Features**

**🔍 Find/Replace Menu**
- **Find**: Search for substring using modal dialog
- **Replace**: Replace substring using modal dialog

**↩️ Actions Menu**
- **Undo**: Revert last change
- **Redo**: Reapply undone change  
- **Screen Keyboard**: Show on-screen keyboard
- **Insert Date**: Insert current date/time

**🏗️ Structure Tags Menu**
- **Main**: `<main>content</main>` - Main content
- **Section**: `<section>content</section>` - Thematic grouping
- **Article**: `<article>content</article>` - Independent content
- **Aside**: `<aside>content</aside>` - Side content
- **Header**: `<header>content</header>` - Introductory content
- **Footer**: `<footer>content</footer>` - Closing content
- **Nav**: `<nav>links</nav>` - Navigation links
- **Address**: `<address>contact</address>` - Contact information

**📖 Definitions Submenu**
- **DL**: `<dl>definition list</dl>` - Definition list
- **DT**: `<dt>term</dt>` - Definition term
- **DD**: `<dd>definition</dd>` - Definition description

**📝 Forms Menu**
- **Form**: `<form>elements</form>` - Input form
- **Input Text**: `<input type="text">` - Text field
- **Input Password**: `<input type="password">` - Password field
- **Checkbox**: `<input type="checkbox">` - Checkbox
- **Radio**: `<input type="radio">` - Radio button
- **Hidden Input**: `<input type="hidden">` - Hidden field
- **Select**: `<select>options</select>` - Dropdown list
- **Option**: `<option>value</option>` - Dropdown option
- **Textarea**: `<textarea>content</textarea>` - Multi-line text
- **Output**: `<output>result</output>` - Calculation result

**🎬 Media Content Menu**
- **Video**: `<video>sources</video>` - Video player
- **Video Source**: `<source src="video.mp4">` - Video source
- **Audio**: `<audio>sources</audio>` - Audio player  
- **Audio Source**: `<source src="audio.mp3">` - Audio source

**📄 Meta Tags Menu**
- **Meta Description**: `<meta name="description" content="...">`
- **Meta Author**: `<meta name="author" content="...">`

### 🛠️ **Editor Features**
- **Syntax-aware editing**: Monospace font with proper text wrapping
- **Live preview**: See HTML rendering in real-time as you type
- **Auto-save on change**: Content is saved to server automatically during editing
- **Undo/Redo**: Standard browser undo/redo functionality works

### 📁 **File Operations**
| Button | Function | Description |
|--------|----------|-------------|
| **Save** | Save File | Save current HTML to disk. Creates new file if none exists |
| **Open** | Open File | Open HTML file from local computer via file dialog |
| **Clear** | Clear Editor | Remove all content from editor (with confirmation) |

### 🌐 **Preview Features**
- **Live rendering**: Actual HTML/CSS/JavaScript execution in embedded browser
- **Static asset support**: Images, CSS, JS files load from current directory
- **Automatic refresh**: Preview updates on every keystroke
- **Full browser context**: Preview behaves like actual web page

### ⚙️ **Technical Features**
- **No dependencies**: Pure Python standard library only
- **Cross-platform**: Works on Windows, macOS, Linux
- **Auto-port selection**: Automatically finds available port (8080-8099)
- **Command-line support**: Open files directly from terminal
- **Browser auto-launch**: Opens editor in default web browser automatically

## Installation

No installation required! This is a pure Python script with no external dependencies.

### Requirements
- Python 3.6 or higher
- Modern web browser (Chrome, Firefox, Edge, Safari)

## Usage

### Basic usage
```bash
# Run the editor (opens in browser)
python3 edit_html_file.py

# Open an HTML file for editing
python3 edit_html_file.py index.html

# Edit HTML templates for entity_xml_crud_app
python3 edit_html_file.py path/to/template.html
```

### Using the Editor Interface

1. **Panels Layout**:
   - **Left Panel (HTML Source)**: Edit your HTML code here
   - **Right Panel (Live Preview)**: See rendered HTML output
   - **Splitter (`‖`)**: Drag horizontally to resize panels

2. **Toolbar Operations**:
   - **File Operations**: Save, Open, Clear
   - **Tag Formatting**: B, I, U, P, DIV, SPAN buttons
   - All changes are reflected immediately in the preview panel

3. **Workflow**:
   - Type HTML in left panel → See results in right panel
   - Select text → Click tag button → Text gets wrapped
   - Save frequently with Save button or automatically

### Tag Insertion Methods
1. **With selection**: Select text → Click tag → Text gets wrapped
2. **Without selection**: Click tag → `<tag>text</tag>` inserted at cursor
3. **Nested tags**: Wrap already-tagged content with additional tags

### Keyboard & Mouse Controls
- **Text selection**: Standard click/drag or Shift+arrow keys
- **Tag insertion**: Click buttons with or without text selected
- **Panel resizing**: Click and drag the splitter between panels
- **File operations**: Use toolbar buttons or browser's file dialog

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

### Asset Loading
The preview automatically serves static files (CSS, JS, images) from the HTML file's directory, making it perfect for:
- Template development with linked stylesheets
- Testing image paths and relative URLs
- Debugging JavaScript functionality
- Previewing responsive designs

## How It Works

### Architecture
```
Terminal Command → Python Script → Local HTTP Server → Browser Editor
      ↓                    ↓               ↓               ↓
  File path        Content loading    Port 8080      User Interface
      ↓                    ↓               ↓               ↓
HTML file ←─── File System ←── Auto-save ←── User edits
```

### Server Details
The editor runs a local HTTP server that:
1. Serves the editor interface at `http://localhost:8080`
2. Handles file operations (open/save)
3. Manages content updates between editor and preview
4. Supports static file serving for preview assets

## Roadmap & Planned Features

### Phase 1: Core Editor (Current)
- ✓ Split-pane interface with resizable panels
- ✓ Basic tag formatting (B, I, U, P, DIV, SPAN)
- ✓ File operations (Open, Save, Clear)
- ✓ Live preview with static asset support

### Phase 2: Enhanced Features (Planned)
- 🔄 Find/Replace functionality
- 🔄 Undo/Redo operations
- 🔄 Structured tag menus (Forms, Media, Meta tags)
- 🔄 Screen keyboard and date insertion

### Phase 3: Advanced Features (Future)
- 🔲 Syntax highlighting
- 🔲 Code validation
- 🔲 Multiple file tabs
- 🔲 Export to PDF/Word
- 🔲 Template library

## Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **Port already in use** | Script auto-tries ports 8080-8099. Close conflicting apps or wait |
| **Images/CSS not loading** | Ensure asset files are in same directory or use correct relative paths |
| **Browser doesn't open** | Manually navigate to `http://localhost:8080` (or shown port) |
| **File save fails** | Check write permissions in target directory |
| **Preview not updating** | Ensure auto-refresh is working; try manual edit to trigger update |
| **Tag buttons not working** | Make sure text is selected or cursor is placed in editor |

### Port Conflicts
If you see "Address already in use", the script will automatically try the next port. Check terminal output for the actual port number.

### Static File Issues
For proper asset loading in preview:
- Keep images in same directory as HTML file
- Use relative paths: `<img src="image.jpg">`
- External URLs work normally: `<img src="https://...">`

## Stopping the Editor
- **Normal shutdown**: Press **Ctrl+C** in the terminal
- **Force quit**: Close terminal or kill Python process
- **Browser**: Simply close the browser tab/window

## Project Structure
```
edit_html_file/
├── edit_html_file.py    # Main editor script (single file!)
├── README.md           # This documentation
└── (no dependencies, no installation needed)
```

## Development Notes

### Single File Design
The entire editor is contained in one Python file for maximum portability:
- No package management required
- Easy to distribute and share
- Simple to understand and modify

### Extensibility
The modular design allows for easy addition of:
- New tag buttons and menu categories
- Additional file formats
- Custom themes/styles
- Enhanced preview features

## License
Open source - free to use, modify, and distribute.

## Related Projects
- [ArtNazarov/entity_xml_crud_app](https://github.com/ArtNazarov/entity_xml_crud_app) - Ideal companion for HTML template development
- Perfect for web development students, template designers, and quick HTML prototyping

## Version History
- **v1.0**: Initial release with split-pane editor, basic tag buttons, live preview
- **v1.1**: Added static file serving, improved UI, bug fixes
- **v1.2**: Planned - Find/Replace, Undo/Redo, expanded tag menus

---

## Quick Start Checklist
- [ ] Python 3.6+ installed
- [ ] Download `edit_html_file.py`
- [ ] Run: `python3 edit_html_file.py`
- [ ] Edit HTML in left panel
- [ ] See live preview in right panel
- [ ] Use tag buttons for quick formatting
- [ ] Save your work frequently

**Perfect for**: Quick HTML edits, template development, learning HTML, prototyping, or testing web snippets with immediate visual feedback! 
