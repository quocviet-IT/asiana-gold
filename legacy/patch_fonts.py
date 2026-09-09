import os, sys

SP = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(SP, 'shell.html')
s = open(p, encoding='utf-8').read()
n = 0


def rep(old, new, count=1):
    global s, n
    if old not in s:
        sys.stderr.write('!! NOT FOUND: ' + old[:90].replace('\n', ' ') + '\n')
        return False
    s = s.replace(old, new, count)
    n += 1
    return True


# ---- 1. font loading: Cormorant Garamond + EB Garamond (Cardo stand-in) ----
rep('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:ital,wght@1,900&family=Be+Vietnam+Pro:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600&display=swap">',
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    'family=Archivo:ital,wght@1,900&'
    'family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600&'
    'family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&'
    'family=IBM+Plex+Mono:wght@400;500;600&display=swap">')

# ---- 2. root scale: a Garamond needs more room than a grotesque ----
rep('*{box-sizing:border-box}\nbody{background:var(--paper);color:var(--ink);\n'
    '  font-family:"Be Vietnam Pro","Segoe UI",system-ui,sans-serif;font-size:15px;line-height:1.62;\n'
    '  -webkit-font-smoothing:antialiased}',
    '*{box-sizing:border-box}\n'
    ':root{font-size:17px}\n'
    '/* type roles: Cormorant Garamond displays, EB Garamond reads, Plex Mono counts */\n'
    'body{background:var(--paper);color:var(--ink);\n'
    '  font-family:"EB Garamond",Georgia,"Times New Roman",serif;font-size:1rem;line-height:1.7;\n'
    '  -webkit-font-smoothing:antialiased}\n'
    '.sans{font-family:"Segoe UI",system-ui,-apple-system,sans-serif}')

# ---- 3. headings: light weight, italic accents, no bold anywhere ----
rep('h1,h2{font-family:"Playfair Display",Georgia,serif;font-weight:700;letter-spacing:-.01em}\n'
    'h1{font-size:clamp(2.05rem,4.4vw,3.4rem)}\n'
    'h2{font-size:clamp(1.6rem,3vw,2.35rem)}\n'
    'h3{font-family:"Be Vietnam Pro",sans-serif;font-size:1.02rem;font-weight:700;letter-spacing:-.01em}',
    'h1,h2{font-family:"Cormorant Garamond",Georgia,serif;font-weight:500;letter-spacing:0;line-height:1.08}\n'
    'h1{font-size:clamp(2.5rem,5.4vw,4.1rem)}\n'
    'h2{font-size:clamp(1.95rem,3.6vw,2.85rem)}\n'
    'h1 em,h2 em{font-style:italic;font-weight:400}\n'
    'h3{font-family:"Cormorant Garamond",Georgia,serif;font-size:1.3rem;font-weight:600;letter-spacing:.005em}')

# ---- 4. every small label becomes letterspaced serif caps ----
rep('.eyebrow{display:inline-flex;align-items:center;gap:8px;font-family:"IBM Plex Mono",monospace;\n'
    '  font-size:.68rem;letter-spacing:.2em;text-transform:uppercase;color:var(--g600);font-weight:500}',
    '.eyebrow{display:inline-flex;align-items:center;gap:9px;font-family:"Cormorant Garamond",Georgia,serif;\n'
    '  font-size:.82rem;letter-spacing:.2em;text-transform:uppercase;color:var(--g600);font-weight:600}')

rep('nav.main > button,.navitem > button{padding:9px 13px;border-radius:7px;font-size:.9rem;font-weight:500;\n'
    '  color:var(--ink-2);white-space:nowrap;transition:background .16s,color .16s;display:inline-flex;align-items:center;gap:6px}',
    'nav.main > button,.navitem > button{padding:9px 13px;border-radius:7px;\n'
    '  font-family:"Cormorant Garamond",Georgia,serif;font-size:.92rem;font-weight:600;\n'
    '  letter-spacing:.13em;text-transform:uppercase;\n'
    '  color:var(--ink-2);white-space:nowrap;transition:background .16s,color .16s;display:inline-flex;align-items:center;gap:6px}')

rep('.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;padding:12px 22px;\n'
    '  border-radius:8px;font-weight:600;font-size:.92rem;border:1px solid transparent;\n'
    '  transition:transform .14s,box-shadow .18s,background .18s;white-space:nowrap}',
    '.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;padding:13px 24px;\n'
    '  border-radius:8px;font-family:"Cormorant Garamond",Georgia,serif;font-weight:600;font-size:.95rem;\n'
    '  letter-spacing:.13em;text-transform:uppercase;border:1px solid transparent;\n'
    '  transition:transform .14s,box-shadow .18s,background .18s;white-space:nowrap}')
rep('.btn-gold{background:var(--metal);background-size:200% 100%;color:#2A1F09;font-weight:700;',
    '.btn-gold{background:var(--metal);background-size:200% 100%;color:#2A1F09;font-weight:600;')

# display numerals
rep('.rail b{display:block;font-family:"Playfair Display",serif;font-weight:700;font-size:1.6rem;color:var(--g600);line-height:1.1}',
    '.rail b{display:block;font-family:"Cormorant Garamond",Georgia,serif;font-weight:600;font-size:2rem;color:var(--g600);line-height:1.1}')
rep('.rail span{display:block;font-size:.78rem;color:var(--ink-2);margin-top:3px}',
    '.rail span{display:block;font-family:"Cormorant Garamond",Georgia,serif;font-size:.8rem;\n'
    '  letter-spacing:.11em;text-transform:uppercase;font-weight:600;color:var(--ink-2);margin-top:5px}')
rep('.step .n{font-family:"Playfair Display",serif;font-weight:700;font-size:2.5rem;line-height:1;',
    '.step .n{font-family:"Cormorant Garamond",Georgia,serif;font-weight:600;font-size:3rem;line-height:1;')
rep('.finder-sum div b{font-family:"Playfair Display",serif;font-size:1.25rem;color:var(--ink)}',
    '.finder-sum div b{font-family:"Cormorant Garamond",Georgia,serif;font-weight:600;font-size:1.55rem;color:var(--ink)}')

# small caps labels across chrome
for old, new in [
    ('footer h4{font-family:"IBM Plex Mono",monospace;font-size:.66rem;letter-spacing:.16em;text-transform:uppercase;\n  color:var(--g300);margin-bottom:14px;font-weight:600}',
     'footer h4{font-family:"Cormorant Garamond",Georgia,serif;font-size:.86rem;letter-spacing:.18em;text-transform:uppercase;\n  color:var(--g300);margin-bottom:14px;font-weight:600}'),
    ('thead th{font-family:"IBM Plex Mono",monospace;font-size:.66rem;letter-spacing:.11em;text-transform:uppercase;\n  color:var(--g700);font-weight:600;background:var(--g50)}',
     'thead th{font-family:"Cormorant Garamond",Georgia,serif;font-size:.84rem;letter-spacing:.13em;text-transform:uppercase;\n  color:var(--g700);font-weight:600;background:var(--g50)}'),
    ('.fgroup > p{font-family:"IBM Plex Mono",monospace;font-size:.64rem;letter-spacing:.14em;text-transform:uppercase;\n  color:var(--g700);margin-bottom:9px;font-weight:600}',
     '.fgroup > p{font-family:"Cormorant Garamond",Georgia,serif;font-size:.84rem;letter-spacing:.15em;text-transform:uppercase;\n  color:var(--g700);margin-bottom:9px;font-weight:600}'),
    ('.fc > span{font-family:"IBM Plex Mono",monospace;font-size:.64rem;letter-spacing:.14em;\n  text-transform:uppercase;color:var(--g700);font-weight:600}',
     '.fc > span{font-family:"Cormorant Garamond",Georgia,serif;font-size:.84rem;letter-spacing:.15em;\n  text-transform:uppercase;color:var(--g700);font-weight:600}'),
    ('.finder-sum div span{display:block;font-family:"IBM Plex Mono",monospace;font-size:.63rem;\n  letter-spacing:.12em;text-transform:uppercase;color:var(--g700)}',
     '.finder-sum div span{display:block;font-family:"Cormorant Garamond",Georgia,serif;font-size:.82rem;font-weight:600;\n  letter-spacing:.14em;text-transform:uppercase;color:var(--g700)}'),
    ('.kv dt{color:var(--g700);font-family:"IBM Plex Mono",monospace;font-size:.68rem;letter-spacing:.1em;\n  text-transform:uppercase;padding-top:3px;font-weight:600}',
     '.kv dt{color:var(--g700);font-family:"Cormorant Garamond",Georgia,serif;font-size:.86rem;letter-spacing:.13em;\n  text-transform:uppercase;padding-top:2px;font-weight:600}'),
    ('.field label{font-family:"IBM Plex Mono",monospace;font-size:.65rem;letter-spacing:.12em;\n  text-transform:uppercase;color:var(--g700);font-weight:600}',
     '.field label{font-family:"Cormorant Garamond",Georgia,serif;font-size:.85rem;letter-spacing:.14em;\n  text-transform:uppercase;color:var(--g700);font-weight:600}'),
    ('.cat-tile .body u{text-decoration:none;margin-top:auto;padding-top:11px;display:flex;align-items:center;gap:6px;\n  font-family:"IBM Plex Mono",monospace;font-size:.72rem;color:var(--g600);letter-spacing:.05em}',
     '.cat-tile .body u{text-decoration:none;margin-top:auto;padding-top:11px;display:flex;align-items:center;gap:6px;\n  font-family:"Cormorant Garamond",Georgia,serif;font-size:.85rem;font-weight:600;color:var(--g600);\n  letter-spacing:.14em;text-transform:uppercase}'),
]:
    rep(old, new)

# tile / card titles read as display, not body
rep('.cat-tile .body b{font-size:1rem;font-weight:700}',
    '.cat-tile .body b{font-family:"Cormorant Garamond",Georgia,serif;font-size:1.3rem;font-weight:600;line-height:1.2}')
rep('.cat-tile .body i{font-style:normal;font-size:.79rem;color:var(--ink-3)}',
    '.cat-tile .body i{font-style:italic;font-size:.92rem;color:var(--ink-3)}')
rep('.card .m b{font-size:.89rem;font-weight:600;line-height:1.32}',
    '.card .m b{font-family:"Cormorant Garamond",Georgia,serif;font-size:1.15rem;font-weight:600;line-height:1.22}')
rep('.card .m i{font-style:normal;font-size:.76rem;color:var(--ink-3);line-height:1.36}',
    '.card .m i{font-style:italic;font-size:.88rem;color:var(--ink-3);line-height:1.34}')
rep('.row b{display:block;font-size:.9rem;font-weight:600}',
    '.row b{display:block;font-family:"Cormorant Garamond",Georgia,serif;font-size:1.15rem;font-weight:600;line-height:1.25}')
rep('.row i{font-style:normal;font-size:.77rem;color:var(--ink-3)}',
    '.row i{font-style:italic;font-size:.88rem;color:var(--ink-3)}')
rep('.mega b{display:block;font-size:.87rem;font-weight:600}',
    '.mega b{display:block;font-family:"Cormorant Garamond",Georgia,serif;font-size:1.1rem;font-weight:600}')
rep('.mega i{font-style:normal;font-size:.74rem;color:var(--ink-3)}',
    '.mega i{font-style:italic;font-size:.86rem;color:var(--ink-3)}')
rep('.qline b{display:block;font-size:.85rem;font-weight:600;line-height:1.3}',
    '.qline b{display:block;font-family:"Cormorant Garamond",Georgia,serif;font-size:1.08rem;font-weight:600;line-height:1.25}')
rep('.qa summary{padding:16px 20px;cursor:pointer;font-weight:600;font-size:.95rem;display:flex;\n  align-items:center;gap:14px;list-style:none}',
    '.qa summary{padding:16px 20px;cursor:pointer;font-family:"Cormorant Garamond",Georgia,serif;\n'
    '  font-weight:600;font-size:1.2rem;display:flex;align-items:center;gap:14px;list-style:none}')

# the lede carries the reference\'s italic voice
rep('.lede{color:var(--ink-2);font-size:1.02rem;max-width:62ch}',
    '.lede{color:var(--ink-2);font-size:1.05rem;font-style:italic;max-width:60ch}')

# chrome that must stay sans / mono
rep('.f-zalo{background:#0068FF;color:#fff;font-weight:800;font-size:.78rem;letter-spacing:-.02em}',
    '.f-zalo{background:#0068FF;color:#fff;font-family:"Segoe UI",system-ui,sans-serif;\n'
    '  font-weight:800;font-size:.76rem;letter-spacing:-.02em}')
rep('.util{background:var(--espresso-2);color:var(--onDark-2);font-size:.79rem}',
    '.util{background:var(--espresso-2);color:var(--onDark-2);font-family:"Cormorant Garamond",Georgia,serif;\n'
    '  font-size:.88rem;letter-spacing:.09em;text-transform:uppercase;font-weight:600}')

# ---- 5. italic accent in every hero headline, the reference\'s signature move ----
rep('hVi:"Dây chuyền vàng 18K,<br>sản xuất theo mã.", hEn:"18K gold chains,<br>made to code.",',
    'hVi:"Dây chuyền vàng 18K,<br><em>sản xuất theo mã.</em>", hEn:"18K gold chains,<br><em>made to code.</em>",')
rep('hVi:"Đủ cỡ, đủ tuổi vàng,<br>đủ chiều dài.", hEn:"Every gauge, purity<br>and length.",',
    'hVi:"Đủ cỡ, đủ tuổi vàng,<br><em>đủ chiều dài.</em>", hEn:"Every gauge, purity<br><em>and length.</em>",')
rep('hVi:"Gửi mẫu của bạn,<br>xưởng dựng khuôn riêng.", hEn:"Send your sample,<br>we cut the die.",',
    'hVi:"Gửi mẫu của bạn,<br><em>xưởng dựng khuôn riêng.</em>", hEn:"Send your sample,<br><em>we cut the die.</em>",')
rep('<h2 style="margin:12px 0 14px">${t("Đọc được cả sợi dây<br>chỉ từ tám ký tự","Eight characters<br>describe the whole chain")}</h2>',
    '<h2 style="margin:12px 0 14px">${t("Đọc được cả sợi dây<br><em>chỉ từ tám ký tự</em>","Eight characters<br><em>describe the whole chain</em>")}</h2>')

open(p, 'w', encoding='utf-8').write(s)
sys.stderr.write('applied %d replacements\n' % n)
for bad in ['Playfair', 'Be Vietnam Pro']:
    sys.stderr.write('%-16s still present: %d\n' % (bad, s.count(bad)))
