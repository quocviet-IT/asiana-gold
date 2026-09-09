import json, os, re, sys

SP = os.path.dirname(os.path.abspath(__file__))
prods = json.load(open(os.path.join(SP, 'products.json'), encoding='utf-8'))
specs = json.load(open(os.path.join(SP, 'specs.json'), encoding='utf-8'))

# --- normalise section headings into VI / EN halves -------------------------
FIX = {
    'DÂY CHUYỀN BI': ('Dây chuyền bi', 'Bead chain'),
    'LẮC TAY BI': ('Lắc tay bi', 'Bead bracelet'),
    'DÂY CHUYỀN MÌ': ('Dây chuyền mì', 'Snake chain'),
    'DÂY CHUYỀN MÌ DẸP': ('Dây chuyền mì dẹp', 'Herringbone chain'),
    'DÂY MÌ VUÔNG CÓ BI': ('Dây mì vuông có bi', 'Square snake chain with bead'),
}


def title_case_vi(s):
    s = s.strip()
    return s[:1] + s[1:].lower() if s.isupper() else s


for p in prods:
    sec = p.get('secVi', '').strip()
    en = p.get('secEn', '').strip()
    if sec in FIX:
        vi, en2 = FIX[sec]
        p['secVi'], p['secEn'] = vi, en2
    elif ' - ' in sec and not en:
        a, b = sec.rsplit(' - ', 1)
        p['secVi'], p['secEn'] = title_case_vi(a), title_case_vi(b)
    else:
        p['secVi'], p['secEn'] = title_case_vi(sec), title_case_vi(en)

# --- derive attributes ------------------------------------------------------
COLOR_WORDS = {'Y': ('Vàng', 'Yellow'), 'W': ('Trắng', 'White'), 'R': ('Hồng', 'Rose')}

for p in prods:
    dec = {k.strip(): v.strip() for k, v in p.get('decode', [])}
    # colours present in the code decode
    cols = []
    for k, v in p.get('decode', []):
        kk = k.strip().upper()
        if kk in COLOR_WORDS and v.strip().lower().startswith(COLOR_WORDS[kk][1].lower()):
            if kk not in cols:
                cols.append(kk)
    if not cols:
        m = re.match(r'^[CB]B?([YWR]+)', p['ag'])
        if m:
            cols = list(dict.fromkeys(m.group(1)))
    p['colors'] = cols or ['Y']
    # kind: chain / bracelet
    p['kind'] = 'bracelet' if p['ag'].startswith('B') else 'chain'
    # diameters mentioned in the VI name (e.g. "2.5mm & 4.0mm", "4 li")
    dias = [float(x) for x in re.findall(r'(\d+(?:\.\d+)?)\s*(?:mm|li)', p['vi'])]
    if not dias:
        m = re.match(r'^C[YW](\d\d)', p['ag'])
        if m:
            dias = [int(m.group(1)) / 10]
    p['dia'] = sorted(set(dias))

# --- attach spec groups -----------------------------------------------------
by_code = {}
for g in specs:
    for r in g['rows']:
        by_code.setdefault(r['y'].strip().upper(), g)
by_title = {g['title'].strip().lower(): g for g in specs}

attached = 0
for p in prods:
    g = by_code.get(p['ag'].upper()) or by_title.get(p['vi'].strip().lower())
    if g:
        p['spec'] = g
        attached += 1

order = ['Dây chuyền mì', 'Dây chuyền mì dẹp', 'Dây mì vuông có bi', 'Dây chuyền franco',
         'Dây chuyền khoen lật', 'Dây chuyền chữ cong', 'Dây chuyền bi', 'Lắc tay bi']
prods.sort(key=lambda p: (order.index(p['secVi']) if p['secVi'] in order else 99, p['ag']))

payload = dict(products=prods, specs=specs)
json.dump(payload, open(os.path.join(SP, 'payload.json'), 'w', encoding='utf-8'), ensure_ascii=False)

secs = {}
for p in prods:
    secs.setdefault((p['secVi'], p['secEn']), 0)
    secs[(p['secVi'], p['secEn'])] += 1
sys.stderr.write('products=%d  with-spec=%d  spec-groups=%d\n' % (len(prods), attached, len(specs)))
for (a, b), n in secs.items():
    sys.stderr.write('  %-24s %-32s %d\n' % (a, b, n))
alld = sorted({d for p in prods for d in p['dia']})
sys.stderr.write('diameters: %s\n' % alld)
sys.stderr.write('payload %.2f MB\n' % (os.path.getsize(os.path.join(SP, 'payload.json')) / 1048576))
