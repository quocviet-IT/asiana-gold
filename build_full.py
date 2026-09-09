# -*- coding: utf-8 -*-
"""Lift every product that has both a photo and a name out of both catalogues,
writing photos as separate files so the page stays small enough to load fast.

Ownership rule is the strict one: a photo belongs to the code sitting directly
beneath it in its own column. A looser match mixed up neighbouring variants."""
import zipfile, os, sys, re, io, json, hashlib, shutil
from collections import defaultdict
from xml.etree import ElementTree as ET
from PIL import Image

NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'xdr': 'http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'pr': 'http://schemas.openxmlformats.org/package/2006/relationships'}
BS = chr(92)
SP = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]                      # directory to write img/ into
SRCS = sys.argv[2:]

CODE = re.compile(r'^(?:KSC|KSL|AGC)\d{5}$|^C[YWBM][A-Z0-9.\-]{2,}$|^BB[A-Z0-9.\-]{2,}$')
NOISE = re.compile(r'^(STT|MÃ|HÌNH|GHI|VÀNG|CHỈ|GRAM|CHIỀU|18K|BẠC|SV-)', re.I)


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


products = {}
zips = {}
for path in SRCS:
    z = zipfile.ZipFile(path)
    zips[path] = z
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
                cells[ref] = ' '.join(str(val).split())
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
            code = name = en = None
            for d in (1, 2, 3, 4):
                raw = cells.get(col_letters(col) + str(row + d))
                if not raw:
                    continue
                parts = [x.strip() for x in raw.split(chr(10)) if x.strip()]
                first = parts[0]
                if code is None and CODE.match(first.upper()) and not NOISE.match(first):
                    code = first.upper()
                    continue
                if code and name is None and len(first) > 6 and not CODE.match(first.upper()):
                    name = first
                    if len(parts) > 1 and re.search(r'[a-z]', parts[1]) and not CODE.match(parts[1].upper()):
                        en = parts[1]
            if not code:
                continue
            p = products.setdefault(code, {'ag': code, 'vi': name, 'en': en, 'media': []})
            if name and not p['vi']:
                p['vi'] = name
            if en and not p['en']:
                p['en'] = en
            if (path, norm(drawing, t3)) not in p['media']:
                p['media'].append((path, norm(drawing, t3)))

products = {k: v for k, v in products.items() if v['vi']}
sys.stderr.write('mã có ảnh + tên: %d\n' % len(products))

imgdir = os.path.join(OUT, 'img')
if os.path.isdir(imgdir):
    shutil.rmtree(imgdir)
os.makedirs(imgdir)

MAX_PER = 3
seen_hash = {}
total_bytes = 0
out = []
for code in sorted(products):
    p = products[code]
    files = []
    for src, media in p['media'][:MAX_PER]:
        raw = zips[src].read(media)
        h = hashlib.md5(raw).hexdigest()[:16]
        if h in seen_hash:
            if seen_hash[h] not in files:
                files.append(seen_hash[h])
            continue
        try:
            im = Image.open(io.BytesIO(raw))
        except Exception:
            continue
        if im.mode in ('RGBA', 'LA', 'P'):
            im = im.convert('RGBA')
            bg = Image.new('RGB', im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[-1])
            im = bg
        else:
            im = im.convert('RGB')
        if min(im.size) < 180:
            continue
        im.thumbnail((620, 620), Image.LANCZOS)
        fn = h + '.jpg'
        im.save(os.path.join(imgdir, fn), 'JPEG', quality=76, optimize=True, progressive=True)
        total_bytes += os.path.getsize(os.path.join(imgdir, fn))
        seen_hash[h] = fn
        files.append(fn)
    if not files:
        continue
    out.append({'ag': code, 'vi': p['vi'], 'en': p['en'] or '', 'imgs': files})

json.dump(out, open(os.path.join(SP, 'products_full.json'), 'w', encoding='utf-8'), ensure_ascii=False)
sys.stderr.write('sản phẩm xuất được : %d\n' % len(out))
sys.stderr.write('file ảnh           : %d  (%.1f MB)\n' % (len(seen_hash), total_bytes / 1048576))
sys.stderr.write('trung bình mỗi ảnh : %.0f KB\n' % (total_bytes / max(1, len(seen_hash)) / 1024))
