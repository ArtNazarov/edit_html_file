
// Example: highlight "function", "// comment", and strings
            function highlight(text) {
            return text
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/("(?:[^"\\]|\\.)*")/g, '<span style="color:#d73a49;text-shadow: 0 0 7px yellow;font-weight:700;">$1</span>') // strings
                .replace(/(\/\/.*)/g, '<span style="color:blue;font-weight:500;text-shadow: 0 0 8px cyan">$1</span>')           // comments
                .replace(/\b(function|return|if|else|for|while)\b/g, '<span style="color:white;text-shadow: 0 0 3px #ff0000, 0 0 5px #ff00ff;">$1</span>');
            }

            function  colorer(editor, highlight){
                const text = editor.value;
                highlighter.innerHTML = highlight(text) || '\n'; // prevent collapse
                highlighter.style.height = editor.scrollHeight + 'px';

            }

            function ApplyHighlight(editor, highlighter){
                 editor.addEventListener('input', () => {
                    colorer(editor, highlighter);
                });

                // Optional: sync scroll
                editor.addEventListener('scroll', () => {
                highlighter.scrollTop = editor.scrollTop;
                });
            }