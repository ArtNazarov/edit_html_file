// Main Menu Generator
function makeMainMenu() {
    const menuContainer = document.getElementById('main-menu-container');
    menuContainer.innerHTML = '';
    
    const menuBar = document.createElement('ul');
    menuBar.className = 'menu-bar';
    
    // File Menu
    const fileMenu = createMenuItem('File', [
        {text: 'New', action: 'newFile'},
        {text: 'Open...', action: 'openFile'},
        {text: 'Save', action: 'saveFile'},
        {text: 'Save As...', action: 'saveAsFile'},
        {text: '---'},
        {text: 'Exit', action: 'exitApp'}
    ]);
    menuBar.appendChild(fileMenu);
    
    // Edit Menu
    const editMenu = createMenuItem('Edit', [
        {text: 'Undo', action: 'undo'},
        {text: 'Redo', action: 'redo'},
        {text: '---'},
        {text: 'Cut', action: 'cut'},
        {text: 'Copy', action: 'copy'},
        {text: 'Paste', action: 'paste'},
        {text: '---'},
        {text: 'Find/Replace...', action: 'findReplace'}
    ]);
    menuBar.appendChild(editMenu);
    
    // Actions Menu
    const actionsMenu = createMenuItem('Actions', [
        {text: 'Insert Date', action: 'insertDate'},
        {text: 'Screen Keyboard', action: 'screenKeyboard'}
    ]);
    menuBar.appendChild(actionsMenu);
    
    // Structure Menu
    const structureMenu = createMenuItem('Structure', [
        {text: 'main', action: 'insertTag', data: 'main'},
        {text: 'section', action: 'insertTag', data: 'section'},
        {text: 'article', action: 'insertTag', data: 'article'},
        {text: 'aside', action: 'insertTag', data: 'aside'},
        {text: 'header', action: 'insertTag', data: 'header'},
        {text: 'footer', action: 'insertTag', data: 'footer'},
        {text: 'nav', action: 'insertTag', data: 'nav'},
        {text: 'address', action: 'insertTag', data: 'address'},
        {text: '---'},
        {
            text: 'Definitions', 
            submenu: [
                {text: 'dl', action: 'insertTag', data: 'dl'},
                {text: 'dt', action: 'insertTag', data: 'dt'},
                {text: 'dd', action: 'insertTag', data: 'dd'}
            ]
        }
    ]);
    menuBar.appendChild(structureMenu);
    
    // Forms Menu
    const formsMenu = createMenuItem('Forms', [
        {text: 'New Form', action: 'insertForm'},
        {text: 'input text', action: 'insertInput', data: 'text'},
        {text: 'input password', action: 'insertInput', data: 'password'},
        {text: 'checkbox', action: 'insertInput', data: 'checkbox'},
        {text: 'radio', action: 'insertInput', data: 'radio'},
        {text: 'hidden input', action: 'insertInput', data: 'hidden'},
        {text: 'select', action: 'insertSelect'},
        {text: 'option', action: 'insertOption'},
        {text: 'textarea', action: 'insertTextarea'},
        {text: 'output', action: 'insertTag', data: 'output'}
    ]);
    menuBar.appendChild(formsMenu);
    
    // Media Menu
    const mediaMenu = createMenuItem('Media', [
        {text: 'video', action: 'insertVideo'},
        {text: 'audio', action: 'insertAudio'}
    ]);
    menuBar.appendChild(mediaMenu);
    
    // Meta Menu
    const metaMenu = createMenuItem('Meta', [
        {text: 'meta description', action: 'insertMeta', data: 'description'},
        {text: 'meta author', action: 'insertMeta', data: 'author'}
    ]);
    menuBar.appendChild(metaMenu);
    
    // Help Menu
    const helpMenu = createMenuItem('Help', [
        {text: 'About', action: 'showAbout'},
        {text: 'Documentation', action: 'showDocs'}
    ]);
    menuBar.appendChild(helpMenu);
    
    menuContainer.appendChild(menuBar);
}

function createMenuItem(label, items) {
    const li = document.createElement('li');
    li.className = 'menu-item';
    li.textContent = label;
    
    if (items && items.length > 0) {
        const submenu = document.createElement('ul');
        submenu.className = 'submenu';
        
        items.forEach(item => {
            if (item === '---') {
                const hr = document.createElement('hr');
                hr.style.margin = '5px 0';
                hr.style.border = 'none';
                hr.style.borderTop = '1px solid #404565';
                submenu.appendChild(hr);
            } else if (item.submenu) {
                const submenuItem = document.createElement('li');
                submenuItem.className = 'submenu-item has-submenu';
                submenuItem.textContent = item.text;
                
                const subsubmenu = document.createElement('ul');
                subsubmenu.className = 'subsubmenu';
                
                item.submenu.forEach(subitem => {
                    const subsubmenuItem = document.createElement('li');
                    subsubmenuItem.className = 'subsubmenu-item';
                    subsubmenuItem.textContent = subitem.text;
                    subsubmenuItem.onclick = function(e) {
                        e.stopPropagation();
                        handleMenuItemClick(subitem.action, subitem.data);
                    };
                    subsubmenu.appendChild(subsubmenuItem);
                });
                
                submenuItem.appendChild(subsubmenu);
                submenu.appendChild(submenuItem);
            } else {
                const menuItem = document.createElement('li');
                menuItem.className = 'submenu-item';
                menuItem.textContent = item.text;
                menuItem.onclick = function(e) {
                    e.stopPropagation();
                    handleMenuItemClick(item.action, item.data);
                };
                submenu.appendChild(menuItem);
            }
        });
        
        li.appendChild(submenu);
    }
    
    return li;
}

function handleMenuItemClick(action, data) {
    console.log('Menu action:', action, 'Data:', data);
    if (typeof window.handleAction === 'function') {
        window.handleAction(action, data);
    }
}

// Expose to window
window.makeMainMenu = makeMainMenu;
window.handleMenuItemClick = handleMenuItemClick;