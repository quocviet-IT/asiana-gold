import zipfile, json, os, sys, io, re, base64
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


def col_letters(n):
    s = ''
    while n >= 0:
        s = chr(n % 26 + 65) + s
        n = n // 26 - 1
    return s


def sheet_data(z, sst, want):
    wb = ET.fromstring(z.read('xl/workbook.xml'))
    wbrels = rels(z, 'xl/workbook.xml')
    for s in wb.findall('m:sheets/m:sheet', NS):
        if want not in s.get('name'):
            continue
        spath = norm('xl/workbook.xml', wbrels[s.get('{%s}id' % NS['r'])][0])
        cells = {}
        for c in ET.fromstring(z.read(spath)).iter('{%s}c' % NS['m']):
            ref, t = c.get('r'), c.get('t')
            v, isx = c.find('m:v', NS), c.find('m:is', NS)
            val = None
            if t == 's' and v is not None and v.text is not None:
                i = int(v.text)
                val = sst[i] if i < len(sst) else None
            elif isx is not None:
                val = ''.join(x.text or '' for x in isx.iter('{%s}t' % NS['m']))
            elif v is not None:
                val = v.text
            if val is not None and str(val).strip():
                cells[ref] = str(val).strip()
        drawing = None
        for rid, (tgt, typ) in rels(z, spath).items():
            if typ == 'drawing':
                drawing = norm(spath, tgt)
        imgs = []
        if drawing and drawing in z.namelist():
            drels = rels(z, drawing)
            for anch in list(ET.fromstring(z.read(drawing))):
                frm = anch.find('xdr:from', NS)
                blip = anch.find('.//a:blip', NS)
                if frm is None or blip is None:
                    continue
                tgt = drels.get(blip.get('{%s}embed' % NS['r']), (None,))[0]
                if tgt:
                    imgs.append(dict(row=int(frm.find('xdr:row', NS).text) + 1,
                                     col=int(frm.find('xdr:col', NS).text) + 1,
                                     media=norm(drawing, tgt)))
        return s.get('name'), cells, imgs
    return None, {}, []


def sst_of(z):
    out = []
    if 'xl/sharedStrings.xml' in z.namelist():
        for si in ET.fromstring(z.read('xl/sharedStrings.xml')):
            out.append(''.join(t.text or '' for t in si.iter('{%s}t' % NS['m'])))
    return out


def to_data_uri(z, media, box=620, q=76):
    raw = z.read(media)
    im = Image.open(io.BytesIO(raw))
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA')
        bg = Image.new('RGB', im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert('RGB')
    im.thumbnail((box, box), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=q, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode(), im.size


src = sys.argv[1]
z = zipfile.ZipFile(src)
sst = sst_of(z)
name, cells, imgs = sheet_data(z, sst, 'QLSPAG 1.0-TÊN TIẾNG ANH-ne')
sys.stderr.write('sheet=%s cells=%d imgs=%d\n' % (name, len(cells), len(imgs)))

# section headers: any cell whose text starts with ASIANA GOLD -
sections = {}
for ref, val in cells.items():
    if val.upper().startswith('ASIANA GOLD'):
        m = re.match(r'([A-Z])(\d+)', ref)
        row = int(m.group(2))
        head = val.split(chr(10))
        vi = head[0].replace('ASIANA GOLD -', '').strip(' -')
        en = head[1].strip() if len(head) > 1 else ''
        sections[row] = (vi, en)

seen = set()
products = []
for im in sorted(imgs, key=lambda x: (x['row'], x['col'])):
    L = col_letters(im['col'] - 1)
    code = cells.get(L + str(im['row'] + 1), '')
    names = cells.get(L + str(im['row'] + 2), '')
    agcell = cells.get(L + str(im['row'] + 3), '')
    if not names or not agcell:
        continue
    parts = [p.strip() for p in names.split(chr(10)) if p.strip()]
    vi = parts[0] if parts else ''
    en = parts[1] if len(parts) > 1 else ''
    aglines = [p.strip() for p in agcell.split(chr(10)) if p.strip()]
    ag = aglines[0] if aglines else ''
    if not re.match(r'^[A-Z]{2,3}[A-Z0-9.]*$', ag.replace(' ', '')):
        continue
    decode = []
    for ln in aglines[1:]:
        if '=' in ln:
            k, v = ln.split('=', 1)
            decode.append([k.strip(), v.strip()])
    sec = ('', '')
    for r in sorted(sections):
        if r <= im['row']:
            sec = sections[r]
    key = ag.replace(' ', '')
    if key in seen:
        continue
    seen.add(key)
    uri, size = to_data_uri(z, im['media'])
    products.append(dict(ag=key, ksc=code, vi=vi, en=en, decode=decode,
                         secVi=sec[0], secEn=sec[1], img=uri, w=size[0], h=size[1]))
    sys.stderr.write('  %-12s %-10s %-40s %s\n' % (key, code, vi[:38], sec[0][:22]))

json.dump(products, open(os.path.join(SP, 'products.json'), 'w', encoding='utf-8'), ensure_ascii=False)
total = sum(len(p['img']) for p in products)
sys.stderr.write('PRODUCTS %d   payload %.1f MB\n' % (len(products), total / 1048576))
