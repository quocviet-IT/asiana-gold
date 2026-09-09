# -*- coding: utf-8 -*-
"""How many products can be lifted out of every sheet, not just the bilingual tab?

Same strict ownership rule as before: an image belongs to a code only when that
code sits directly beneath it, in the image's own column. Anything looser mixed
up neighbouring variants last time."""
import zipfile, os, sys, re, hashlib
from collections import defaultdict
from xml.etree import ElementTree as ET

NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'xdr': 'http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'pr': 'http://schemas.openxmlformats.org/package/2006/relationships'}
BS = chr(92)
CODE = re.compile(r'^(?:KSC|KSL|AGC)\d{5}|^C[YWBM][A-Z0-9.\-]{2,}|^BB[A-Z0-9.\-]{2,}')
NOISE = re.compile(r'^(STT|MÃ|HÌNH|GHI CHÚ|VÀNG|CHỈ|GRAM|CHIỀU DÀI|18K|BẠC)', re.I)


def rels(z, p):
    rp = os.path.dirname(p) + '/_rels/' + os.path.basename(p) + '.rels'
    o = {}
    if rp in z.namelist():
        for r in ET.fromstring(z.read(rp)).findall('pr:Relationship', NS):
            o[r.get('Id')] = (r.get('Target'), r.get('Type').rsplit('/', 1)[-1])
    return o


def norm(b, t):
    if t.startswith('/'):
        return t.lstrip('/')
    return os.path.normpath(os.path.join(os.path.dirname(b), t)).replace(BS, '/')


def col_letters(k):
    s = ''
    while k >= 0:
        s = chr(k % 26 + 65) + s
        k = k // 26 - 1
    return s


found = {}          # code -> dict
img_of = defaultdict(set)

for path in sys.argv[1:]:
    z = zipfile.ZipFile(path)
    sst = []
    if 'xl/sharedStrings.xml' in z.namelist():
        for si in ET.fromstring(z.read('xl/sharedStrings.xml')):
            sst.append(''.join(t.text or '' for t in si.iter('{%s}t' % NS['m'])))
    wb = ET.fromstring(z.read('xl/workbook.xml'))
    wr = rels(z, 'xl/workbook.xml')
    for sh in wb.findall('m:sheets/m:sheet', NS):
        tgt = wr.get(sh.get('{%s}id' % NS['r']), (None,))[0]
        if not tgt:
            continue
        spath = norm('xl/workbook.xml', tgt)
        if spath not in z.namelist():
            continue
        cells = {}
        for c in ET.fromstring(z.read(spath)).iter('{%s}c' % NS['m']):
            ref, ty = c.get('r'), c.get('t')
            v, isx = c.find('m:v', NS), c.find('m:is', NS)
            val = None
            if ty == 's' and v is not None and v.text is not None:
                i = int(v.text)
                val = sst[i] if i < len(sst) else None
            elif isx is not None:
                val = ''.join(x.text or '' for x in isx.iter('{%s}t' % NS['m']))
            elif v is not None:
                val = v.text
            if val and str(val).strip():
                cells[ref] = str(val).strip()
        drawing = None
        for _, (t2, typ) in rels(z, spath).items():
            if typ == 'drawing':
                drawing = norm(spath, t2)
        if not drawing or drawing not in z.namelist():
            continue
        drels = rels(z, drawing)
        for anch in list(ET.fromstring(z.read(drawing))):
            frm = anch.find('xdr:from', NS)
            blip = anch.find('.//a:blip', NS)
            if frm is None or blip is None:
                continue
            t3 = drels.get(blip.get('{%s}embed' % NS['r']), (None,))[0]
            if not t3:
                continue
            col = int(frm.find('xdr:col', NS).text)
            row = int(frm.find('xdr:row', NS).text) + 1
            media = norm(drawing, t3)
            code, name = None, None
            for d in (1, 2, 3, 4):
                ref = col_letters(col) + str(row + d)
                txt = cells.get(ref)
                if not txt:
                    continue
                first = txt.split(chr(10))[0].strip()
                if code is None and CODE.match(first.upper()) and not NOISE.match(first):
                    code = first.upper()
                    continue
                if code and name is None and len(first) > 6 and not CODE.match(first.upper()):
                    name = first
            if not code:
                continue
            e = found.setdefault(code, {'name': None, 'imgs': set(), 'sheets': set()})
            if name and not e['name']:
                e['name'] = name
            e['imgs'].add((path, media))
            e['sheets'].add(sh.get('name'))

withname = {k: v for k, v in found.items() if v['name']}
print('mã có ít nhất một ảnh          : %d' % len(found))
print('trong đó có cả tên tiếng Việt  : %d' % len(withname))
print('tổng số ảnh gắn được vào mã    : %d' % sum(len(v['imgs']) for v in found.values()))
print()
print('phân bố theo tiền tố:')
pref = defaultdict(int)
for k in withname:
    pref[re.match(r'^[A-Z]+', k).group(0)] += 1
for k, v in sorted(pref.items(), key=lambda x: -x[1]):
    print('   %-5s %d' % (k, v))
print()
print('ví dụ 12 mẫu có tên:')
for k in list(withname)[:12]:
    print('   %-12s %-46s %d ảnh' % (k, withname[k]['name'][:46], len(withname[k]['imgs'])))
