(function(){
var $=function(s){return document.querySelector(s)},$$=function(s){return [].slice.call(document.querySelectorAll(s))};
var b=$('#menuBtn'),n=$('#nav');
if(b&&n){b.addEventListener('click',function(){b.setAttribute('aria-expanded',String(n.classList.toggle('open')))});
 $$('#nav a').forEach(function(a){a.addEventListener('click',function(){n.classList.remove('open');b.setAttribute('aria-expanded','false')})});
 document.addEventListener('keydown',function(e){if(e.key==='Escape'&&n.classList.contains('open')){n.classList.remove('open');b.setAttribute('aria-expanded','false');b.focus()}})}
var h=$('header.top');if(h){var f=function(){h.classList.toggle('sc',window.scrollY>8)};f();window.addEventListener('scroll',f,{passive:true})}
var chips=$$('.chip');
chips.forEach(function(c){c.addEventListener('click',function(){
 chips.forEach(function(x){var on=x===c;x.classList.toggle('on',on);x.setAttribute('aria-pressed',String(on))});
 var k=c.getAttribute('data-f'),cards=$$('.grid .card'),shown=0;
 cards.forEach(function(d){var ok=k==='all'||d.getAttribute('data-c').split(' ').indexOf(k)>-1;d.hidden=!ok;if(ok)shown++});
 var s=$('#count');if(s)s.textContent='Showing '+shown+' projects'})});
})();
