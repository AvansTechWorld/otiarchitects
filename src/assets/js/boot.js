/* Runs first. Marks the page as script-enabled and blocks framing (clickjacking). */
document.documentElement.className+=' js';
if(window.top!==window.self){try{window.top.location=window.self.location}catch(e){document.documentElement.hidden=true}}
