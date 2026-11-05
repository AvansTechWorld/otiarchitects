/* Runs first. Marks the page as script-enabled and blocks framing (clickjacking). */
document.documentElement.className+=' js';
if(window.top!==window.self){try{window.top.location=window.self.location}catch(e){document.documentElement.hidden=true}}

try{var P=localStorage.getItem('oti-motion'),O=matchMedia('(prefers-reduced-motion:reduce)').matches;if(P==='on')document.documentElement.className+=' fm';if(P==='off'||(O&&P!=='on'))document.documentElement.className+=' rmx'}catch(e){if(matchMedia('(prefers-reduced-motion:reduce)').matches)document.documentElement.className+=' rmx'}
