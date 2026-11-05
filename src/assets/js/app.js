(function(){
var $=function(s,r){return (r||document).querySelector(s)},$$=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};
/* ---------- menu + header ---------- */
var b=$('#menuBtn'),n=$('#nav');
if(b&&n){b.addEventListener('click',function(){b.setAttribute('aria-expanded',String(n.classList.toggle('open')))});
 $$('#nav a').forEach(function(a){a.addEventListener('click',function(){n.classList.remove('open');b.setAttribute('aria-expanded','false')})});
 document.addEventListener('keydown',function(e){if(e.key==='Escape'&&n.classList.contains('open')){n.classList.remove('open');b.setAttribute('aria-expanded','false');b.focus()}})}
var h=$('header.top');if(h){var f=function(){h.classList.toggle('sc',window.scrollY>8)};f();window.addEventListener('scroll',f,{passive:true})}

/* ---------- projects: filter chips + image/index views ---------- */
var chips=$$('.chip[data-f]'),items=$$('.grid .card,.idx .row');
function count(){var s=$('#count');if(!s)return;var g=$('#vGrid'),n=0;$$('.card',g).forEach(function(d){if(!d.hidden)n++});s.textContent='Showing '+n+' projects'}
chips.forEach(function(c){c.addEventListener('click',function(){
 chips.forEach(function(x){var on=x===c;x.classList.toggle('on',on);x.setAttribute('aria-pressed',String(on))});
 var k=c.getAttribute('data-f');
 items.forEach(function(d){d.hidden=!(k==='all'||d.getAttribute('data-c').split(' ').indexOf(k)>-1)});count()})});
var vts=$$('.vt .chip');
vts.forEach(function(c){c.addEventListener('click',function(){
 vts.forEach(function(x){var on=x===c;x.classList.toggle('on',on);x.setAttribute('aria-pressed',String(on))});
 var list=c.getAttribute('data-v')==='list';$('#vGrid').hidden=list;$('#vList').hidden=!list})});

/* ---------- selected-work gallery ---------- */
var g=$('#gal');
if(g){var step=function(d){var s=$('.slide',g);g.scrollBy({left:d*(s?s.getBoundingClientRect().width+16:320),behavior:'smooth'})};
 var pv=$('#galPrev'),nx=$('#galNext');if(pv)pv.addEventListener('click',function(){step(-1)});if(nx)nx.addEventListener('click',function(){step(1)});
 g.addEventListener('keydown',function(e){if(e.key==='ArrowRight'){e.preventDefault();step(1)}if(e.key==='ArrowLeft'){e.preventDefault();step(-1)}})}

/* ---------- enquiry form ---------- */
var dlg=$('#enq'),form=$('#enqForm');
if(dlg&&form){
 var EMAIL=dlg.getAttribute('data-email'),EP=dlg.getAttribute('data-endpoint'),KEY=dlg.getAttribute('data-key');
 var F=function(k){return form.elements[k]},V=function(k){return (F(k).value||'').trim()};
 var msg=function(t,err){var m=$('#enqMsg');m.textContent=t||'';m.className='msg'+(err?' err':'')};
 var openD=function(){
  var nm=$('#nav');if(nm)nm.classList.remove('open');
  if(typeof dlg.showModal==='function'){if(!dlg.open)dlg.showModal()}else dlg.setAttribute('open','');
  document.documentElement.classList.add('lock');setTimeout(function(){var f=F('name');if(f)f.focus()},30)};
 var closeD=function(){if(typeof dlg.close==='function')dlg.close();else dlg.removeAttribute('open');document.documentElement.classList.remove('lock')};
 dlg.addEventListener('close',function(){document.documentElement.classList.remove('lock')});
 dlg.addEventListener('click',function(e){if(e.target===dlg)closeD()});
 $('#enqX').addEventListener('click',closeD);$$('[data-close]',dlg).forEach(function(x){x.addEventListener('click',closeD)});
 $$('a[data-enquire]').forEach(function(a){a.addEventListener('click',function(e){if(e.metaKey||e.ctrlKey||e.shiftKey||e.button)return;e.preventDefault();openD()})});
 if(location.hash==='#enquire')openD();
 var subject=function(){return 'Project enquiry'+(V('name')?' from '+V('name'):'')};
 var body=function(){return ['Hello OTI Architects,','','My name: '+V('name'),'Phone: '+V('phone'),'Email: '+V('email'),'Project type: '+V('type'),'Location: '+V('location'),'','About the project:',V('details')].join('\r\n')};
 var valid=function(){F('email').setCustomValidity(!V('email')&&!V('phone')?'Please give a phone number or an email address so we can reply.':'');
  if(!V('name')){F('name').setCustomValidity('Please tell us your name.')}else F('name').setCustomValidity('');
  if(!V('details')){F('details').setCustomValidity('Please add a few words about the project.')}else F('details').setCustomValidity('');
  return form.reportValidity()};
 ['name','phone','email','details'].forEach(function(k){F(k).addEventListener('input',function(){F('email').setCustomValidity('');F('name').setCustomValidity('');F('details').setCustomValidity('')})});
 var copy=function(t,ok,bad){
  var fb=function(){var a=document.createElement('textarea');a.value=t;a.className='sr';document.body.appendChild(a);a.select();var r=false;try{r=document.execCommand('copy')}catch(e){}a.remove();r?ok():bad()};
  if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(t).then(ok,fb)}else fb()};
 var q=encodeURIComponent;
 $$('[data-way]',dlg).forEach(function(btn){btn.addEventListener('click',function(){
  if(!valid())return;var w=btn.getAttribute('data-way'),su=subject(),bd=body();
  if(w==='gmail'){window.open('https://mail.google.com/mail/?view=cm&fs=1&to='+q(EMAIL)+'&su='+q(su)+'&body='+q(bd),'_blank','noopener');msg('Gmail is opening in a new tab. Press Send there to finish.')}
  else if(w==='outlook'){window.open('https://outlook.office.com/mail/deeplink/compose?to='+q(EMAIL)+'&subject='+q(su)+'&body='+q(bd),'_blank','noopener');msg('Outlook is opening in a new tab. Press Send there to finish.')}
  else if(w==='app'){location.href='mailto:'+EMAIL+'?subject='+q(su)+'&body='+q(bd);msg('If your email app did not open, choose Gmail, Outlook or Copy message instead.')}
  else{copy('To: '+EMAIL+'\r\nSubject: '+su+'\r\n\r\n'+bd,function(){msg('Copied. Paste it into any email and send it to '+EMAIL+'.')},function(){msg('Copy was blocked by your browser. Please email '+EMAIL+' directly.',true)})}})});
 $$('[data-copy]',dlg).forEach(function(c){c.addEventListener('click',function(){copy(c.getAttribute('data-copy'),function(){c.textContent='Copied'},function(){c.textContent='Select and copy'});setTimeout(function(){c.textContent='Copy address'},2500)})});
 var done=function(){$('#enqBody').hidden=true;msg('');$('#enqDone').hidden=false};
 form.addEventListener('submit',function(e){
  e.preventDefault();if(!EP)return;if(V('website')){done();return}if(!valid())return;
  var s=$('#enqSend');s.disabled=true;msg('Sending...');
  var data={name:V('name'),phone:V('phone'),email:V('email'),project_type:V('type'),location:V('location'),message:V('details'),subject:subject()};if(KEY)data.access_key=KEY;
  fetch(EP,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(data)})
   .then(function(r){return r.json().catch(function(){return {}}).then(function(j){if(r.ok&&j.success!==false&&j.ok!==false){done()}else throw 0})})
   .catch(function(){s.disabled=false;var d=$('details.alt',dlg);if(d)d.open=true;msg('We could not send this just now. Please use one of the email options below, or call us.',true)})});
}
})();

/* ================= motion layer ================= */
(function(){
var d=document,r=d.documentElement,W=window,$=function(s,x){return(x||d).querySelector(s)},$$=function(s,x){return[].slice.call((x||d).querySelectorAll(s))};
var rm=r.classList.contains('rmx'),cl=function(v,a,b){return Math.max(a,Math.min(b,v))};
var mt=$('.mt');if(mt){mt.textContent=rm?'Play animation':'Pause animation';mt.setAttribute('aria-pressed',String(rm));
 mt.addEventListener('click',function(){try{localStorage.setItem('oti-motion',rm?'on':'off')}catch(e){}location.reload()})}
/* the opening plays once per visit and can be skipped by scrolling, tapping or pressing a key */
if(!rm&&$('.hero')){['wheel','keydown','pointerdown','touchstart'].forEach(function(e){W.addEventListener(e,function(){r.classList.add('sk')},{once:true,passive:true})});try{sessionStorage.setItem('oti-intro','1')}catch(e){}}
/* page transitions */
if(!rm){W.addEventListener('pageshow',function(e){if(e.persisted)r.classList.remove('go')});
 d.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href]');
  if(!a||e.defaultPrevented||e.metaKey||e.ctrlKey||e.shiftKey||e.button||a.target||a.hasAttribute('data-enquire')||a.hasAttribute('download'))return;
  var u=new URL(a.href,location.href);if(u.origin!==location.origin||u.protocol==='mailto:'||u.protocol==='tel:')return;
  if(u.pathname===location.pathname&&u.hash)return;if(u.href===location.href)return;
  e.preventDefault();r.classList.add('go');setTimeout(function(){location.href=u.href},320)})}
/* headlines rise word by word; section lines draw as they enter */
var io=W.IntersectionObserver&&new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{threshold:.35});
$$('.hero h1,.ph h1,main h2:not(.sr),.band blockquote').forEach(function(el){
 if(!rm&&!el.querySelector('a,svg,img')){var t=el.textContent.trim().split(/\s+/);el.setAttribute('aria-label',t.join(' '));el.textContent='';
  t.forEach(function(w,i){var s=d.createElement('span'),q=d.createElement('i');s.className='hw';s.setAttribute('aria-hidden','true');q.textContent=w;q.style.setProperty('--i',i);s.appendChild(q);el.appendChild(s);el.appendChild(d.createTextNode(' '))})}
 if(io)io.observe(el);else el.classList.add('in')});
/* scroll-linked: hero drift, image parallax, services line */
var hero=$('.hero'),sv=$('.svcs'),gal=$('#gal'),ims=$$('.im img'),slides=$$('.slide img'),tick=false;
function frame(){tick=false;if(rm)return;var y=W.scrollY,vh=W.innerHeight;
 if(hero&&y<vh*1.2)hero.style.setProperty('--sy',y);
 ims.forEach(function(im){var b=im.parentNode.getBoundingClientRect();if(b.bottom<-50||b.top>vh+50)return;im.style.setProperty('--py',(((b.top+b.height/2-vh/2)/vh)*-26)+'px')});
 if(sv){var b=sv.getBoundingClientRect();sv.style.setProperty('--sp',cl((vh*.72-b.top)/b.height,0,1))}}
function req(){if(!tick){tick=true;requestAnimationFrame(frame)}}
W.addEventListener('scroll',req,{passive:true});W.addEventListener('resize',req);req();
function shift(){var vw=W.innerWidth;slides.forEach(function(im){var b=im.parentNode.getBoundingClientRect();im.style.setProperty('--px',(((b.left+b.width/2-vw/2)/vw)*-60)+'px')})}
if(gal&&!rm){gal.addEventListener('scroll',function(){requestAnimationFrame(shift)},{passive:true});shift()}
/* pointer: hero follows the mouse; gallery drags */
if(!rm&&W.matchMedia('(pointer:fine)').matches){
 if(hero)hero.addEventListener('pointermove',function(e){hero.style.setProperty('--mx',(e.clientX/W.innerWidth*2-1).toFixed(3));hero.style.setProperty('--my',(e.clientY/W.innerHeight*2-1).toFixed(3))});
 if(gal){var dn=false,sx=0,sl=0,mv=0;
  gal.addEventListener('pointerdown',function(e){if(e.button)return;dn=true;mv=0;sx=e.clientX;sl=gal.scrollLeft});
  W.addEventListener('pointermove',function(e){if(!dn)return;var dx=e.clientX-sx;mv=Math.max(mv,Math.abs(dx));if(mv>6)gal.classList.add('drag');gal.scrollLeft=sl-dx});
  W.addEventListener('pointerup',function(e){if(!dn)return;dn=false;var dx=e.clientX-sx,sl2=$$('.slide',gal),st=sl2.length>1?sl2[1].offsetLeft-sl2[0].offsetLeft:gal.clientWidth;gal.classList.remove('drag');if(Math.abs(dx)>50&&sl2.length)gal.scrollTo({left:Math.max(0,sl+(dx<0?st:-st)),behavior:'smooth'})});
  gal.addEventListener('click',function(e){if(mv>6){e.preventDefault();e.stopPropagation()}},true);
  gal.addEventListener('dragstart',function(e){e.preventDefault()})}}
})();
