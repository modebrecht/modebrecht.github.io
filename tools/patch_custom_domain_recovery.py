from pathlib import Path

path = Path('bo2026-recovery.html')
html = path.read_text(encoding='utf-8')

html = html.replace(
    'content="BO2026 Notfall-Recovery für Vercel und Render."',
    'content="BO2026 Notfall-Recovery für Vercel, Render und eigene Domains."',
    1,
)

css_marker = '.raw-result{margin-top:8px;color:var(--muted);font-size:.78rem}'
css_add = css_marker + '.custom-source{margin-top:12px;padding:13px;border:1px solid var(--line);border-radius:14px;background:rgba(255,255,255,.025)}.custom-source label{display:block;margin-bottom:8px;color:#dbe5f5;font-size:.8rem;font-weight:800}.custom-row{display:grid;gap:8px}.custom-row input{width:100%;min-height:50px;padding:11px 13px;border:1px solid var(--line);border-radius:12px;background:#080d19;color:var(--text);outline:none}.custom-row input:focus{border-color:rgba(120,148,255,.62);box-shadow:0 0 0 2px rgba(120,148,255,.09)}.custom-error{min-height:18px;margin-top:7px;color:var(--red);font-size:.74rem}'
if css_marker not in html:
    raise SystemExit('CSS marker not found')
html = html.replace(css_marker, css_add, 1)
html = html.replace(
    '@media(min-width:650px){.shell{padding-inline:24px}.choices.two{grid-template-columns:1fr 1fr}.choices.three{grid-template-columns:repeat(3,1fr)}.actions.two{grid-template-columns:1fr 1fr}.panel-inner,.result{padding:24px}}',
    '@media(min-width:650px){.shell{padding-inline:24px}.choices.two{grid-template-columns:1fr 1fr}.choices.three{grid-template-columns:repeat(3,1fr)}.actions.two{grid-template-columns:1fr 1fr}.custom-row{grid-template-columns:1fr auto}.custom-row .btn{min-width:130px}.panel-inner,.result{padding:24px}}',
    1,
)

old_sources = '''        <div class="choices two" id="sourceChoices">
          <button class="choice" data-source="vercel"><strong>Vercel</strong><span>bo2026.vercel.app</span></button>
          <button class="choice" data-source="render"><strong>Render</strong><span>dev-bo2026.onrender.com</span></button>
        </div>'''
new_sources = '''        <div class="choices three" id="sourceChoices">
          <button class="choice" data-source="vercel"><strong>Vercel</strong><span>bo2026.vercel.app</span></button>
          <button class="choice" data-source="render"><strong>Render</strong><span>dev-bo2026.onrender.com</span></button>
          <button class="choice" data-source="custom"><strong>Eigene Domain</strong><span>z. B. bo.schule.ch</span></button>
        </div>
        <div class="custom-source hidden" id="customSource">
          <label for="customDomain">Domain oder URL eingeben</label>
          <div class="custom-row"><input id="customDomain" type="text" inputmode="url" autocomplete="url" placeholder="bo.schule.ch"><button class="btn" id="customUse" type="button">Verwenden</button></div>
          <div class="custom-error" id="customError"></div>
        </div>'''
if old_sources not in html:
    raise SystemExit('Source choices marker not found')
html = html.replace(old_sources, new_sources, 1)

start = html.index('const TARGETS={')
end = html.index('function J(s)', start)
new_js = r'''const EXE='https://github.com/modebrecht/modebrecht.github.io/releases/download/bo2026-recovery-latest/BO2026-Recovery-Windows.exe';
const SHA='https://github.com/modebrecht/modebrecht.github.io/releases/download/bo2026-recovery-latest/BO2026-Recovery-Windows.exe.sha256';
const TARGETS={
  vercel:{name:'Vercel',host:'bo2026.vercel.app',origin:'https://bo2026.vercel.app',otherName:'Render',other:'https://dev-bo2026.onrender.com/',exe:EXE,sha:SHA},
  render:{name:'Render',host:'dev-bo2026.onrender.com',origin:'https://dev-bo2026.onrender.com',otherName:'Vercel',other:'https://bo2026.vercel.app/',exe:EXE,sha:SHA}
};
let source=null,device=null,customTarget=null;
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const basePy=$('#recoveryPython').textContent;
function normalizeCustom(raw){let value=String(raw||'').trim();if(!value)throw new Error('Bitte eine Domain eingeben.');if(!/^[a-zA-Z][a-zA-Z0-9+.-]*:\/\//.test(value))value='https://'+value;let u;try{u=new URL(value)}catch{throw new Error('Domain/URL nicht erkannt.')}if(!['http:','https:'].includes(u.protocol))throw new Error('Nur http:// oder https:// verwenden.');if(u.username||u.password)throw new Error('Keine Zugangsdaten in der URL verwenden.');if(!u.hostname)throw new Error('Keine gültige Domain erkannt.');return{name:'Eigene Domain',host:u.host,origin:u.origin,custom:true,exe:EXE,sha:SHA};}
function target(){return source==='custom'?customTarget:TARGETS[source]||null}
function pyForTarget(t){if(!t)return basePy;const a='HOST="bo2026.vercel.app"; ORIGIN="https://bo2026.vercel.app"; KIND="cv-cover-charm-dossier"; VERSION=1';const b=`HOST="${t.host}"; ORIGIN="${t.origin}"; KIND="cv-cover-charm-dossier"; VERSION=1`;return basePy.replace(a,b)}
function downloadText(name,text,type='text/plain'){const b=new Blob([text],{type}),a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)}
async function copyText(text,btn){try{await navigator.clipboard.writeText(text);const old=btn.textContent;btn.textContent='✓ Kopiert';setTimeout(()=>btn.textContent=old,900)}catch{}}
function choose(kind,value){const selector=kind==='source'?'[data-source]':'[data-device]';$$(selector).forEach(b=>b.classList.toggle('active',b.dataset[kind]===value));if(kind==='source'){source=value;device=null;$$('[data-device]').forEach(b=>b.classList.remove('active'));$('#resultPanel').classList.add('hidden');if(value==='custom'){customTarget=null;$('#customSource').classList.remove('hidden');$('#devicePanel').classList.add('hidden');$('#customError').textContent='';setTimeout(()=>$('#customDomain').focus(),0)}else{$('#customSource').classList.add('hidden');$('#devicePanel').classList.remove('hidden')}}else{device=value;renderResult()}}
$$('[data-source]').forEach(b=>b.onclick=()=>choose('source',b.dataset.source));
$$('[data-device]').forEach(b=>b.onclick=()=>choose('device',b.dataset.device));
function applyCustom(){try{customTarget=normalizeCustom($('#customDomain').value);$('#customError').textContent='';$('#devicePanel').classList.remove('hidden');$('#resultPanel').classList.add('hidden');$('#devicePanel').scrollIntoView({behavior:'smooth',block:'nearest'})}catch(err){customTarget=null;$('#devicePanel').classList.add('hidden');$('#resultPanel').classList.add('hidden');$('#customError').textContent=String(err.message||err)}}
$('#customUse').onclick=applyCustom;$('#customDomain').addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();applyCustom()}});
function route(t){if(t.custom)return `<div class="route"><b>${t.origin}</b><span class="arrow">→ Daten retten</span></div>`;return `<div class="route"><b>${t.name}</b><span class="arrow">→ Daten retten →</span><b>${t.otherName}</b><span>zum Weiterarbeiten</span></div>`}
function continueButtons(t){if(t.custom)return `<div class="actions two" style="margin-top:14px"><a class="btn secondary" href="https://bo2026.vercel.app/" target="_blank" rel="noopener">Vercel öffnen →</a><a class="btn secondary" href="https://dev-bo2026.onrender.com/" target="_blank" rel="noopener">Render öffnen →</a></div>`;return `<div class="actions" style="margin-top:14px"><a class="btn secondary" href="${t.other}" target="_blank" rel="noopener">${t.otherName} öffnen →</a></div>`}
function renderResult(){const t=target();if(!t||!device)return;let h=`<p class="step-label">3 · Rettung</p><h2>${t.custom?t.origin:t.name+'-Daten'} von ${device==='windows'?'Windows':device==='mac'?'macOS':'Android'} retten</h2>${route(t)}`;
  if(device==='windows')h+=`<div class="actions two"><a class="btn" href="${t.exe}">🪟 BO2026 Recovery starten</a><a class="btn secondary" href="${t.sha}" target="_blank" rel="noopener">SHA-256</a></div><div class="checklist"><div class="check"><b>1</b><span>Desktop-Browser vollständig schließen.</span></div><div class="check"><b>2</b><span>EXE starten. Für eine eigene Domain dort <strong>4</strong> wählen und die Domain eingeben. <strong>Enter = Vercel + Render</strong>.</span></div><div class="check"><b>3</b><span>Auf dem Desktop entsteht <code>Bewerbungsdossier-RECOVERED-*.json</code>.</span></div><div class="check"><b>4</b><span>Projektdatei anschließend auf einer funktionierenden BO2026-Seite laden.</span></div></div>${continueButtons(t)}<div class="notice">Die Windows-EXE kann Vercel, Render, beide oder eine frei eingegebene Domain auslesen. Die EXE ist noch nicht öffentlich code-signiert; Windows SmartScreen kann deshalb beim ersten Start warnen.</div>`;
  if(device==='mac')h+=`<div class="actions"><button class="btn" id="macDownload">🍎 Recovery-Skript laden</button></div><div class="checklist"><div class="check"><b>1</b><span>Browser vollständig schließen.</span></div><div class="check"><b>2</b><span>Einmalig den Install-Befehl im Terminal ausführen.</span></div></div><div class="cmd"><pre id="macInstall">python3 -m pip install "git+https://github.com/cclgroupltd/ccl_chromium_reader.git" python-snappy</pre><button class="copy" data-copy="#macInstall">⧉</button></div><div class="cmd"><pre id="macRun">python3 bo2026_recover.py</pre><button class="copy" data-copy="#macRun">⧉</button></div>${continueButtons(t)}`;
  if(device==='android')h+=`<div class="notice"><strong>Chrome NICHT schließen</strong>, wenn der BO2026-Tab noch offen ist.</div><div class="checklist"><div class="check"><b>1</b><span>Android per USB mit PC/Mac verbinden und USB-Debugging aktivieren.</span></div><div class="check"><b>2</b><span>Auf dem Desktop Chrome öffnen: <code>chrome://inspect/#devices</code></span></div><div class="check"><b>3</b><span>BO2026-Tab → Inspect → Application → Local Storage → <code>${t.origin}</code>.</span></div></div><details class="subtle"><summary>Tab ist weg / Root?</summary><div class="subtle-body">Ohne Root gibt es nach geschlossenem Tab keinen verlässlichen Direktzugriff auf Chromes App-Sandbox. Mit Root liegt Chrome typischerweise unter <code>/data/user/0/com.android.chrome/</code>. Chrome nicht deinstallieren und keine App-Daten löschen.</div></details>`;
  $('#result').innerHTML=h;$('#resultPanel').classList.remove('hidden');$('#resultPanel').scrollIntoView({behavior:'smooth',block:'nearest'});$('#macDownload')?.addEventListener('click',()=>downloadText('bo2026_recover.py',pyForTarget(t)));$$('[data-copy]').forEach(b=>b.onclick=()=>copyText($(b.dataset.copy).textContent,b));
}
$('#copyPython').onclick=e=>copyText(pyForTarget(target()),e.currentTarget);
'''
html = html[:start] + new_js + html[end:]
path.write_text(html, encoding='utf-8')
print('Custom domain UI patched')
