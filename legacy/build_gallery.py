"""Collect extra photos for a product ONLY where the sheet proves ownership:
the image is anchored directly above a cell, in its own column, whose text is
that product's AG or internal code. Anything looser pulls in neighbouring
variants — verified: a loose match gave CY25SR two photos of twisted/cut weaves."""
import zipfile, json, os, sys, io, re, base64, hashlib
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


def rels(z, path):
    rp = os.path.dirname(path) + '/_rels/' + os.path.basename(path) + '.rels'
    out = {}
    if rp in z.namelist():
        for rel in ET.fromstring(z.read(rp)).findall('pr:Relationship', NS):
            out[rel.get('Id')] = (rel.get('Target'), rel.get('Type').rsplit('/', 1)[-1])
    return out


def norm(base, target):
    if target.startswith('/'):
        return target.lstrip('/')
    return os.path.normpath(os.path.join(os.path.dirname(base), target)).replace(BS, '/')


def col_letters(k):
    s = ''
    while k >= 0:
        s = chr(k % 26 + 65) + s
        k = k // 26 - 1
    return s


def scan(path):
    z = zipfile.ZipFile(path)
    sst = []
    if 'xl/sharedStrings.xml' in z.namelist():
        for si in ET.fromstring(z.read('xl/sharedStrings.xml')):
            sst.append(''.join(t.text or '' for t in si.iter('{%s}t' % NS['m'])))
    wb = ET.fromstring(z.read('xl/workbook.xml'))
    wbrels = rels(z, 'xl/workbook.xml')
    found = []
    for sh in wb.findall('m:sheets/m:sheet', NS):
        tgt = wbrels.get(sh.get('{%s}id' % NS['r']), (None,))[0]
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
            # STRICT: own column only, the three rows immediately beneath
            owners = []
            for d in (1, 2, 3):
                ref = col_letters(col) + str(row + d)
                if ref in cells:
                    first = cells[ref].split(chr(10))[0].strip().upper()
                    if re.fullmatch(r'[A-Z]{2,4}[A-Z0-9.\-]{1,14}', first):
                        owners.append(first)
            if owners:
                found.append((owners, norm(drawing, t3), path))
    return z, found


zips, index = {}, defaultdict(list)
for path in (sys.argv[1], sys.argv[2]):
    z, found = scan(path)
    zips[path] = z
    for owners, media, src in found:
        for o in owners:
            index[o].append((src, media))
    sys.stderr.write('%s -> %d owned images\n' % (os.path.basename(path)[:8], len(found)))


def encode(src, media, box=560, q=74):
    raw = zips[src].read(media)
    h = hashlib.md5(raw).hexdigest()
    im = Image.open(io.BytesIO(raw))
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA')
        bg = Image.new('RGB', im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert('RGB')
    if min(im.size) < 200:
        return None, h
    im.thumbnail((box, box), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=q, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode(), h


payload = json.load(open(os.path.join(SP, 'payload.backup.json'), encoding='utf-8'))
prods = payload['products']
MAX = 4
counts = defaultdict(int)
for p in prods:
    keys = [p['ag'].upper()]
    if p.get('ksc'):
        keys += [k.strip().upper() for k in re.split(r'[-\s]+', p['ksc']) if len(k.strip()) > 3]
    gallery = [p['img']]
    hashes = {hashlib.md5(base64.b64decode(p['img'].split(',', 1)[1])).hexdigest()}
    seen = set()
    for k in keys:
        for src, media in index.get(k, []):
            if len(gallery) >= MAX or media in seen:
                continue
            seen.add(media)
            uri, h = encode(src, media)
            if uri is None or h in hashes:
                continue
            hashes.add(h)
            gallery.append(uri)
    p['gallery'] = gallery
    counts[len(gallery)] += 1

json.dump(payload, open(os.path.join(SP, 'payload.json'), 'w', encoding='utf-8'), ensure_ascii=False)
sys.stderr.write('gallery sizes: %s\n' % dict(sorted(counts.items())))
sys.stderr.write('with >1 photo: %d / %d\n' % (sum(1 for p in prods if len(p['gallery']) > 1), len(prods)))
sys.stderr.write('payload %.2f MB\n' % (os.path.getsize(os.path.join(SP, 'payload.json')) / 1048576))
