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
