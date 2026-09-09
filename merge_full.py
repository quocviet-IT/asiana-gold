# -*- coding: utf-8 -*-
"""Fold the full catalogue into the payload.

Photos move out of the HTML into files: at ~330 products, inlining them as data
URIs would push the page past 15 MB. The three hero cut-outs stay inline so the
first screen paints without a second request."""
import json, os, sys, re, base64, hashlib
from collections import Counter

SP = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1]
IMGDIR = os.path.join(SITE, 'img')

pay = json.load(open(os.path.join(SP, 'payload.json'), encoding='utf-8'))
full = json.load(open(os.path.join(SP, 'products_full.json'), encoding='utf-8'))

# rows whose "name" is an internal status note, not a product
STATUS = re.compile(r'chưa\s*(sản xuất|có|làm)|không\s*(sản xuất|làm|được)|ngưng|đang làm|chờ', re.I)
dropped = [p for p in full if STATUS.search(p['vi'])]
full = [p for p in full if not STATUS.search(p['vi'])]

# ---- existing photos move from base64 into the same file store ---------------
def stash(uri):
    raw = base64.b64decode(uri.split(',', 1)[1])
    h = hashlib.md5(raw).hexdigest()[:16] + '.jpg'
    path = os.path.join(IMGDIR, h)
    if not os.path.exists(path):
        open(path, 'wb').write(raw)
    return 'img/' + h

for p in pay['products']:
    p['gallery'] = [stash(u) for u in (p.get('gallery') or [p['img']])]
    p['img'] = p['gallery'][0]

# ---- family, kind, gauge for the newcomers ----------------------------------
FAM = [
    (r'lắc tay.*bi|lắc bi', 'Lắc tay bi', 'Bead bracelet'),
    (r'lắc tay', 'Lắc tay', 'Bracelet'),
    (r'lắc chân', 'Lắc chân', 'Anklet'),
    (r'vỏ xoàn', 'Vỏ xoàn', 'Diamond setting'),
    (r'chữ f|chữ s', 'Dây chuyền chữ F, chữ S', 'F and S chain'),
    (r'bện', 'Dây chuyền bện', 'Braided chain'),
    (r'ghép', 'Dây chuyền ghép', 'Combination chain'),
    (r'franco', 'Dây chuyền franco', 'Franco chain'),
    (r'khoen lật', 'Dây chuyền khoen lật', 'Curb chain'),
    (r'chữ cong|cong', 'Dây chuyền chữ cong', 'Cable chain'),
    (r'mì dẹp', 'Dây chuyền mì dẹp', 'Herringbone chain'),
    (r'mì', 'Dây chuyền mì', 'Snake chain'),
    (r'\bbi\b|bi ', 'Dây chuyền bi', 'Bead chain'),
    (r'hỏa tiễn|hoả tiễn', 'Dây hoả tiễn', 'Rocket chain'),
    (r'oval', 'Dây oval', 'Oval chain'),
    (r'bông mai', 'Dây bông mai', 'Blossom chain'),
    (r'móc máy', 'Dây móc máy', 'Machine-linked chain'),
    (r'khắc ống', 'Dây khắc ống', 'Engraved tube chain'),
    (r'hộp', 'Dây hộp', 'Box chain'),
    (r'dẹp', 'Dây dẹp', 'Flat chain'),
]


def family(name):
    low = name.lower()
    for pat, vi, en in FAM:
        if re.search(pat, low):
            return vi, en
    return 'Kiểu khác', 'Other styles'


def gauges(name, code):
    d = [float(x) for x in re.findall(r'(\d+(?:[.,]\d+)?)\s*(?:mm|li)', name.replace(',', '.'))]
    if not d:
        m = re.match(r'^C[YW](\d\d)', code)
        if m:
            d = [int(m.group(1)) / 10]
    return sorted(set(x for x in d if 0.5 <= x <= 20))


def colours(code, name):
    c = []
    m = re.match(r'^C?B?B?([YWR]{1,3})', code)
    if m and not code.startswith(('KSC', 'KSL', 'AGC')):
        c = list(dict.fromkeys(m.group(1)))
    return c


have = {p['ag'].upper() for p in pay['products']}
added = 0
for p in full:
    if p['ag'].upper() in have:
        continue
    vi, en = family(p['vi'])
    pay['products'].append({
        'ag': p['ag'], 'ksc': '', 'vi': p['vi'], 'en': p['en'] or '',
        'decode': [], 'secVi': vi, 'secEn': en,
        'img': 'img/' + p['imgs'][0],
        'gallery': ['img/' + f for f in p['imgs']],
        'colors': colours(p['ag'], p['vi']),
        'kind': 'bracelet' if re.match(r'^\s*lắc', p['vi'], re.I) else 'chain',
        'dia': gauges(p['vi'], p['ag']),
        'silver': None,
    })
    added += 1

json.dump(pay, open(os.path.join(SP, 'payload.json'), 'w', encoding='utf-8'), ensure_ascii=False)

fams = Counter(p['secVi'] for p in pay['products'])
sys.stderr.write('bỏ vì là ghi chú tình trạng : %d\n' % len(dropped))
for p in dropped:
    sys.stderr.write('    %-12s %s\n' % (p['ag'], p['vi'][:64]))
sys.stderr.write('thêm mới                    : %d\n' % added)
sys.stderr.write('tổng sản phẩm               : %d\n' % len(pay['products']))
sys.stderr.write('file ảnh trong img/         : %d\n' % len(os.listdir(IMGDIR)))
sys.stderr.write('payload                     : %.2f MB\n' % (os.path.getsize(os.path.join(SP, 'payload.json')) / 1048576))
sys.stderr.write('\ndòng sản phẩm:\n')
for k, v in fams.most_common():
    sys.stderr.write('   %-30s %d\n' % (k, v))
