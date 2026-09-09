import os, re, sys

SP = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(SP, 'shell.html')
s = open(p, encoding='utf-8').read()
n, miss = 0, []


def rep(old, new, count=1):
    global s, n
    if old not in s:
        miss.append(old[:78].replace('\n', ' '))
        return
    s = s.replace(old, new, count)
    n += 1


ROUTER = r'''
/* ---------------- routing ----------------
   Real paths where the page owns its address bar (the Vercel deploy).
   Falls back to a hash route inside an artifact iframe or a file:// copy,
   where pushState either throws or would point at a URL nothing serves. */
const PATH_MODE = (location.protocol === "http:" || location.protocol === "https:")
  && window.top === window.self
  && !/\/artifact\//.test(location.pathname);
let muteHash = false;

function slugify(x){
  return String(x).normalize("NFD").replace(/[̀-ͯ]/g, "")
    .replace(/[đĐ]/g, "d")            // đ / Đ survive NFD, so map them by hand
    .toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
}
const famBySlug = m => FAMS.find(f => slugify(f.vi) === m);

function currentURL(){
  let path;
  if(view.name === "product")                     path = "/product/" + encodeURIComponent(view.code);
  else if(view.name === "catalogue" && filt.fam)  path = "/catalogue/" + slugify(filt.fam);
  else                                            path = "/" + view.name;
  const q = new URLSearchParams();
  if(lang === "en") q.set("lang", "en");
  if(view.name === "catalogue"){
    if(catUI.q)            q.set("q", catUI.q);
    if(filt.kind)          q.set("kind", filt.kind);
    if(filt.color)         q.set("color", filt.color);
    if(filt.dia)           q.set("dia", filt.dia);
    if(catUI.sort !== "code") q.set("sort", catUI.sort);
    if(catUI.mode !== "grid") q.set("view", catUI.mode);
  }
  const qs = q.toString();
  return path + (qs ? "?" + qs : "");
}

function writeURL(replace){
  const url = currentURL();
  try{
    if(PATH_MODE){
      history[replace ? "replaceState" : "pushState"](null, "", url);
    }else{
      muteHash = true;
      history[replace ? "replaceState" : "pushState"](null, "", "#" + url);
      setTimeout(()=>{ muteHash = false; }, 0);
    }
  }catch(e){ /* sandboxed host: stay on the current address */ }
}

function readURL(){
  const raw = PATH_MODE ? location.pathname + location.search
                        : (location.hash.slice(1) || "/home");
  const cut = raw.split("?");
  const q = new URLSearchParams(cut[1] || "");
  const l = q.get("lang");
  if(l === "en" || l === "vi") lang = l;

  const seg = cut[0].split("/").filter(Boolean);
  const head = seg[0] || "home";
  filt  = {fam:null, kind:null, color:null, dia:null};
  catUI = {q:"", sort:"code", mode:"grid"};
  pdSize = null; pdPhoto = 0;

  if(head === "product" && seg[1]){
    const code = decodeURIComponent(seg[1]);
    view = prod(code) ? {name:"product", code:code} : {name:"catalogue"};
  }else if(head === "catalogue"){
    view = {name:"catalogue"};
    if(seg[1]){ const f = famBySlug(seg[1]); if(f) filt.fam = f.vi; }
    catUI.q    = q.get("q") || "";
    filt.kind  = q.get("kind") || null;
    filt.color = q.get("color") || null;
    filt.dia   = q.get("dia") ? parseFloat(q.get("dia")) : null;
    catUI.sort = q.get("sort") || "code";
    catUI.mode = q.get("view") === "list" ? "list" : "grid";
  }else if(head === "capacity" || head === "careers" || head === "contact" || head === "home"){
    view = {name:head};
  }else{
    view = {name:"home"};
  }
}

function pageTitle(){
  const brand = "Asiana Gold";
  if(view.name === "product"){
    const pr = prod(view.code);
    return pr ? pr.ag + " " + t(pr.vi, pr.en || pr.vi) + " · " + brand : brand;
  }
  const names = {home:brand, catalogue:"Catalogue · " + brand,
    capacity:t("Năng lực sản xuất","Capabilities") + " · " + brand,
    careers:t("Tuyển dụng","Careers") + " · " + brand,
    contact:t("Liên hệ","Contact") + " · " + brand};
  return names[view.name] || brand;
}

window.addEventListener("popstate", ()=>{ readURL(); render(); });
window.addEventListener("hashchange", ()=>{ if(!muteHash){ readURL(); render(); } });

'''

rep('/* ---------- render ---------- */\nfunction render(){', ROUTER + '/* ---------- render ---------- */\nfunction render(){')

# title follows the route
rep('  document.documentElement.lang = lang;\n  $("#hdr-logo").innerHTML = logoSVG("",180);',
    '  document.documentElement.lang = lang;\n  document.title = pageTitle();\n  $("#hdr-logo").innerHTML = logoSVG("",180);')

# navigation writes a history entry
rep('''function go(name,extra){
  if(name!=="product" || (extra&&extra.code!==view.code)){ pdSize=null; pdPhoto=0; }
  view=Object.assign({name:name},extra||{}); render();
}''',
    '''function go(name,extra){
  if(name!=="product" || (extra&&extra.code!==view.code)){ pdSize=null; pdPhoto=0; }
  view=Object.assign({name:name},extra||{});
  render(); writeURL(false);
}
/* filter and language changes rewrite the address without stacking history */
function reflow(){ render(); writeURL(true); }''')

# filter / search / sort / view / language changes keep the URL in step
rep('''  if(e.target.closest("#lang-vi")){ lang="vi"; store.set("ag-lang","vi"); render(); refreshLayer(); return; }
  if(e.target.closest("#lang-en")){ lang="en"; store.set("ag-lang","en"); render(); refreshLayer(); return; }''',
    '''  if(e.target.closest("#lang-vi")){ lang="vi"; store.set("ag-lang","vi"); reflow(); refreshLayer(); return; }
  if(e.target.closest("#lang-en")){ lang="en"; store.set("ag-lang","en"); reflow(); refreshLayer(); return; }''')
rep('''    filt[k]=(String(filt[k])===String(v))?null:v; render(); return; }
  if(e.target.closest("#clear")){ filt={fam:null,kind:null,color:null,dia:null}; catUI.q=""; render(); return; }
  const vt=e.target.closest("[data-view]");
  if(vt){ catUI.mode=vt.dataset.view; render(); return; }''',
    '''    filt[k]=(String(filt[k])===String(v))?null:v; reflow(); return; }
  if(e.target.closest("#clear")){ filt={fam:null,kind:null,color:null,dia:null}; catUI.q=""; reflow(); return; }
  const vt=e.target.closest("[data-view]");
  if(vt){ catUI.mode=vt.dataset.view; reflow(); return; }''')
rep('''      catUI.q=q.value; const pos=q.selectionStart;
      render(); const nq=$("#q"); if(nq){ nq.focus(); try{nq.setSelectionRange(pos,pos);}catch(e){} }''',
    '''      catUI.q=q.value; const pos=q.selectionStart;
      reflow(); const nq=$("#q"); if(nq){ nq.focus(); try{nq.setSelectionRange(pos,pos);}catch(e){} }''')
rep('const s=$("#sort"); if(s) s.addEventListener("change",()=>{ catUI.sort=s.value; render(); });',
    'const s=$("#sort"); if(s) s.addEventListener("change",()=>{ catUI.sort=s.value; reflow(); });')
rep('  if(photo){ pdPhoto=+photo.dataset.photo; render(); return; }',
    '  if(photo){ pdPhoto=+photo.dataset.photo; render(); return; }  /* gallery: not a page change */')

# boot from whatever address the visitor arrived on
rep('''  const lg=store.get("ag-lang",null);
  if(lg==="vi"||lg==="en") lang=lg;
  render();''',
    '''  const lg=store.get("ag-lang",null);
  if(lg==="vi"||lg==="en") lang=lg;
  readURL();          // the address wins over the stored preference
  render();
  writeURL(true);     // normalise "/" to "/home"''')

open(p, 'w', encoding='utf-8').write(s)
sys.stderr.write('router: %d edits\n' % n)
for m in miss:
    sys.stderr.write('MISS: ' + m + '\n')
