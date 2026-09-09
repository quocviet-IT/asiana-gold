import os, re, sys

SP = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(SP, 'shell.html')
s = open(p, encoding='utf-8').read()
n, miss = 0, []


def rep(old, new, count=1):
    global s, n
    if old not in s:
        miss.append(old[:88].replace('\n', ' '))
        return
    s = s.replace(old, new, count)
    n += 1


# ======================================================================
# 1. CSS — dark photographic hero, counters, positioning block
# ======================================================================
CSS = '''
/* ---------- hero: photographic, on espresso ---------- */
.hero{position:relative;background:#151007;overflow:hidden;isolation:isolate}
.hero::before{content:"";position:absolute;inset:0;z-index:0;
  background:radial-gradient(58% 62% at 66% 42%, rgba(214,178,92,.26), transparent 68%),
             radial-gradient(80% 70% at 12% 10%, rgba(120,92,34,.20), transparent 70%)}
.hero::after{content:"";position:absolute;inset:0;z-index:0;pointer-events:none;
  background:linear-gradient(180deg,rgba(0,0,0,.28),transparent 26%,transparent 72%,rgba(0,0,0,.42))}
.hero > *{position:relative;z-index:1}
.slide-grid{display:grid;grid-template-columns:1.04fr .96fr;gap:clamp(24px,4vw,64px);align-items:center;
  padding-block:clamp(56px,7vw,104px) clamp(96px,10vw,140px)}
@media(max-width:900px){.slide-grid{grid-template-columns:1fr;padding-bottom:120px}}
.hero-copy h1{margin:18px 0 18px;color:#F6EEDC}
.hero-copy .lede{color:#C8B694;max-width:50ch;font-style:italic}
.hero .eyebrow{color:var(--g300)}
.hero .eyebrow::before{background:var(--g400)}
.hero .cta{display:flex;gap:12px;margin-top:30px;flex-wrap:wrap}
.hero .btn-line{border-color:rgba(246,238,220,.34);color:#F6EEDC;background:transparent}
.hero .btn-line:hover{background:rgba(246,238,220,.09)}
.hero-art{position:relative;display:grid;place-items:center;min-height:300px}
.hero-art::before{content:"";position:absolute;width:82%;aspect-ratio:1/1;border-radius:50%;
  background:radial-gradient(circle, rgba(232,205,140,.20), transparent 66%)}
.hero-cut{position:relative;width:100%;max-width:520px;filter:drop-shadow(0 26px 44px rgba(0,0,0,.6))}
.hero-tag{position:absolute;left:0;bottom:-6px;display:flex;align-items:baseline;gap:10px}
.hero-tag b{font-family:"IBM Plex Mono",monospace;font-size:.92rem;letter-spacing:.06em;color:var(--g300)}
.hero-tag span{font-size:.86rem;color:#9B8B6B;font-style:italic}
.hero-nav{position:absolute;left:0;right:0;bottom:44px;z-index:2;pointer-events:none}
.hero-nav .wrap{display:flex;align-items:center;gap:12px}
.dots button{width:30px;height:3px;border-radius:99px;background:rgba(246,238,220,.28);transition:background .2s,width .2s}
.dots button[aria-current="true"]{background:var(--g300);width:54px}
.arrows button{width:40px;height:40px;border-radius:99px;border:1px solid rgba(246,238,220,.26);
  display:grid;place-items:center;color:#F6EEDC;background:transparent;transition:all .18s}
.arrows button:hover{background:var(--g400);color:#241B0A;border-color:transparent}

/* ---------- by the numbers, floated over the hero edge ---------- */
.numbers{position:relative;margin-top:-64px;z-index:5}
.numbers .card-in{background:var(--card);border:1px solid var(--rule);border-radius:16px;
  box-shadow:var(--shadow-l);padding:clamp(28px,3.6vw,46px)}
.numbers .head{text-align:center;margin-bottom:30px}
.numbers .head h2{margin-top:10px}
.numbers .head p{color:var(--ink-2);max-width:60ch;margin:10px auto 0}
.ngrid{display:grid;grid-template-columns:repeat(6,1fr);gap:2px;background:var(--rule-2)}
@media(max-width:1000px){.ngrid{grid-template-columns:repeat(3,1fr)}}
@media(max-width:600px){.ngrid{grid-template-columns:repeat(2,1fr)}}
.ncell{background:var(--card);padding:22px 14px;text-align:center}
.ncell b{display:block;font-family:"Cormorant Garamond",Georgia,serif;font-weight:600;
  font-size:clamp(2rem,3.4vw,2.9rem);line-height:1;color:var(--g600);font-variant-numeric:tabular-nums}
.ncell i{font-style:normal;font-size:.7em;color:var(--g500)}
.ncell span{display:block;margin-top:8px;font-family:"Cormorant Garamond",Georgia,serif;
  font-size:.82rem;letter-spacing:.13em;text-transform:uppercase;font-weight:600;color:var(--ink-2)}
.pending{margin-top:24px;padding-top:20px;border-top:1px solid var(--rule-2);
  display:flex;gap:26px;flex-wrap:wrap;align-items:center;justify-content:center}
.pending > span{font-size:.88rem;color:var(--ink-3);font-style:italic}
.pending ul{list-style:none;display:flex;gap:8px;flex-wrap:wrap;margin:0;padding:0}
.pending li{font-family:"Cormorant Garamond",Georgia,serif;font-size:.82rem;letter-spacing:.1em;
  text-transform:uppercase;font-weight:600;color:#B4552F;border:1px dashed #B4552F;
  padding:3px 10px;border-radius:99px}

/* ---------- who we work for ---------- */
.who{display:grid;grid-template-columns:1fr 1fr;gap:clamp(26px,4vw,58px);align-items:start}
@media(max-width:880px){.who{grid-template-columns:1fr}}
.pillars{display:flex;flex-direction:column;gap:0;border-top:1px solid var(--rule)}
.pillar{padding:20px 0;border-bottom:1px solid var(--rule-2);display:grid;grid-template-columns:34px 1fr;gap:16px}
.pillar .pi{color:var(--g500);padding-top:2px}
.pillar h3{margin-bottom:5px}
.pillar p{font-size:.94rem;color:var(--ink-2)}
.clients{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}
.clients span{font-family:"Cormorant Garamond",Georgia,serif;font-size:.86rem;letter-spacing:.13em;
  text-transform:uppercase;font-weight:600;color:var(--g700);border:1px solid var(--rule);
  border-radius:99px;padding:6px 15px;background:var(--g50)}

/* ---------- purity cards ---------- */
.alloys{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
@media(max-width:900px){.alloys{grid-template-columns:repeat(2,1fr)}}
@media(max-width:480px){.alloys{grid-template-columns:1fr}}
.alloy{background:var(--card);border:1px solid var(--rule);border-radius:13px;padding:22px 20px;
  display:flex;flex-direction:column;gap:6px;transition:border-color .18s,transform .18s}
.alloy:hover{border-color:var(--g400);transform:translateY(-2px)}
.alloy .k{font-family:"Cormorant Garamond",Georgia,serif;font-size:2.4rem;font-weight:600;line-height:1;
  background:var(--metal);-webkit-background-clip:text;background-clip:text;color:transparent}
.alloy .au{font-family:"IBM Plex Mono",monospace;font-size:.84rem;color:var(--ink-2)}
.alloy .kt{font-family:"Cormorant Garamond",Georgia,serif;font-size:.86rem;letter-spacing:.13em;
  text-transform:uppercase;font-weight:600;color:var(--g600)}
.alloy .note{margin-top:auto;padding-top:12px;font-size:.86rem;color:var(--ink-3);font-style:italic}
'''
rep('.hidden{display:none!important}\n</style>', CSS + '\n.hidden{display:none!important}\n</style>')

# ======================================================================
# 2. purity is 750 / 680 / 610 / 416 everywhere
# ======================================================================
rep('const PAGES=[["home","Trang chủ","Home"],["catalogue","Catalogue","Catalogue"],',
    '''const PURITIES=[
  {k:"750", au:"75,0", auEn:"75.0", kt:"18K",      ktEn:"18K",      spec:true},
  {k:"680", au:"68,0", auEn:"68.0", kt:"≈ 16,3K",  ktEn:"≈ 16.3K",  spec:false},
  {k:"610", au:"61,0", auEn:"61.0", kt:"≈ 14,6K",  ktEn:"≈ 14.6K",  spec:true},
  {k:"416", au:"41,6", auEn:"41.6", kt:"10K",      ktEn:"10K",      spec:false}
];
const PURITY_LINE = PURITIES.map(x=>x.k).join(" · ");
const PAGES=[["home","Trang chủ","Home"],["catalogue","Catalogue","Catalogue"],''')

rep('    [t("Tuổi vàng","Purity"), "750 · 610"],', '    [t("Tuổi vàng","Purity"), PURITY_LINE],')
rep('<dt>${t("Tuổi vàng","Purity")}</dt><dd class="mono">750 · 610</dd>',
    '<dt>${t("Tuổi vàng","Purity")}</dt><dd class="mono">${PURITY_LINE}</dd>')
rep('''          <option>750 (18K)</option><option>610</option><option>${t("Cả hai","Both")}</option></select></div>''',
    '''          ${PURITIES.map(x=>`<option>${x.k}${x.k==="750"?" (18K)":""}</option>`).join("")}
          <option>${t("Nhiều tuổi vàng","Several")}</option></select></div>''')
rep('      <div><b>2</b><span>${t("tuổi vàng 750 · 610","purities 750 · 610")}</span></div>',
    '      <div><b>4</b><span>${t("tuổi vàng "+PURITY_LINE,"purities "+PURITY_LINE)}</span></div>')
rep('''    "Đúc và đan tại xưởng Asiana Gold, làm được ở vàng 750 và 610, màu "+cols+".",
    "Drawn and woven at the Asiana Gold factory in 750 and 610 gold, "+cols+"."));''',
    '''    "Đúc và đan tại xưởng Asiana Gold, làm được ở tuổi vàng "+PURITY_LINE+", màu "+cols+".",
    "Drawn and woven at the Asiana Gold factory in "+PURITY_LINE+" gold, "+cols+"."));''')

open(p, 'w', encoding='utf-8').write(s)
sys.stderr.write('stage 1: %d edits\n' % n)
for m in miss:
    sys.stderr.write('MISS: ' + m + '\n')
