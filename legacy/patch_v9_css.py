import os, re, sys

SP = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(SP, 'shell.html')
s = open(p, encoding='utf-8').read()
n, miss = 0, []


def rep(old, new, count=1):
    global s, n
    if old not in s:
        miss.append(old[:80].replace('\n', ' '))
        return
    s = s.replace(old, new, count)
    n += 1


# ---- palette: gold becomes ink, not a surface -------------------------------
rep('  --paper:#FFFFFF; --tint:#FDF9EF; --plate:#FFFFFF; --card:#FFFFFF;',
    '  --paper:#FFFFFF; --tint:#F4F1E8; --plate:#FFFFFF; --card:#FFFFFF;')
rep('  --rule:#E8DCC0; --rule-2:#F2E9D4;',
    '  --rule:#D8CFBB; --rule-2:#EAE3D2;')

# ---- labels: no dash, no all-caps tracking ---------------------------------
rep('''.eyebrow{display:inline-flex;align-items:center;gap:9px;font-family:"Cormorant Garamond",Georgia,serif;
  font-size:.82rem;letter-spacing:.2em;text-transform:uppercase;color:var(--g600);font-weight:600}
.eyebrow::before{content:"";width:22px;height:1px;background:var(--g400)}
.eyebrow.on-dark{color:var(--g300)}
.eyebrow.on-dark::before{background:var(--g400)}''',
    '''.eyebrow{display:block;font-family:"EB Garamond",Georgia,serif;font-size:1rem;
  font-style:italic;color:var(--g700);margin-bottom:2px}
.eyebrow.on-dark{color:var(--g300)}''')

# ---- buttons: flat, square, no lift, no shimmer ------------------------------
rep('''.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;padding:13px 24px;
  border-radius:8px;font-family:"Cormorant Garamond",Georgia,serif;font-weight:600;font-size:.95rem;
  letter-spacing:.13em;text-transform:uppercase;border:1px solid transparent;
  transition:transform .14s,box-shadow .18s,background .18s;white-space:nowrap}
.btn:hover{transform:translateY(-1px)}
.btn-gold{background:var(--metal);background-size:200% 100%;color:#2A1F09;font-weight:600;
  box-shadow:0 4px 14px -6px rgba(160,120,30,.65)}
.btn-gold:hover{animation:shimmer 1.6s linear infinite;box-shadow:0 8px 22px -8px rgba(160,120,30,.85)}''',
    '''.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;padding:13px 26px;
  border-radius:2px;font-family:"EB Garamond",Georgia,serif;font-weight:600;font-size:1.02rem;
  border:1px solid transparent;transition:background .18s,color .18s,border-color .18s;white-space:nowrap}
.btn-gold{background:var(--g700);color:#FDFBF5}
.btn-gold:hover{background:var(--g800,#63490F)}''')
rep('.btn-dark{background:var(--espresso);color:var(--onDark)}',
    '.btn-dark{background:var(--espresso);color:var(--onDark);border-radius:2px}')
rep('.btn-line{border-color:var(--g400);color:var(--g700);background:transparent}\n.btn-line:hover{background:var(--g50)}',
    '.btn-line{border-color:var(--rule);color:var(--ink);background:transparent}\n.btn-line:hover{border-color:var(--g600);color:var(--g700)}')
rep('.btn-sm{padding:9px 16px;font-size:.85rem}', '.btn-sm{padding:9px 18px;font-size:.94rem}')

# ---- product grids: photograph and caption, no card -------------------------
rep('''.cat-tile{position:relative;background:var(--card);border:1px solid var(--rule);border-radius:13px;
  overflow:hidden;text-align:left;display:flex;flex-direction:column;
  transition:transform .18s,box-shadow .2s,border-color .2s}
.cat-tile:hover{transform:translateY(-3px);box-shadow:var(--shadow-m);border-color:var(--g400)}
.cat-tile .pic{background:var(--plate);aspect-ratio:4/3;display:grid;place-items:center;padding:18px;
  border-bottom:1px solid var(--rule-2);overflow:hidden}''',
    '''.cat-tile{position:relative;background:transparent;border:0;text-align:left;
  display:flex;flex-direction:column;padding:0}
.cat-tile .pic{background:var(--plate);aspect-ratio:4/3;display:grid;place-items:center;padding:14px;
  border:1px solid var(--rule-2);overflow:hidden}
.cat-tile:hover .pic{border-color:var(--g500)}''')
rep('.cat-tile .body{padding:15px 17px 17px;display:flex;flex-direction:column;gap:3px;flex:1}',
    '.cat-tile .body{padding:13px 0 0;display:flex;flex-direction:column;gap:2px;flex:1}')
rep('''.cat-tile .body u{text-decoration:none;margin-top:auto;padding-top:11px;display:flex;align-items:center;gap:6px;
  font-family:"Cormorant Garamond",Georgia,serif;font-size:.85rem;font-weight:600;color:var(--g600);
  letter-spacing:.14em;text-transform:uppercase}''',
    '''.cat-tile .body u{text-decoration:none;margin-top:auto;padding-top:7px;
  font-family:"EB Garamond",Georgia,serif;font-size:.94rem;font-style:italic;color:var(--g700)}
.cat-tile:hover .body u{text-decoration:underline;text-underline-offset:3px}''')
rep('''.ribbon{position:absolute;top:11px;left:11px;background:var(--espresso);color:var(--g300);
  font-family:"IBM Plex Mono",monospace;font-size:.66rem;padding:3px 8px;border-radius:5px;letter-spacing:.06em}''',
    '.ribbon{display:none}')

rep('''.card{background:var(--card);border:1px solid var(--rule);border-radius:12px;overflow:hidden;
  text-align:left;display:flex;flex-direction:column;position:relative;
  transition:transform .16s,box-shadow .2s,border-color .2s}
.card:hover{transform:translateY(-3px);border-color:var(--g400);box-shadow:var(--shadow-m)}
.card .pic{background:var(--plate);aspect-ratio:1/1;display:grid;place-items:center;padding:18px;
  border-bottom:1px solid var(--rule-2);position:relative;overflow:hidden}''',
    '''.card{background:transparent;border:0;text-align:left;display:flex;flex-direction:column;position:relative}
.card .pic{background:var(--plate);aspect-ratio:1/1;display:grid;place-items:center;padding:16px;
  border:1px solid var(--rule-2);position:relative;overflow:hidden}
.card:hover .pic{border-color:var(--g500)}''')
rep('.card .m{padding:12px 14px 14px;display:flex;flex-direction:column;gap:3px;flex:1}',
    '.card .m{padding:11px 0 0;display:flex;flex-direction:column;gap:2px;flex:1}')
rep('.card .m .foot{display:flex;gap:5px;margin-top:auto;padding-top:10px;align-items:center}',
    '.card .m .foot{display:flex;gap:5px;margin-top:auto;padding-top:8px;align-items:center}')
rep('''.quick{position:absolute;left:50%;bottom:10px;transform:translate(-50%,10px);opacity:0;
  background:var(--espresso);color:var(--g200);font-size:.76rem;font-weight:600;padding:7px 14px;
  border-radius:99px;transition:all .2s;white-space:nowrap;pointer-events:auto}
.card:hover .quick{opacity:1;transform:translate(-50%,0)}''',
    '''.quick{position:absolute;left:0;right:0;bottom:0;opacity:0;background:rgba(23,18,8,.88);
  color:#F4EEDF;font-size:.94rem;padding:9px 0;text-align:center;transition:opacity .18s;
  white-space:nowrap;pointer-events:auto;font-style:italic}
.card:hover .quick{opacity:1}''')
rep('.card .pic img{width:100%;height:100%;object-fit:contain;transition:transform .35s}\n.card:hover .pic img{transform:scale(1.07)}',
    '.card .pic img{width:100%;height:100%;object-fit:contain}')
rep('.cat-tile .pic img{width:100%;height:100%;object-fit:contain;transition:transform .35s}\n.cat-tile:hover .pic img{transform:scale(1.06)}',
    '.cat-tile .pic img{width:100%;height:100%;object-fit:contain}')

# ---- lists, tables, notes: rules instead of boxes ---------------------------
rep('''.row{display:grid;grid-template-columns:64px 1fr auto auto;gap:16px;align-items:center;
  background:var(--card);border:1px solid var(--rule);border-radius:11px;padding:10px 14px;text-align:left;
  transition:border-color .16s,box-shadow .18s}
.row:hover{border-color:var(--g400);box-shadow:var(--shadow-s)}''',
    '''.row{display:grid;grid-template-columns:64px 1fr auto auto;gap:18px;align-items:center;
  background:transparent;border:0;border-bottom:1px solid var(--rule-2);padding:12px 2px;text-align:left}
.row:hover{background:var(--tint)}''')
rep('.row .pic{width:64px;height:64px;background:var(--plate);border:1px solid var(--rule-2);border-radius:8px;\n  display:grid;place-items:center;padding:5px}',
    '.row .pic{width:64px;height:64px;background:var(--plate);border:1px solid var(--rule-2);\n  display:grid;place-items:center;padding:5px}')
rep('.list{display:flex;flex-direction:column;gap:9px}',
    '.list{display:flex;flex-direction:column;border-top:1px solid var(--rule)}')

rep('.tablewrap{overflow-x:auto;border:1px solid var(--rule);border-radius:12px;background:var(--card)}',
    '.tablewrap{overflow-x:auto;border-top:1.5px solid var(--ink);border-bottom:1px solid var(--rule);background:transparent}')
rep('''thead th{font-family:"Cormorant Garamond",Georgia,serif;font-size:.84rem;letter-spacing:.13em;text-transform:uppercase;
  color:var(--g700);font-weight:600;background:var(--g50)}''',
    '''thead th{font-family:"EB Garamond",Georgia,serif;font-size:.95rem;font-style:italic;
  color:var(--ink-2);font-weight:500;background:transparent;border-bottom:1px solid var(--rule)}''')
rep('tbody tr:hover{background:var(--g50)}', 'tbody tr:hover{background:var(--tint)}')
rep('.grp td{background:var(--g100);font-weight:700;color:var(--ink)}',
    '.grp td{background:transparent;font-weight:600;color:var(--ink);padding-top:22px;\n  border-bottom:1px solid var(--ink)}')

rep('''.note{border-left:3px solid var(--g400);background:var(--g50);border-radius:0 9px 9px 0;
  padding:14px 17px;font-size:.87rem;color:var(--ink-2)}''',
    '''.note{border-top:1px solid var(--rule);background:transparent;border-radius:0;
  padding:13px 0 0;font-size:.98rem;color:var(--ink-2);max-width:60ch}''')
rep('.band-dark .note{background:rgba(255,255,255,.05);color:var(--onDark-2)}',
    '.band-dark .note{background:transparent;border-top-color:rgba(255,255,255,.18);color:var(--onDark-2)}')

# ---- feature / alloy / step / job blocks lose their boxes -------------------
rep('''.feat{background:var(--card);border:1px solid var(--rule);border-radius:13px;padding:24px 21px;
  display:flex;flex-direction:column;gap:11px;transition:border-color .18s,transform .18s}
.feat:hover{border-color:var(--g400);transform:translateY(-2px)}
.band-dark .feat{background:rgba(255,255,255,.045);border-color:rgba(255,255,255,.12)}
.feat .ic{width:44px;height:44px;border-radius:10px;background:var(--metal);display:grid;place-items:center;color:#2A1F09}''',
    '''.feat{background:transparent;border:0;border-top:1px solid var(--rule);padding:18px 0 0;
  display:flex;flex-direction:column;gap:8px}
.band-dark .feat{border-top-color:rgba(255,255,255,.18)}
.feat .ic{color:var(--g600);margin-bottom:2px}''')

rep('''.alloy{background:var(--card);border:1px solid var(--rule);border-radius:13px;padding:22px 20px;
  display:flex;flex-direction:column;gap:6px;transition:border-color .18s,transform .18s}
.alloy:hover{border-color:var(--g400);transform:translateY(-2px)}
.alloy .k{font-family:"Cormorant Garamond",Georgia,serif;font-size:2.4rem;font-weight:600;line-height:1;
  background:var(--metal);-webkit-background-clip:text;background-clip:text;color:transparent}''',
    '''.alloy{background:transparent;border:0;border-top:1.5px solid var(--ink);padding:16px 0 0;
  display:flex;flex-direction:column;gap:5px}
.alloy .k{font-family:"Cormorant Garamond",Georgia,serif;font-size:2.6rem;font-weight:500;
  line-height:1;color:var(--g700)}''')
rep('.alloy .kt{font-family:"Cormorant Garamond",Georgia,serif;font-size:.86rem;letter-spacing:.13em;\n  text-transform:uppercase;font-weight:600;color:var(--g600)}',
    '.alloy .kt{font-family:"EB Garamond",Georgia,serif;font-size:1rem;color:var(--ink);font-weight:600}')

rep('''.step{background:var(--card);border:1px solid var(--rule);border-radius:13px;padding:22px 19px;transition:border-color .18s}
.step:hover{border-color:var(--g400)}
.step .n{font-family:"Cormorant Garamond",Georgia,serif;font-weight:600;font-size:3rem;line-height:1;
  background:var(--metal);-webkit-background-clip:text;background-clip:text;color:transparent;display:block;margin-bottom:10px}''',
    '''.step{background:transparent;border:0;border-top:1px solid var(--rule);padding:16px 0 0}
.step .n{font-family:"IBM Plex Mono",monospace;font-weight:500;font-size:.86rem;line-height:1;
  color:var(--g700);display:block;margin-bottom:12px}''')

rep('''.job{display:grid;grid-template-columns:1fr auto;gap:16px;align-items:center;background:var(--card);
  border:1px solid var(--rule);border-radius:12px;padding:18px 20px}
.job:hover{border-color:var(--g400)}''',
    '''.job{display:grid;grid-template-columns:1fr auto;gap:16px;align-items:center;background:transparent;
  border:0;border-bottom:1px solid var(--rule-2);padding:18px 2px}''')
rep('.jobs{display:flex;flex-direction:column;gap:12px}',
    '.jobs{display:flex;flex-direction:column;border-top:1.5px solid var(--ink)}')

rep('.basket{background:var(--card);border:1px solid var(--rule);border-radius:13px;padding:19px 21px}',
    '.basket{background:transparent;border:0;border-top:1.5px solid var(--ink);padding:18px 0 0}')
rep('''.form{display:grid;grid-template-columns:1fr 1fr;gap:15px;background:var(--card);
  border:1px solid var(--rule);border-radius:13px;padding:24px}''',
    '.form{display:grid;grid-template-columns:1fr 1fr;gap:17px;background:transparent;border:0;padding:0}')
rep('''.finder{background:var(--card);border:1px solid var(--rule);border-radius:14px;padding:24px;box-shadow:var(--shadow-s)}''',
    '.finder{background:transparent;border:0;border-top:1.5px solid var(--ink);padding:22px 0 0}')
rep('.finder-out{border:1px solid var(--rule);border-radius:11px;overflow:hidden}',
    '.finder-out{border:0}')
rep('.finder-sum{display:flex;flex-wrap:wrap;gap:22px;padding:14px 18px;background:var(--g50);border-bottom:1px solid var(--rule)}',
    '.finder-sum{display:flex;flex-wrap:wrap;gap:34px;padding:0 0 18px;background:transparent;border-bottom:1px solid var(--rule)}')
rep('''.gauge{display:flex;align-items:flex-end;gap:clamp(16px,3.4vw,38px);flex-wrap:wrap;background:var(--card);
  border:1px solid var(--rule);border-radius:13px;padding:30px 26px 20px}''',
    '''.gauge{display:flex;align-items:flex-end;gap:clamp(16px,3.4vw,38px);flex-wrap:wrap;background:transparent;
  border:0;border-top:1px solid var(--rule);padding:28px 0 0}''')
rep('''.filters{position:sticky;top:96px;display:flex;flex-direction:column;gap:20px;background:var(--card);
  border:1px solid var(--rule);border-radius:13px;padding:19px}''',
    '''.filters{position:sticky;top:96px;display:flex;flex-direction:column;gap:22px;background:transparent;
  border:0;border-top:1.5px solid var(--ink);padding:18px 0 0}''')
rep('.qa{background:var(--card);border:1px solid var(--rule);border-radius:11px;overflow:hidden;transition:border-color .18s}\n.qa[open]{border-color:var(--g400)}',
    '.qa{background:transparent;border:0;border-bottom:1px solid var(--rule-2);border-radius:0}')
rep('.qa summary{padding:16px 20px;cursor:pointer;font-family:"Cormorant Garamond",Georgia,serif;\n  font-weight:600;font-size:1.2rem;display:flex;align-items:center;gap:14px;list-style:none}',
    '.qa summary{padding:16px 2px;cursor:pointer;font-family:"Cormorant Garamond",Georgia,serif;\n  font-weight:600;font-size:1.28rem;display:flex;align-items:center;gap:14px;list-style:none}')
rep('.qa summary:hover{background:var(--g50)}', '.qa summary:hover{color:var(--g700)}')
rep('.qa .a{padding:0 20px 18px;font-size:.9rem;color:var(--ink-2);max-width:78ch}',
    '.qa .a{padding:0 2px 20px;font-size:1rem;color:var(--ink-2);max-width:70ch}')
rep('.faq{display:flex;flex-direction:column;gap:10px}',
    '.faq{display:flex;flex-direction:column;border-top:1.5px solid var(--ink)}')

# ---- selection controls: solid, not gradient --------------------------------
rep('.chip[aria-pressed="true"]{background:var(--metal);border-color:transparent;color:#2A1F09;font-weight:700}',
    '.chip[aria-pressed="true"]{background:var(--ink);border-color:var(--ink);color:#FDFBF5;font-weight:600}')
rep('.chip{border:1px solid var(--rule);border-radius:99px;padding:5px 12px;font-size:.79rem;color:var(--ink-2);\n  background:var(--paper);transition:all .15s}',
    '.chip{border:1px solid var(--rule);border-radius:2px;padding:5px 12px;font-size:.92rem;color:var(--ink-2);\n  background:transparent;transition:all .15s}')
rep('.seg-ctrl button[aria-pressed="true"]{background:var(--metal);color:#2A1F09}',
    '.seg-ctrl button[aria-pressed="true"]{background:var(--ink);color:#FDFBF5}')
rep('.seg-ctrl{display:flex;border:1px solid var(--rule);border-radius:9px;overflow:hidden}',
    '.seg-ctrl{display:flex;border:1px solid var(--rule);border-radius:2px;overflow:hidden}')
rep('.viewtog button[aria-pressed="true"]{background:var(--metal);color:#2A1F09}',
    '.viewtog button[aria-pressed="true"]{background:var(--ink);color:#FDFBF5}')
rep('.sizepick button[aria-pressed="true"]{background:var(--metal);border-color:transparent;color:#2A1F09}',
    '.sizepick button[aria-pressed="true"]{background:var(--ink);border-color:var(--ink);color:#FDFBF5}')
rep('.sizepick button{border:1px solid var(--rule);border-radius:8px;padding:8px 13px;',
    '.sizepick button{border:1px solid var(--rule);border-radius:2px;padding:8px 13px;')
rep('.f-tel{background:var(--metal);color:#2A1F09}', '.f-tel{background:var(--g700);color:#FDFBF5}')
rep('.cta-band{background:var(--metal);border-radius:16px;padding:clamp(30px,4.4vw,52px);color:#2A1F09}\n.cta-band h2{color:#241A0B}\n.cta-band p{color:#4A3922;max-width:50ch;margin-top:11px}',
    '.cta-band{background:transparent;border-top:1.5px solid var(--ink);border-radius:0;\n  padding:clamp(28px,4vw,44px) 0 0;color:var(--ink)}\n.cta-band h2{color:var(--ink)}\n.cta-band p{color:var(--ink-2);max-width:52ch;margin-top:11px}')

# ---- numbers block: keep the float, drop the card look ----------------------
rep('''.numbers .card-in{background:var(--card);border:1px solid var(--rule);border-radius:16px;
  box-shadow:var(--shadow-l);padding:clamp(28px,3.6vw,46px)}''',
    '''.numbers .card-in{background:var(--paper);border:0;border-radius:0;
  box-shadow:0 -1px 0 var(--rule);padding:clamp(30px,3.8vw,52px) clamp(24px,3vw,44px)}''')
rep('.ncell b{display:block;font-family:"Cormorant Garamond",Georgia,serif;font-weight:600;\n  font-size:clamp(2rem,3.4vw,2.9rem);line-height:1;color:var(--g600);font-variant-numeric:tabular-nums}',
    '.ncell b{display:block;font-family:"Cormorant Garamond",Georgia,serif;font-weight:500;\n  font-size:clamp(2.2rem,3.6vw,3.1rem);line-height:1;color:var(--ink);font-variant-numeric:tabular-nums}')
rep('.ncell span{display:block;margin-top:8px;font-family:"Cormorant Garamond",Georgia,serif;\n  font-size:.82rem;letter-spacing:.13em;text-transform:uppercase;font-weight:600;color:var(--ink-2)}',
    '.ncell span{display:block;margin-top:7px;font-family:"EB Garamond",Georgia,serif;\n  font-size:.98rem;color:var(--ink-2)}')
rep('.pending li{font-family:"Cormorant Garamond",Georgia,serif;font-size:.82rem;letter-spacing:.1em;\n  text-transform:uppercase;font-weight:600;color:#B4552F;border:1px dashed #B4552F;\n  padding:3px 10px;border-radius:99px}',
    '.pending li{font-family:"EB Garamond",Georgia,serif;font-size:.96rem;color:#9A4A28;\n  border-bottom:1px dashed #C08268;padding:0 0 1px}')
rep('.clients span{font-family:"Cormorant Garamond",Georgia,serif;font-size:.86rem;letter-spacing:.13em;\n  text-transform:uppercase;font-weight:600;color:var(--g700);border:1px solid var(--rule);\n  border-radius:99px;padding:6px 15px;background:var(--g50)}',
    '.clients span{font-family:"EB Garamond",Georgia,serif;font-size:1rem;color:var(--ink);\n  border:0;border-bottom:1px solid var(--g400);padding:0 0 2px}')
rep('.clients{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}',
    '.clients{display:flex;flex-wrap:wrap;gap:6px 22px;margin-top:22px}')

# ---- kill the scroll-entrance choreography ---------------------------------
rep('.stagger > *{animation:rise .55s cubic-bezier(.2,.7,.3,1) backwards}',
    '.stagger > *{animation:none}')

# ---- misc chrome ------------------------------------------------------------
rep('.kv dt{color:var(--g700);font-family:"Cormorant Garamond",Georgia,serif;font-size:.86rem;letter-spacing:.13em;\n  text-transform:uppercase;padding-top:2px;font-weight:600}',
    '.kv dt{color:var(--ink-2);font-family:"EB Garamond",Georgia,serif;font-size:1rem;\n  font-style:italic;padding-top:1px;font-weight:400}')
rep('.field label{font-family:"Cormorant Garamond",Georgia,serif;font-size:.85rem;letter-spacing:.14em;\n  text-transform:uppercase;color:var(--g700);font-weight:600}',
    '.field label{font-family:"EB Garamond",Georgia,serif;font-size:1rem;font-style:italic;\n  color:var(--ink-2);font-weight:400}')
rep('.fgroup > p{font-family:"Cormorant Garamond",Georgia,serif;font-size:.84rem;letter-spacing:.15em;text-transform:uppercase;\n  color:var(--g700);margin-bottom:9px;font-weight:600}',
    '.fgroup > p{font-family:"EB Garamond",Georgia,serif;font-size:1rem;font-style:italic;\n  color:var(--ink-2);margin-bottom:9px;font-weight:400}')
rep('.fc > span{font-family:"Cormorant Garamond",Georgia,serif;font-size:.84rem;letter-spacing:.15em;\n  text-transform:uppercase;color:var(--g700);font-weight:600}',
    '.fc > span{font-family:"EB Garamond",Georgia,serif;font-size:1rem;font-style:italic;\n  color:var(--ink-2);font-weight:400}')
rep('.finder-sum div span{display:block;font-family:"Cormorant Garamond",Georgia,serif;font-size:.82rem;font-weight:600;\n  letter-spacing:.14em;text-transform:uppercase;color:var(--g700)}',
    '.finder-sum div span{display:block;font-family:"EB Garamond",Georgia,serif;font-size:.98rem;\n  font-style:italic;color:var(--ink-2)}')
rep('footer h4{font-family:"Cormorant Garamond",Georgia,serif;font-size:.86rem;letter-spacing:.18em;text-transform:uppercase;\n  color:var(--g300);margin-bottom:14px;font-weight:600}',
    'footer h4{font-family:"EB Garamond",Georgia,serif;font-size:1.02rem;font-style:italic;\n  color:var(--g300);margin-bottom:14px;font-weight:400}')
rep('''nav.main > button,.navitem > button{padding:9px 13px;border-radius:7px;
  font-family:"Cormorant Garamond",Georgia,serif;font-size:.92rem;font-weight:600;
  letter-spacing:.13em;text-transform:uppercase;
  color:var(--ink-2);white-space:nowrap;transition:background .16s,color .16s;display:inline-flex;align-items:center;gap:6px}''',
    '''nav.main > button,.navitem > button{padding:9px 12px;border-radius:0;
  font-family:"EB Garamond",Georgia,serif;font-size:1.06rem;font-weight:500;
  color:var(--ink-2);white-space:nowrap;transition:color .16s;display:inline-flex;align-items:center;gap:6px}''')
rep('nav.main > button:hover,.navitem > button:hover{background:var(--g50);color:var(--g700)}',
    'nav.main > button:hover,.navitem > button:hover{color:var(--g700)}')
rep('nav.main > button[aria-current="page"]{color:var(--g700);background:var(--g50);font-weight:700}',
    'nav.main > button[aria-current="page"]{color:var(--ink);background:transparent;font-weight:600;\n  box-shadow:inset 0 -1px 0 var(--g600)}')
rep('''.util{background:var(--espresso-2);color:var(--onDark-2);font-family:"Cormorant Garamond",Georgia,serif;
  font-size:.88rem;letter-spacing:.09em;text-transform:uppercase;font-weight:600}''',
    '''.util{background:var(--espresso-2);color:var(--onDark-2);font-family:"EB Garamond",Georgia,serif;
  font-size:.96rem;font-weight:400}''')
rep('.back-link{display:inline-flex;align-items:center;gap:8px;margin-top:20px;\n  font-family:"Cormorant Garamond",Georgia,serif;font-size:.9rem;font-weight:600;\n  letter-spacing:.14em;text-transform:uppercase;color:var(--g600)}',
    '.back-link{display:inline-flex;align-items:center;gap:8px;margin-top:22px;\n  font-family:"EB Garamond",Georgia,serif;font-size:1rem;font-style:italic;color:var(--g700)}')
rep('.gal-count{position:absolute;right:14px;bottom:12px;font-family:"Cormorant Garamond",Georgia,serif;\n  font-size:.85rem;letter-spacing:.14em;color:var(--plate-ink,#3B2C1A);opacity:.5;pointer-events:none}',
    '.gal-count{position:absolute;right:12px;bottom:10px;font-family:"IBM Plex Mono",monospace;\n  font-size:.72rem;color:#3B2C1A;opacity:.45;pointer-events:none}')
rep('.gal-main{position:relative;background:var(--plate);border:1px solid var(--rule);border-radius:12px;',
    '.gal-main{position:relative;background:var(--plate);border:1px solid var(--rule-2);border-radius:0;')
rep('.gal-thumbs button{background:var(--plate);border:1px solid var(--rule);border-radius:8px;',
    '.gal-thumbs button{background:var(--plate);border:1px solid var(--rule-2);border-radius:0;')
rep('.rel .plate{background:var(--plate);border:1px solid var(--rule);border-radius:10px;aspect-ratio:1/1;',
    '.rel .plate{background:var(--plate);border:1px solid var(--rule-2);border-radius:0;aspect-ratio:1/1;')
rep('.rel:hover .plate img{transform:scale(1.05)}', '')
rep('.rel .plate img{width:100%;height:100%;object-fit:contain;transition:transform .3s}',
    '.rel .plate img{width:100%;height:100%;object-fit:contain}')
rep('.rel span{font-family:"Cormorant Garamond",Georgia,serif;font-size:.82rem;letter-spacing:.14em;\n  text-transform:uppercase;color:var(--ink-3);font-weight:600}',
    '.rel span{font-family:"IBM Plex Mono",monospace;font-size:.78rem;color:var(--g700)}')
rep('.romans{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(22px,3.5vw,48px)}',
    '.romans{display:none}')
rep('.spec-list li::before{content:"";position:absolute;left:0;top:.68em;width:6px;height:1px;background:var(--g400)}',
    '.spec-list li::before{content:"";position:absolute;left:0;top:.7em;width:5px;height:1px;background:var(--rule)}')
rep('.orn{display:flex;align-items:center;gap:14px;justify-content:center;color:var(--g400);padding-block:6px}',
    '.orn{display:none}')

open(p, 'w', encoding='utf-8').write(s)
sys.stderr.write('CSS pass: %d edits\n' % n)
for m in miss:
    sys.stderr.write('MISS: ' + m + '\n')
