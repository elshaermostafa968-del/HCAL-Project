'use strict';
const $ = s => document.querySelector(s);
const chat = $('#chat'), quick = $('#quick'), box = $('#message');
let busy=false, closed=false, last=null, response=null, hint=1, controller=null;
let session=crypto.randomUUID();
let gState='full';
let stage=1, exampleSeen=false, guidedComplete=false;
const sample={message:'Check APA missing year: Earlier research supports this claim (Nadir).',style:'APA',category:'Citation & Formatting',hint_level:1};
function updateStage(){
 $('#step-label').textContent='Step '+stage+' of 3'+(stage===1?': see an example':'')+((stage===1&&exampleSeen)||(stage===2&&guidedComplete)?' ✓':'');
 $('#onboarding').classList.toggle('independent',stage===3);
 $('#onboarding-title').textContent=stage===1?'See an example':stage===2?'Try with guidance':'Work on your own';
 $('#stage-description').textContent=stage===1?'See a worked fictional example. The rule, source, and limits appear with the answer.':stage===2?'Try the fictional citation with guidance. Choose APA, submit it, then inspect Why this rule? and use a hint. Revise it yourself.':'Work independently on a fictional excerpt. Hints, sources, Help, and Talk to a person remain available on request.';
 $('#stage-primary').textContent=stage===1?(exampleSeen?'Continue to co-pilot':'See an example'):stage===2?(guidedComplete?'Continue independently':'Load guided task'):'Restart guided onboarding';
 const bc=$('#bar-continue');bc.hidden=stage===3||gState==='full';bc.textContent=$('#stage-primary').textContent;
 $('#stage-status').textContent=stage===1?(exampleSeen?'Example complete. Notice the source and Mandatory rule label.':''):stage===2?(guidedComplete?'Guided check complete. Review the evidence, then continue when ready.':'You choose when to move on; no skill score or proficiency claim is made.'):'Independent mode. Request help whenever you want.';
}
$('#stage-primary').onclick=()=>{if(busy)return;if(stage===1){if(exampleSeen){stage=2;updateStage();}else{$('#style').value='APA';send({...sample});}}else if(stage===2){if(guidedComplete){stage=3;updateStage();box.value='';initialQuick();box.focus();}else{$('#style').value='APA';box.value=sample.message;say('Guided task: choose APA, send the fictional citation, open Why this rule?, and try one hint. The year must come from the real source, never a guess.');box.focus();}}else{stage=1;exampleSeen=false;guidedComplete=false;updateStage();}};
$('#stage-skip').onclick=()=>{if(busy)return;stage=3;updateStage();box.focus();};
$('#restart-onboarding').onclick=()=>{if(busy)return;stage=1;exampleSeen=false;guidedComplete=false;updateStage();};
const contacts = [
 {title:'Your course instructor',detail:'Use the contact in your syllabus. Ask which local requirement applies.'},
 {title:'Your university writing center or librarian',detail:'Find the right service on your university website.'},
 {title:'APA official guidance',url:'https://apastyle.apa.org/style-grammar-guidelines/citations/basic-principles'},
 {title:'MLA official guidance',url:'https://style.mla.org/in-text-citations-overview/'},
 {title:'IEEE official guide',url:'https://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/IEEE-Reference-Guide.pdf'}
];
function node(tag,text,cls){const e=document.createElement(tag);if(text)e.textContent=text;if(cls)e.className=cls;return e;}
function entry(who){const e=node('article',null,'entry '+(who==='You'?'user':who.toLowerCase()));e.append(node('span',who,'who'));chat.append(e);return e;}
function say(text){entry('Coach').append(node('p',text));scroll();}
function scroll(){requestAnimationFrame(()=>{const area=$('#session-scroll');area.scrollTop=area.scrollHeight;});}
function button(text,fn){const b=node('button',text);b.type='button';b.onclick=fn;return b;}
function initialQuick(){quick.replaceChildren();[['Check a paragraph',()=>choose('paragraph')],['Verify a citation',()=>choose('citation')],['How does this work?',help]] .forEach(([t,f])=>quick.append(button(t,f)));}
function followQuick(){quick.replaceChildren();
 [['Previous hint',()=>changeHint(-1)],['Next hint',()=>changeHint(1)],['Why this rule?',()=>{const panels=chat.querySelectorAll('details');const d=panels[panels.length-1];if(d){d.open=true;d.scrollIntoView({block:'nearest'});}}],['Show source only',()=>{if(response?.evidence)say(response.evidence.source+'\n'+response.evidence.source_url);} ],['Check another',()=>{closed=false;last=null;response=null;initialQuick();box.focus();}],['Edit last message',()=>{if(last){box.value=last.message;closed=false;box.focus();}}],["I'm done",closure]].forEach(([t,f])=>quick.append(button(t,f)));}
function welcome(){const e=entry('Coach');e.append(node('p',"I'm an AI and I can make mistakes, so every answer comes with its source."),node('div','Try this fictional example: Earlier research supports this claim (Nadir).\nQuestion: Is an author-date element missing? Choose APA first.','example'));initialQuick();}
function help(){say('1. Choose a style guide and share a fictional excerpt with one question.\n2. I retrieve one case from 40 synthetic examples. A similarity score is not confidence.\n3. Check the source and distinguish Mandatory rule from Style suggestion.\n4. Revise in your own words. Use Next hint, or contact a person if context is missing.\nLocal mode uses fixed dataset feedback, not a live model. Hosted mode calls a model from this backend, with strict extractive validation.');}
function choose(type){closed=false;if(type==='citation'&&$('#style').value==='General')$('#style').value='APA';box.value=type==='citation'?'Check APA missing year: Earlier research supports this claim (Nadir).':'';say(type==='citation'?'Choose the style required by your assignment, then check this fictional citation or add another.':'Paste a fictional paragraph and tell me what concerns you.');box.focus();}
function setBusy(v){if(v&&clearSnapshot){clearSnapshot=null;clearTimeout(clearTimer);$('#clear-toast').hidden=true;}busy=v;$('#send').disabled=v;quick.querySelectorAll('button').forEach(b=>b.disabled=v);$('#status').textContent=v?'Checking the style guide...':'';}
async function send(payload,showUser=true){if(busy)return;closed=false;last=payload;hint=payload.hint_level;setBusy(true);if(showUser)entry('You').append(node('p',payload.message));scroll();controller=new AbortController();const timer=setTimeout(()=>controller.abort(),28000);
 try{const r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload),signal:controller.signal});if(!r.ok)throw Error(r.status===422?'Please keep the message between 1 and 4,000 characters and choose a supported style.':'The backend could not complete this request.');response=await r.json();render(response);}
 catch(err){say(err.name==='AbortError'?'The request took too long. Your text is still in this tab. Try again or talk to a person.':err.message+' Your text is still in this tab.');quick.replaceChildren(button('Try again',()=>send(last,false)),button('Talk to a person',handover));}
 finally{clearTimeout(timer);controller=null;setBusy(false);scroll();}}
function render(data){const e=entry('Coach');e.append(node('span',data.mode==='local'?'Local demo · No live model':data.live_model_response?'Live model · Backend response':'Backend · '+data.status,'badge '+(data.mode==='local'?'local':'')));if(data.label)e.append(node('span',data.label==='mandatory_rule'?'Mandatory rule':'Style suggestion','badge'));e.append(node('p',data.message));
 if(data.hint)e.append(node('div','Hint '+data.hint_level+' / 3 · '+data.hint,'hint'));
 if(data.uncertainty_note)e.append(node('div',(data.status==='ok'?'Limit: ':'Uncertainty: ')+data.uncertainty_note,'notice'));
 if(data.evidence){const x=data.evidence;const d=node('details');d.append(node('summary','Why this rule? · '+x.rule_id));d.append(node('p',x.rule));const a=node('a',x.source);a.href=x.source_url;a.target='_blank';a.rel='noopener noreferrer';d.append(a,node('p','Evidence similarity: '+x.score+' / 1. '+x.score_note),node('p','Matched terms: '+x.matched_terms.join(', ')),node('p','Retrieved rule set: '+x.retrieved_set.join(', ')));e.append(d);}
 const ratings=node('div',null,'rating');ratings.append(node('span','Was this helpful?'),button('Yes, helpful',()=>rate(data,true,'clear',ratings)),button('Not helpful',()=>reasonForm(data,ratings)));e.append(ratings);
 if(data.status==='ok'){if(stage===1)exampleSeen=true;else if(stage===2)guidedComplete=true;updateStage();followQuick();}else{initialQuick();if(data.status==='error')quick.prepend(button('Try again',()=>send(last,false)));}scroll();}
function reasonForm(data,target){target.replaceChildren();const label=node('label','What did not help? ');const select=node('select');['unclear','wrong_rule','not_relevant','too_complex','other'].forEach(v=>{const o=node('option',v.replaceAll('_',' '));o.value=v;select.append(o);});label.append(select);target.append(label,button('Send feedback',()=>rate(data,false,select.value,target)));select.focus();}
async function rate(data,helpful,reason,target){try{const r=await fetch('/feedback',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({response_id:data.response_id,session_id:session,helpful,reason})});if(!r.ok)throw Error();const result=await r.json();target.replaceChildren(node('span',result.status==='recorded'?'Thank you. Your rating was recorded.':result.message));if(result.offer_handover){say('Two suggestions have not helped. It may be better to pause and contact a person.');handover();}}catch{target.append(node('span','Rating not saved. Please try again.'));}}
function changeHint(delta){if(!last||!response?.evidence)return;const n=Math.min(3,Math.max(1,hint+delta));if(n===hint){say(delta>0?'That was the final hint. Try your own revision or talk to a person.':'You are on the first hint.');return;}send({...last,hint_level:n},false);}
function closure(){if(busy)return;closed=true;say(response?.evidence?'Session summary: review '+response.evidence.rule_id+' and apply this rule in your own words: '+response.evidence.rule+' No draft has been rewritten. You can clear this chat or start another check.':'Session paused. Keep your draft and assignment instructions ready for your instructor or writing center. You can clear this chat or start another check.');quick.replaceChildren(button('Clear chat',clearChat),button('Check another',()=>{closed=false;initialQuick();box.focus();}));}
function handover(){const area=$('#contacts');area.replaceChildren();contacts.forEach(c=>{const s=node('section');s.append(node('h3',c.title));if(c.detail)s.append(node('p',c.detail));if(c.url){const a=node('a','Open official guide');a.href=c.url;a.target='_blank';a.rel='noopener noreferrer';s.append(a);}area.append(s);});$('#handover').showModal();if(!busy)closure();}
let clearSnapshot=null,clearTimer=null;
function clearChat(){if(busy){say('Please wait for this check to finish before clearing.');return;}clearSnapshot={nodes:Array.from(chat.childNodes),quickNodes:Array.from(quick.childNodes),last,response,hint,closed,session,stage,exampleSeen,guidedComplete,text:box.value,style:$('#style').value,guidance:gState,prevG};clearTimeout(clearTimer);$('#clear-toast').hidden=false;clearTimer=setTimeout(()=>{clearSnapshot=null;$('#clear-toast').hidden=true;},6000);chat.replaceChildren();last=null;response=null;hint=1;closed=false;session=crypto.randomUUID();stage=1;exampleSeen=false;guidedComplete=false;updateStage();box.value='';welcome();box.focus();}
$('#composer').onsubmit=e=>{e.preventDefault();const text=box.value.trim();if(!text||busy)return;box.value='';send({message:text,style:$('#style').value,category:'Auto',hint_level:1});};
box.onkeydown=e=>{if(e.key==='Enter'&&!e.shiftKey&&!e.isComposing){e.preventDefault();$('#composer').requestSubmit();}};
$('#human').onclick=handover;$('#close-human').onclick=()=>$('#handover').close();$('#clear').onclick=clearChat;$('#help').onclick=help;
updateStage();
welcome();
fetch('/health').then(r=>r.json()).then(d=>{$('#mode').textContent=d.provider==='local'?'Local demo · 40 teaching cases\nNo API key. No live model.':d.configured?'Live provider · '+d.provider.toUpperCase()+'\nSynthetic excerpts are sent to this provider.':'Provider not configured · Add your key on the server.';}).catch(()=>{$('#mode').textContent='Backend unreachable · Start FastAPI, then reload.';});

// About expands the information panel without resetting the conversation.
$('#about-toggle').onclick=()=>{
 const panel=$('#about-panel');
 panel.hidden=!panel.hidden;
 $('#about-toggle').setAttribute('aria-expanded',String(!panel.hidden));
};


function setGuidance(mode){gState=mode;{const bc=$('#bar-continue');bc.hidden=stage===3||mode==='full';}const o=$('#onboarding');o.hidden=mode==='hidden';$('#onboarding-content').hidden=mode!=='full';$('#guidance-show').hidden=mode!=='hidden';}
$('#onboarding-toggle').onclick=()=>{prevG=gState;setGuidance('hidden');};
let prevG='full';
$('#guidance-show').onclick=()=>{setGuidance(prevG==='hidden'?'bar':prevG);};
$('#bar-continue').onclick=()=>$('#stage-primary').click();
$('#undo-clear').onclick=()=>{if(!clearSnapshot)return;clearTimeout(clearTimer);const s=clearSnapshot;chat.replaceChildren(...s.nodes);quick.replaceChildren(...s.quickNodes);({last,response,hint,closed,session,stage,exampleSeen,guidedComplete}=s);box.value=s.text;$('#style').value=s.style;updateStage();setGuidance(s.guidance);clearSnapshot=null;$('#clear-toast').hidden=true;scroll();};
const stageAction=$('#stage-primary').onclick;$('#stage-primary').onclick=()=>{stageAction();setGuidance('bar');};
const skipAction=$('#stage-skip').onclick;$('#stage-skip').onclick=()=>{skipAction();setGuidance('bar');};
const restartAction=$('#restart-onboarding').onclick;$('#restart-onboarding').onclick=()=>{restartAction();setGuidance('full');};

$('#close-about').onclick=()=>{$('#about-panel').hidden=true;$('#about-toggle').setAttribute('aria-expanded','false');$('#about-toggle').focus();};
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!$('#about-panel').hidden)$('#close-about').click();});

// Quick replies sit in the Citation style row once the chat has messages.
const quickHome=quick.parentNode;
function placeQuick(){const has=!!chat.querySelector('.entry.user');const slot=$('#quick-slot');if(has&&quick.parentNode!==slot)slot.append(quick);else if(!has&&quick.parentNode!==quickHome)quickHome.append(quick);}
new MutationObserver(placeQuick).observe(chat,{childList:true});
placeQuick();
